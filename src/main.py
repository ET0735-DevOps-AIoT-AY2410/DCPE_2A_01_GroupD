from dotenv import load_dotenv
load_dotenv()
import json
from mongoApi import MongoDB
from datetime import datetime, timedelta
from time import sleep, time
import os

try:
    from hal import hal_dc_motor as PiMotor
    from hal import hal_led as PiLed
    from hal import hal_lcd as PiLcd
    from hal import hal_rfid_reader as PiReader
    from better_buzzer import customBuzzer as PiBuzzer
except:
    pass

from threading import Thread
from queue import Queue

booksDB = MongoDB('books2')
usersDB = MongoDB('users')
currentDate = datetime.now()
lcdMessageQueue = Queue()

# FOR PI: SCAN CARD-> HANDLE LOAN -> BORROW BOOK -> DISPENSE BOOK
def defaultRFIDMessage():
    lcdMessageQueue.put((0,"Tap RFID", "w Student Card", "clr"))


def defaultBarcodeMessage():
    lcdMessageQueue.put((0,"Scan Barcode", "w The Camera", "clr"))


def dispenseBook(bookId):
    lcdMessageQueue.put((0,f"Book ID: {bookId}","","clr"))
    PiMotor.set_motor_speed(100)  # type: ignore # set motor to dispense book
    PiLed.set_output(24,1) # type: ignore #turn led on
    sleep(1)
    PiMotor.set_motor_speed(0)  # type: ignore # to stop the dispensing motor
    PiLed.set_output(24,0)  # type: ignore #turn led off

    lcdMessageQueue.put((2,"","Dispensed!",""))


# deductFromCard returns False when an error occurs
def deductFromCard(cardBal: float, loanDue: float, dataDict: dict):
    
    # Determine new balance of card
    newBal = ('%f' % (cardBal - loanDue)).rstrip('0').rstrip('.') # Weird trick to format float
    dataDict['cash'] = newBal
    writeData = json.dumps(dataDict) # Prepare data to be written

    # Try about 100 times
    for _ in range(100):
        foundFlag = False
        id, data = my_reader.read_no_block()

        # Guards invalid data (or no data)
        if not data:
            # If data does not exist
            continue
        elif "Error" in data:
            # If error detected in read
            print("Error detected")
            continue
        else:
            foundFlag = True
            break

    if not foundFlag:
        return False
    
    # Card should still be on the reader at this point
    try:
        my_reader.write(writeData)
    except IndexError:
        return False
    else:
        return True
    

def MongoDB_Worker(): # The worker that controls some of the database
    # Cancel reserved books after 5 days if not collected
    while True:
        users = usersDB.getItems(filter={f"reservedBooks": {"$exists": "true"}})
        for user in users:
            reservedBooks = user.get('reservedBooks')
            # Reserved books is an object
            for bookId, dateString in reservedBooks.items():
                dueDate = datetime.strptime(dateString, "%d/%m/%y") # Parse duedate into time format
                if currentDate > dueDate:
                    print(f"Book {bookId} is being unreserved from {user.get('studentId')}")
                    # Unreserve the book
                    booksDB.unsetItem(search={'id':bookId}, field="status.reserved")
                    usersDB.unsetItem(search={'studentId':user.get('studentId')}, field=f"reservedBooks.{bookId}")



        sleep(3600) # Runs check every hour

def LCD_Message_Worker(): # The worker that allows for buffering of LCD displayed data
    def LCDPrint(duration: float = 0, msg1: str = "", msg2: str = "", *args):
        if args:
            if args[0] == "clr":
                my_lcd.lcd_clear()
        my_lcd.lcd_display_string(msg1,1)
        my_lcd.lcd_display_string(msg2,2)
        sleep(duration)


    while True:
        # Get stuff 
        LCDPrint(*lcdMessageQueue.get())
        lcdMessageQueue.task_done()


