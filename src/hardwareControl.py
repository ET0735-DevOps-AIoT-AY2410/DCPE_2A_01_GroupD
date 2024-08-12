from hal import hal_dc_motor as PiMotor
from hal import hal_led as PiLed
from hal import hal_lcd as PiLcd
from hal import hal_rfid_reader as PiReader
from better_buzzer import customBuzzer as PiBuzzer
import json

# Init LCD
global my_lcd
my_lcd = PiLcd.lcd()

# Init LED
PiLed.init()

# Init Motor
PiMotor.init()

# Init RFID Reader
global my_reader
my_reader = PiReader.init()

# Init Buzzer
global my_buzzer
my_buzzer = PiBuzzer(20)

def ADMIN_setup_card():
    x = {
        "userId": "P2302223",
        "cash": 30,
        }
    y = json.dumps(x)
    my_reader.write(y)


def ADMIN_read_card():
    data = my_reader.read()
    print(data)