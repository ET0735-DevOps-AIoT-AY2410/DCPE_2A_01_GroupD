from dotenv import load_dotenv
load_dotenv()
from mongoApi import MongoDB
from datetime import date, datetime, timedelta
from time import sleep
from hal import hal_dc_motor as PiMotor
from hal import hal_led as PiLed
from hal import hal_lcd as PiLcd 
import RPi.GPIO as GPIO

booksDB = MongoDB('books')
usersDB = MongoDB('users')
currentDate = datetime.now()

# FOR PI: SCAN CARD-> HANDLE LOAN -> BORROW BOOK -> DISPENSE BOOK

def handlePayment(userId):
    # TO BE COMPLETED
    pass

        # There should only be one user at this point

            # User has payment due

            # FUNCTION TO DEAL WITH RFID READER HERE


            # User can proceed to borrow book


def borrow_book_from_db(userId):
    my_lcd.lcd_clear()
    user = usersDB.getItems(filter={"userId": userId}) #get user
    user = user[0]
    if "reservedBooks" in user and user["reservedBooks"]: #checks if user has any books reserved
        reserved_book_id = user["reservedBooks"][0]
        print(f"Dispensing book with ID: {reserved_book_id}")
        my_lcd.lcd_display_string("Dispensing Book with ID: {reserved_book_id}", 1) #display on lcd
        set_motor_speed(100)  # set motor to dispense book
        set_led_output(GPIO.HIGH) #turn led on
        sleep(5)
        set_motor_speed(0)  # to stop the dispensing motor
        set_led_output(GPIO.LOW)  #turn led off
        my_lcd.lcd_display_string("Dispensing complete", 2) #display on lcd
        
        booksDB.updateItem({"_id": reserved_book_id}, {"status": "borrowed"})  # Update book status
        usersDB.updateItem({"_id": userId}, {"reservedBooks": user['reservedBooks']})
       
        usersDB.appendItem({"_id": userId}, {"borrowedBooks": reserved_book_id}) # Add book to user borrowedBooks
    else:
        my_lcd.lcd_display_string("No reservations", 1) #display on lcd if no book reservations
       

def process_bar_code(image):
    pass
    # If not detected then print the message 


            # Print the barcode data 

                # print(barcode.type)

                # Should never enter here

        
    
def main():
    # While true
    # Loop camera
    # If camera detects card, check loans (pay loans via RFID, or timeout and restart) -> dispense books -> updateDB
    pass

def init():
    # Init LCD
    global my_lcd
    my_lcd = PiLcd.lcd()
    # Display 
    # "Welcome to SP library"
    # "Please scan card to proceed"

    # Init Camera
    pass

if __name__ == "__main__":
    print("""

    -PROGRAM START-


    """)
    # booksDB.listItems()
    # usersDB.listItems()
    
    print("""

    -STUFF HAPPENS-


    """)

    # process_bar_code("barcode01.png")
    init()
    # main()
    # borrow_book_from_db("P2302223")
    # testDb = MongoDB()
    # testDb.updateItem(search={"_id": { "$oid": "663a60797c645edcd6132b1a" }}, doc={"text":"GOODBYE WORLD"})
