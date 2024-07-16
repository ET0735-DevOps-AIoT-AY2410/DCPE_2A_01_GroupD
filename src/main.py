from mongoApi import MongoDB
from datetime import date, datetime, timedelta
from hal import hal_rfid_reader as rfid_reader
from hal import hal_led as led
from hal import hal_lcd as LCD

booksDB = MongoDB('books')
usersDB = MongoDB('users')
currentDate = datetime.now()

# FOR PI: SCAN CARD-> HANDLE LOAN -> BORROW BOOK -> DISPENSE BOOK

def handlePayment(userId):
    my_lcd = LCD.lcd()
    led.init()
    my_lcd.lcd_clear()
    reader = rfid_reader.init()

    # Retrieve user information from the database based on userId
    user = usersDB.getItems(filter={"userId": userId})
    user = user[0]

    # Check if the user has a loan and reserved books
    if "loan" in user and user["loan"] != 0 and "reservedBooks" in user and user["reservedBooks"]:
        my_lcd.lcd_display_string("You need to pay your loan", 1)
        my_lcd.lcd_display_string("Tap RFID card", 2)

        # Continuously read RFID until a valid ID is detected
        while True:
            id = reader.read_id_no_block()
            id = str(id)

            if id != "None":
                my_lcd.lcd_clear()
                my_lcd.lcd_display_string("Thank you for the payment", 1)
                
                # Update the user's loan to 0 in the database
                usersDB.updateItem({"_id": userId}, {"$set": {"loan": 0}})
                break  # Exit the loop after successful payment
        


def borrow_book_from_db(userId):
    # Find user by id
    pass

       

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
    # Display 
    # "Welcome to SP library"
    # "Please scan card to proceed"

    # Init Camera
    pass

if __name__ == "__main__":
    print("""

    -PROGRAM START-


    """)
    booksDB.listItems()
    usersDB.listItems()
    
    print("""

    -STUFF HAPPENS-


    """)

    process_bar_code("barcode01.png")
    # init()
    # main()
    # borrow_book_from_db("P2302223")
    # testDb = MongoDB()
    # testDb.updateItem(search={"_id": { "$oid": "663a60797c645edcd6132b1a" }}, doc={"text":"GOODBYE WORLD"})