from mongoApi import MongoDB
from datetime import date, datetime, timedelta

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
    # Find user by id
    pass

        # Found book reserved

        # DISPENSE THREAD HERE


        # Update book status
       
        # Add book to user borrowedBooks
       

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