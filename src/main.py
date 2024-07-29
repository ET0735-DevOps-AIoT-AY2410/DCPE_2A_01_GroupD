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
def dispenseBook(book):
    my_lcd.lcd_display_string("Dispensing Book with ID: {reserved_book_id}", 1) #display on lcd
    PiMotor.set_motor_speed(100)  # set motor to dispense book
    PiLed.set_output(24,1) #turn led on
    sleep(1)
    PiMotor.set_motor_speed(0)  # to stop the dispensing motor
    PiLed.set_output(24,0)  #turn led off
    my_lcd.lcd_display_string("Dispensing complete", 2) #display on lcd

def handlePayment(userId):
    # TO BE COMPLETED
    pass

        # There should only be one user at this point

            # User has payment due

            # FUNCTION TO DEAL WITH RFID READER HERE

            # User can proceed to borrow book


def borrow_book_from_db(userId):
    my_lcd.lcd_clear()
    bookCriteria = {"status.reserved":userId}
    books = booksDB.getItems(filter=bookCriteria)
    if len(books) > 0:
        for book in books:
            print(f"Dispensing book with name: {book['name']}")
            dispenseBook(book)
            
            booksDB.updateItem(search={'id':book['id']},
                            doc={'status':{}})  # Update book status
        
            usersDB.appendItem(search={'studentId':userId}, doc={'borrowedBooks':{
                book['id']: (currentDate + timedelta(days=18)).strftime("%d/%m/%Y"),
            }}) # Add book to user borrowedBooks
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

    # Init LED
    PiLed.init()

    # Init Motor
    PiMotor.init()

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
    borrow_book_from_db("P2302223")
    # usersDB.appendItem(search={'studentId':"P2302223"}, doc={'borrowedBooks':{
    #             4: (currentDate + timedelta(days=18)).strftime("%d/%m/%Y"),
    #         }})
    # testDb = MongoDB()
    # testDb.updateItem(search={"_id": { "$oid": "663a60797c645edcd6132b1a" }}, doc={"text":"GOODBYE WORLD"})
