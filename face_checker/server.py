from flask import Flask, request, jsonify
import pandas as pd
import numpy as np
import face_recognition
import hashlib
import os.path
import cv2
import io

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
MAX_DISTANCE = 0.5


def process_hashes_and_encodings(image_hash, face_encodings):
    if os.path.exists('db_hash_encoding.csv'):
        db_hash_encoding = pd.read_csv("db_hash_encoding.csv")
    else:
        db_hash_encoding = pd.DataFrame()

    known_img_hashes, known_face_encodings = [], []
    for img_hash in db_hash_encoding.columns:
        known_img_hashes.append(img_hash)
        known_face_encodings.append(list(db_hash_encoding[img_hash]))

    db_hash_encoding[image_hash] = face_encodings[0]
    db_hash_encoding.to_csv('db_hash_encoding.csv', index=False)

    distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])

    rec_img_hashes = []
    if np.any(distances <= MAX_DISTANCE):
        match_idx = np.nonzero(distances <= MAX_DISTANCE)
        rec_img_hashes.append(np.array(known_img_hashes)[match_idx])
        rec_img_hashes = list(rec_img_hashes[0])
    else:
        rec_img_hashes = 'No matches found'

    # top, right, bottom, left = face_location[0]
    # cv2.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)

    # if (img.shape[0] > 800) or (img.shape[1] > 1500):
    #     res_img = cv2.resize(img, (600, 800))
    #     cv2.imshow('photo', res_img)
    # else:
    #     cv2.imshow('photo', img)
    # cv2.waitKey()

    return rec_img_hashes


@app.route('/')
def index():
    return '''
    <!doctype html>
    <title>Upload Photo</title>
    <h2>Upload Photo</h2>
    <form action="/upload_photo" method=post enctype=multipart/form-data>
      <p><input type=file name=photo accept="image/*">
         <input type=submit>
    </form>
    '''


@app.route('/upload_photo', methods=['POST'])
def upload_photo():
    photo = request.files['photo']

    in_memory_file = io.BytesIO()
    photo.save(in_memory_file)
    image_data = np.frombuffer(in_memory_file.getvalue(), dtype=np.uint8)
    img = cv2.imdecode(image_data, cv2.IMREAD_COLOR)

    image_hash = hashlib.md5()
    image_hash.update(image_data)
    image_hash = image_hash.hexdigest()

    face_location = face_recognition.face_locations(img)
    face_encodings = face_recognition.face_encodings(img, face_location)

    if face_encodings:
        rec_img_hashes = process_hashes_and_encodings(image_hash, face_encodings)
    else:
        rec_img_hashes = 'Face not found'

    return jsonify(rec_img_hashes)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=int("5000"), debug=True)
