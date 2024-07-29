from dotenv import load_dotenv
load_dotenv()
import json
from mongoApi import MongoDB
from datetime import date, datetime, timedelta
from time import sleep, time
from hal import hal_dc_motor as PiMotor
from hal import hal_led as PiLed
from hal import hal_lcd as PiLcd
from hal import hal_rfid_reader as PiReader
import RPi.GPIO as GPIO
from threading import Thread

booksDB = MongoDB('books')
usersDB = MongoDB('users')
currentDate = datetime.now()

# FOR PI: SCAN CARD-> HANDLE LOAN -> BORROW BOOK -> DISPENSE BOOK
def dispenseBook(bookId):
    my_lcd.lcd_display_string(f"Book ID: {bookId}", 1) #display on lcd
    PiMotor.set_motor_speed(100)  # set motor to dispense book
    PiLed.set_output(24,1) #turn led on
    sleep(1)
    PiMotor.set_motor_speed(0)  # to stop the dispensing motor
    PiLed.set_output(24,0)  #turn led off
    my_lcd.lcd_display_string("Completed!", 2) #display on lcd
    sleep(5)
    my_lcd.lcd_clear()

# handlePayment returns True when user does not have a loan
def handlePayment(userId) -> bool:
    my_lcd.lcd_clear()

    # Retrieve user information from the database based on userId
    users = usersDB.getItems(filter={"studentId": userId})
    user = users[0]

    # Check if the user has a loan and reserved books
    if not user.get('loan'):
        return True
    

    my_lcd.lcd_display_string("Settle loans", 1)
    my_lcd.lcd_display_string("Tap RFID card", 2)

    # Start the timer
    start_time = time()

    # Continuously read RFID until a valid ID is detected or timeout occurs
    while True:
        current_time = time()
        elapsed_time = current_time - start_time

        # Check if timeout (30 seconds) has been reached
        if elapsed_time >= 30:
            my_lcd.lcd_clear()
            my_lcd.lcd_display_string("Timeout. Please try again.", 1)
            break # need to reset the whole system after this break

        id, data = my_reader.read_no_block()

        # Guard incorrect data
        if not data:
            # If data exists
            continue
        elif "Error" in data:
            # If error detected in read
            print("Error detected")
            continue
        elif data.find("{") == -1 or data.find("}") == -1:
            # If card is not json object
            continue

        data = data[data.find("{"):data.find("}")+1]
        dataDict = json.loads(data) # Load data as json object


        # Assume keypair is of correct type
        if float(dataDict.get('cash')) < float(user.get('loan')):
            # Insufficient funds
            my_lcd.lcd_clear()
            my_lcd.lcd_display_string("Low funds,", 1)
            my_lcd.lcd_display_string("Please try again", 2)
            sleep(2)
            my_lcd.lcd_clear()
            my_lcd.lcd_display_string("Settle loans,", 1)
            my_lcd.lcd_display_string("Tap RFID card", 2)
            continue
        else:

            # Subtract from RFID
            my_lcd.lcd_clear()
            my_lcd.lcd_display_string("Thank you!", 1)
            my_lcd.lcd_display_string("Payment done!", 2)
            
            # Update the user's loan to 0 in the database
            # usersDB.updateItem({"_id": userId}, {"$set": {"loan": 0}})
            break  # Exit the loop after successful payment
        



def borrow_book_from_db(userId):
    my_lcd.lcd_clear()
    bookCriteria = {"status.reserved":userId}
    books = booksDB.getItems(filter=bookCriteria)
    if len(books) > 0:
        for book in books:
            print(f"Dispensing book with name: {book['name']}")

            dispenseThread = Thread(target= dispenseBook, args=(book['id']))
            dispenseThread.start()
            
            # booksDB.updateItem(search={'id':book['id']},
            #                 doc={'status':{}})  # Update book status
        
            # usersDB.appendItem(search={'studentId':userId}, doc={'borrowedBooks':{
            #     book['id']: (currentDate + timedelta(days=18)).strftime("%d/%m/%Y"),
            # }}) # Add book to user borrowedBooks
    else:
        my_lcd.lcd_display_string("No reservations", 1) #display on lcd if no book reservations
       

def process_bar_code(image):
    pass
    # If not detected then print the message 


            # Print the barcode data 

                # print(barcode.type)

                # Should never enter here

def ADMIN_setup_card():
    x = {
        "userId": "P2302223",
        "cash": 30,
        }
    y = json.dumps(x)
    my_reader.write(y)
    
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

    # Init RFID Reader
    global my_reader
    my_reader = PiReader.init()

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
    handlePayment("P2302223")
    # main()
    # borrow_book_from_db("P2302223")
    # usersDB.appendItem(search={'studentId':"P2302223"}, doc={'borrowedBooks':{
    #             4: (currentDate + timedelta(days=18)).strftime("%d/%m/%Y"),
    #         }})
    # testDb = MongoDB()
    # testDb.updateItem(search={"_id": { "$oid": "663a60797c645edcd6132b1a" }}, doc={"text":"GOODBYE WORLD"})