# handlePayment returns True when user does not have a loan or 
# when payment is finished
def handlePaymentProcess(userId) -> bool:
    # Retrieve user information from the database based on userId
    users = usersDB.getItems(filter={"studentId": userId})
    user = users[0]

    # Check if the user has a loan and reserved books
    if not (loanDue := user.get('loan')):
        return True
    
    lcdMessageQueue.put((0,f"Loan: ${loanDue}","Tap RFID card","clr"))
    # Delay added so that you tap at 2 separate instances
    # Start the timer
    start_time = time()

    # Continuously read RFID until a valid ID is detected or timeout occurs
    while True:
        sleep(0.25)
        current_time = time()
        elapsed_time = current_time - start_time

        # Check if timeout (30 seconds) has been reached
        if elapsed_time >= 30:
            lcdMessageQueue.put((1,f"Timeout, please","try again","clr"))
            return False # need to reset the whole system after this break

        id, data = my_reader.read_no_block()

        # Guard incorrect data
        if not data: # If data exists
            continue
        elif "Error" in data: # If error detected in read
            print("Error detected in read")
            continue
        elif data.find("{") == -1 or data.find("}") == -1:
            # If card is not json object
            print("Cannot find {} in card")
            continue

        data = data[data.find("{"):data.find("}")+1]
        dataDict = json.loads(data) # Load data as json object


        # Assume keypair is of correct type
        if (cardBal := float(dataDict.get('cash'))) < float(loanDue):
            # Insufficient funds
            lcdMessageQueue.put((2,"Low funds,","Please try again","clr"))
            my_buzzer.playTone("E6",0.04)
            my_buzzer.playTone("B5",0.46)
            continue
        else:

            # Subtract from RFID
            status = deductFromCard(cardBal, loanDue, dataDict)
            if not status:
                print("Error: Could not deduct from card")
                continue
            
            # Clear user's loan from database
            usersDB.unsetItem({"studentId": userId}, "loan")
            lcdMessageQueue.put((2,"Thank you!","Payment done!","clr"))
            break  # Exit the loop after successful payment
    return True
        

def borrow_book_from_db(userId):
    my_lcd.lcd_clear()
    bookCriteria = {"status.reserved":userId}
    books = booksDB.getItems(filter=bookCriteria)
    if len(books) > 0:
        for book in books:
            print(f"Dispensing book with name: {book['name']}")

            dispenseThread = Thread(target= dispenseBook, args=(book['id']))
            dispenseThread.start()
            
            my_buzzer.playTone("B5",0.04)
            my_buzzer.playTone("E6",0.46)

            booksDB.unsetItem(search={'id':book.get("id")},field="status.reserved")
            booksDB.setItem(search={'id':book.get("id")},doc={"status.owner":userId})
            usersDB.setItem(search={'studentId':userId}, doc={f"borrowedBooks.{book.get('id')}":
                                                              (currentDate + timedelta(days=18)).strftime("%d/%m/%y")})
    else:
        lcdMessageQueue.put((1,"Found 0","Reservations!","clr")) #display on lcd if no book reservations


# authUserProcess gets the userId of the collector via RFID and returns its value
# This function is the start of the entire process       
def authRFIDProcess() -> str:
    # Instructions for user
    defaultRFIDMessage()
    data = None
    # Check for userId
    while True: 
        while not data:
            id, data = my_reader.read() # Wait for data

        # Guard incorrect data
        if "Error" in data: # If error detected in read
            print("Error detected in read")
            continue
        elif data.find("{") == -1 or data.find("}") == -1:
            # If card is not json object
            print("Cannot find \{\} in card")
            continue

        data = data[data.find("{"):data.find("}")+1]
        dataDict = json.loads(data) # Load data as json object

        # If the data contains a value for userId
        if userId := dataDict.get('userId'):
            break # Break the loop to proceed
    
    # Information to user
    lcdMessageQueue.put((2,"Registered as",f"{userId}","clr"))
    # Pause for a short while
    return userId # Return the value of userId to be used


def barcodeListener() -> str:
    txt_path = os.path.join(os.path.dirname(__file__), 'images/data.txt')
    while True:
        with open(txt_path, "r+") as f1:
            data = f1.read()
            if data:
                f1.seek(0)
                f1.truncate()
                return data


