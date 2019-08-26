# face-checker
Данная программа сканирует загружаемые в неё изображения лиц, считывает с них эмбеддинги, помещает их в базу вместе с хеш-суммами изображений и выводит из базы список хеш-сумм изображений с похожими лицами.

Для использования программы нужно после запуска server.py в браузере перейти по адресу http://127.0.0.1:5000/ или http://localhost:5000/ , затем нажать на кнопку "Выберите файл", выбрать фотографию с изображением лица в открывшемся окне проводника и нажать кнопку "Отправить", после чего программа обработает фото и выведет хеш-суммы изображений из базы с похожими лицами или сообщение "No matches found", если похожих лиц в базе нету. База хранится в файле db_hash_encoding.csv, если такого фала нет, программа создаст его автоматически.

Для работы программы требуются:
python 3.6+
flask 1.1.1+
opencv 3.4.1+
pandas 0.25.0+
numpy 1.16.4+
dlib 19.17+
face-recognition 1.2.3+

face-recognition - это wrapper dlib, поэтому dlib должен быть установлен заранее, для установки face-recognition на mac или linux используйте комманду:
pip install face_recognition
Для установки face-recognition на windows используйте команду:
pip install --no-dependencies face_recognition
