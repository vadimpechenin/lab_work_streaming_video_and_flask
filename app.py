import time
from importlib import import_module
import os

from flask import Flask, render_template, Response

import cv2
import numpy as np

from io import BytesIO #бинарный поток в памяти

# Эмулятор камеры
#import camera driver
if os.environ.get('CAMERA'):
    Camera = import_module('camera_' + os.environ['CAMERA']).Camera
else:
    from camera import Camera

app = Flask(__name__)


@app.route('/')
def index():
    """Домашняя страница."""
    return render_template('index.html')


def gen(camera):
    """Функция генерации видеопотока."""
    while True:
        frame = camera.get_frame()
        #Преобразование изображения из byte string в матрицы пикселей для дальнейшей работы
        nparr = np.fromstring(frame, np.uint8)
        im = cv2.imdecode(nparr, cv2.IMREAD_UNCHANGED)
        #cv2.imshow('ImageWindow', im)
        #cv2.waitKey()
        #Алгоритм обработки можно взять выделение контуров, яркостная нормализация, детектирование объектов и т.д.
        #Пороговая обработка
        im_processing = np.zeros((im.shape[0], im.shape[1]))
        for j in range(1):
            for i in range(im.shape[1]):
                idx = np.where(im[:,i,j]>200)
                im_processing[idx[0], i] = 255

        #Обратное преобразование
        is_success, im_buf_arr = cv2.imencode(".jpg", im_processing)
        f = BytesIO(im_buf_arr)
        byte_im = f.getvalue()
        time.sleep(1)

        # Создание генератора (коллекция, продущирующая элементы на лету и повторяемая лишь один раз)
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + byte_im + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Маршрут потокового видео. Поместите это в атрибут src тега img."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    #app.run(host='0.0.0.0', debug=True, threaded=True)
    app.run(debug=True)