def authBarcodeProcess() -> str:
    defaultBarcodeMessage()
    while True:
        # Read in data.txt
        data = barcodeListener()
        if len(data[3:]) == 7:
            # For some reason, by admin card shows 2002302746
            data = "P" + data[3:]
        if len(data) != 8: # Guard data by length
            continue
        # Information to user
        lcdMessageQueue.put((2,"Registered as",f"{data}","clr"))
        # Pause for a short while
        return data
                

def ADMIN_setup_card():
    x = {
        "userId": "P2302223",
        "cash": 30,
        }
    y = json.dumps(x)
    my_reader.write(y)


def calculateLoan(books:dict) -> float:
    # Expects books to be in the example format:
    # {"1":"01/01/01"}
    totalLoan = 0
    for date in books.values():
        # Get the date
        dueDate = datetime.strptime(date, "%d/%m/%y")
        loanDays = (currentDate - dueDate).days
        if loanDays > 0:
            # Payment to be made
            loan = loanDays * 0.15
            print(f"You have accumulated a loan of ${loan}")
            # Calculate loan
            totalLoan += loan
    
    return round(totalLoan,2)


def ADMIN_returnUserBooks(userId: str):
    # From userId, retrieve borrowed books
    totalLoan = 0
    users = usersDB.getItems(filter={"studentId": userId})
    for user in users:
        # Expect only one user
        borrowedBooks = user.get("borrowedBooks")
        totalLoan = calculateLoan(borrowedBooks)
        print(totalLoan)
        # Update loan on database
        if currentLoan := user.get("loan"):
            totalLoan += float(currentLoan)

        usersDB.setItem(search={"studentId": userId},doc={"loan":totalLoan})
        
        for bookId in borrowedBooks.keys():
            # Removes owner status from book
            booksDB.unsetItem(search={"id":bookId},field="status.owner")
            # Removes loanExtension from book
            booksDB.unsetItem(search={"id":bookId},field="status.loanExtended")
            # Removes book from user inventory
            usersDB.unsetItem(search={ "$and": [ {"studentId": userId, f"borrowedBooks.{bookId}": {"$exists": "true"}}]}, 
                              field=f"borrowedBooks.{bookId}")


def ADMIN_returnBook(bookId: str):
    bookId = str(bookId)
    # Get user object by the borrowedBook ID
    users = usersDB.getItems(filter={f"borrowedBooks.{bookId}": {"$exists": "true"}})
    for user in users:
        # Expect only one user
        date = user.get("borrowedBooks").pop(bookId)
        totalLoan = calculateLoan({bookId:date})
        print(totalLoan)
        # Update loan on database
        if currentLoan := user.get("loan"):
            totalLoan += float(currentLoan)
        
        usersDB.setItem(search={f"borrowedBooks.{bookId}": {"$exists": "true"}}, doc={"loan":totalLoan})

        # Removes owner status from book
        booksDB.unsetItem(search={"id":bookId},field="status.owner")
        # Removes loanExtension from book
        booksDB.unsetItem(search={"id":bookId},field="status.loanExtended")
        # Removes book from user inventory
        usersDB.unsetItem(search={f"borrowedBooks.{bookId}": {"$exists": "true"}}, field=f"borrowedBooks.{bookId}")


def main():
    global currentDate
    # While true
    while True:
        currentDate = datetime.now()
        userId = authBarcodeProcess()
        my_buzzer.playTone("C4")
        sleep(2)
        status = handlePaymentProcess(userId)
        if status:
            # Payment has been made
            borrow_book_from_db(userId)
            sleep(2)
        else:
            # Payment was not made
            continue # Start from beginning
    # If camera detects card, check loans (pay loans via RFID, or timeout and restart) -> dispense books -> updateDB


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

    # Init Buzzer
    global my_buzzer
    my_buzzer = PiBuzzer(20)

    # Display 
    my_lcd.lcd_clear()
    my_lcd.lcd_display_string("Initialising", 1)
    my_lcd.lcd_display_string("...", 2)

    # Start LCD_Message_Worker
    Thread(target=LCD_Message_Worker, daemon=True).start()
    Thread(target=MongoDB_Worker, daemon=True).start()

    # Init Camera
    pass


if __name__ == "__main__":
    print("""

    -INITIALISING-

    """)

    init()
    
    print( """

    -CALLING MAIN-

    """)

    main()