import pytest
from threading import Thread
import os
from time import sleep
from main import authBarcodeProcess, barcodeListener, calculateLoan
from datetime import datetime

# This function can never fail
def test_authBarcodeProcess():
    # Setup
    expected = "12345678"
    txt_path = os.path.join(os.path.dirname(__file__), '..\images\data.txt')
    with open(txt_path,"w") as f1: # Clear text file
        f1.write("<8Len")

    def writeFile():
        sleep(2)
        with open(txt_path,"w") as f1:
            f1.write(expected)

    writeThread = Thread(target=writeFile)

    # Test
    writeThread.run()
    userId = authBarcodeProcess()
    
    # Assert
    assert (userId == expected)


def test_barcodeListener():
    # Setup
    expected = "I exist"
    txt_path = os.path.join(os.path.dirname(__file__), '..\images\data.txt')
    with open(txt_path,"w") as f1: # Clear text file
        f1.write("")

    def writeFile():
        sleep(2)
        with open(txt_path,"w") as f1:
            f1.write(expected)

    writeThread = Thread(target=writeFile)

    # Test
    writeThread.run()
    userId = barcodeListener()
    
    # Assert
    assert (userId == expected)
    

def test_calculateLoan():
    # Setup
    targetDue = "01/01/01"
    loanDays = (datetime.now() - datetime.strptime(targetDue, "%d/%m/%y")).days
    expected = loanDays * 0.15

    # Test
    actualLoan = calculateLoan({"1":targetDue})

    # Assert
    assert (actualLoan == expected)

    