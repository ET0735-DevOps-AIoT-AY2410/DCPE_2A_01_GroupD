from dotenv import load_dotenv
load_dotenv()
from mongoApi import MongoDB
from datetime import date, datetime, timedelta

booksDB = MongoDB('books2')
usersDB = MongoDB('users')

# Reset Loans, User inventory and Book statuses
def softResetDB():
    booksDB.setItems(search={},doc={"status":{}})
    usersDB.setItems(search={},doc={"borrowedBooks":{}})
    usersDB.setItems(search={},doc={"reservedBooks":{}})
    usersDB.unsetItems(search={},field="loan")

def calculateLoan(books:dict) -> float:
    currentDate = datetime.now()
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
# Example user:
"""
_id: ObjectId
studentId : String
password : String
name : String
loan? : Double
borrowedBooks : {
    bookId?: String("DD/MM/YY")
    ...
}
reservedBooks : {
    bookId?: String("DD?MM/YY")
}
"""
# Example book:
"""
_id: ObjectId
id: String
name: String
category: String
library: String
status: {
    owner?: String(userId)
    reserved?: String(userId)
    loanExtended?: String(userId)
}
"""

ADMIN_returnBook("4")