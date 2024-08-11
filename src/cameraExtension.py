import os
from time import sleep
from pyzbar.pyzbar import decode as decodeImage
from pyzbar.pyzbar import ZBarSymbol
import cv2 as cv
from time import sleep
from picamera import PiCamera

def capture_image(file_path):
    with PiCamera() as camera:
        camera.resolution = (2592, 1944)
        camera.start_preview()
        sleep(1)  # Allow the camera to adjust to lighting
        camera.capture(file_path)
        camera.stop_preview()


def read_barcode(file_path):
    path = r'{}'.format(file_path)
    bwPath = r'{}'.format(os.path.join(os.path.dirname(__file__), 'images/bw.jpg'))
    im = cv.imread(path, cv.IMREAD_GRAYSCALE)
    cv.imwrite(bwPath, im)
    barcodes = decodeImage(im, symbols=[ZBarSymbol.CODE128, ZBarSymbol.CODE39])

    if not barcodes: # Guard when no barcodes found
        return False

    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f' {barcode_data}')

    return barcode_data

def writeToTxt(data):
    txt_path = os.path.join(os.path.dirname(__file__), 'images/data.txt')
    f = open(txt_path, "w")
    if not data:
        f.write("")
    else:
        f.write(data)


def main():
    image_path = os.path.join(os.path.dirname(__file__), 'images/TestBarcode.jpg')
    while True:
        capture_image(image_path)
        data = read_barcode(image_path)
        writeToTxt(data)

if __name__ == "__main__":
    main()
