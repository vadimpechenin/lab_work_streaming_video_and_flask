#D:\gstreamer\1.0\x86\bin>gst-launch-1.0.exe  multifilesrc loop=true start-index=0 stop-index=0 location=d:/python/temp.png ! decodebin ! identity sleep-time=1000000 ! videoconvert ! autovideosink
import shutil
import time
import os,sys
from PIL import Image, ImageFont, ImageDraw, ImageFile
from io import BytesIO #бинарный поток в памяти
from base_camera import BaseCamera

import cv2
pl = 1

if (pl==1):
    im = cv2.imread("test.jpg")
    im = cv2.resize(im, (300, 500))
    font = cv2.FONT_HERSHEY_PLAIN
    color = (0, 0, 255)
    text = time.strftime("%m/%d  %H:%M:%S") + u" Samara time"
    cv2.putText(im, text=text, fontFace=font,  org=(150, 150), fontScale=1, color=color, thickness=1)
    is_success, im_buf_arr = cv2.imencode(".jpg", im)

    cv2.waitKey(0)
    cv2.imwrite("d:\\PYTHON\\Magistracy\\2 семестр\\ПРЗП\\Lab3\\temp\\temp.jpg", im)
    f = BytesIO(im_buf_arr)
    byte_im = f.getvalue()
    f.name = "sdf.jpg"
else:
    im = Image.new("RGB", (300, 30), (220, 180, 180))
    #im.format'JPEG'
    dr = ImageDraw.Draw(im)
    font = ImageFont.truetype(os.path.join("fonts", "arial.ttf"), 16)
    text =time.strftime("%m/%d  %H:%M:%S") +u" время Самарское"
    dr.text((10, 5), text, font=font, fill="#000000")
    im.save("d:\\PYTHON\\Magistracy\\2 семестр\\ПРЗП\\Lab3\\temp\\temp.jpg")

    dr.rectangle((0,0,300,500),fill="#FFFFFF")
    text =time.strftime("%m/%d  %H:%M:%S") +u" время Самарское"
    dr.text((10, 5),text, font=font, fill="#000000")
    f = BytesIO()
    f.name="sdf.jpg"


if (pl==1):
    #cv2.imwrite("JPEG", f)
    pass
else:
    im.save(f,"JPEG")
f.seek(0)

f.close()

class Camera(BaseCamera):
    """Реализация эмуляции камеры, которая передает повторяющуюся последовательность
    файлов 1.jpg, 2.jpg и 3.jpg со скоростью один кадр в секунду."""
    #imgs = [open(f + '.jpg', 'rb').read() for f in ['1', '2', '3']]

    @staticmethod
    def frames():

        while True:
            text =time.strftime("%m/%d  %H:%M:%S") +u" Samara time"
            if (pl==1):
                im = cv2.imread("test.jpg")
                im = cv2.resize(im, (1000, 500))
                font = cv2.FONT_HERSHEY_PLAIN
                color = (0, 0, 255)
                cv2.putText(im, text=text, fontFace=font, org=(150, 150), fontScale=3, color=color, thickness=3)
                is_success, im_buf_arr = cv2.imencode(".jpg", im)
                f = BytesIO(im_buf_arr)
                byte_im = f.getvalue()
                #print(byte_im)
                #im.save(f, 'JPEG')
                try:
                    cv2.imwrite("d:\\PYTHON\\Magistracy\\2 семестр\\ПРЗП\\Lab3\\temp\\temp.jpg", im)

                except:

                    print("Unexpected error:", sys.exc_info()[0])
                    pass
            else:
                dr.rectangle((0,0,300,500),fill="#FFFFFF")
                dr.text((10, 5), text, font=font, fill="#000000")
                f = BytesIO()
                im.save(f,'JPEG')
                try :
                  im.save("d:\\PYTHON\\Magistracy\\2 семестр\\ПРЗП\\Lab3\\temp\\temp.jpg")

                except :

                    print("Unexpected error:", sys.exc_info()[0])
                    pass
          #  shutil.copy("d:/python/temp2.png","d:/python/temp.png")
            f.seek(0)

            time.sleep(1)

            yield  f.read()  #Camera.imgs[int(time.time()) % 3]