import os
from time import sleep
from PIL import Image, ImageFile
from pyzbar.pyzbar import decode as decodeImage
from pyzbar.pyzbar import ZBarSymbol
import cv2
import requests
from time import sleep
# from picamera import PiCamera

def capture_image(file_path):
    with PiCamera() as camera:
        camera.resolution = (1440, 1080)
        camera.start_preview()
        sleep(1)  # Allow the camera to adjust to lighting
        camera.capture(file_path)
        camera.stop_preview()


def read_barcode(file_path):
    path = r'{}'.format(file_path)
    # path = r'C:\Users\leroy\OneDrive\Documents\!School_DevOps\DCPE_2A_01_GroupD\src\images\TestBarcode.jpg'
    im = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    ret, bw_im = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY)
    # cv2.imshow("image",bw_im)
    barcodes = decodeImage(bw_im, symbols=[ZBarSymbol.CODE128])

    if not barcodes: # Guard when no barcodes found
        return False

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f' {barcode_data}')

    return barcode_data

def writeToTxt(data):
    txt_path = os.path.join(os.path.dirname(__file__), 'images\data.txt')
    f = open(txt_path, "w")
    if not data:
        f.write("")
    else:
        f.write(data)


def main():
    image_path = os.path.join(os.path.dirname(__file__), 'images\TestBarcode.jpg')
    while True:
        capture_image(image_path)
        data = read_barcode(image_path)
        writeToTxt(data)

if __name__ == "__main__":
    main()
