# Library Book Reservation and Collection System
![Icon](https://github.com/Leroy-Hong/SP_DevOps_MiniProject_GroupD_Frontend/blob/master/assets/images/App%20Icon.png?raw=true)

This project was developed as part of ET0735 DevOps for AIoT's Mini Project
DCPE-2A-01-GroupD-AY24/25

# Overview
The project was created given the context: 
> To encourage and increase the number of people reading and loaning
> books from the public libraries, an automated book loan and return
> system is proposed.

As such, we have developed a robust system that will make use of a **Frontend** to allow users to make reservations for books in a database, as well as a **Raspberry Pi** handle the collection of books. The 2 systems are linked via an online database known as MongoDB. 

# Features
The following features can be broken down into the Frontend as well as the Raspberry Pi.
## Frontend:
 - An account system that consists of a Login page and a Registration page. Passwords are stored with simple client-side encryption due to the lack of a backend.
 - A page that displays **Your Books**- books currently in your possession or books that are reserved by you. You can choose to extend your loan from here, or cancel reservations.
 - A page that allows you to look at all available books registered in the entire library system. You can choose to make reservations from here.
 - A simple logout page.
 - Integration with MongoDB via API calls that sync the frontend with the library data.
## Raspberry Pi:
- A LCD display that shows instructions
- A message queue system implemented for the LCD display, such all messages have ample time to be read and are not dependent on the speed of the other processes
- A Picamera that is able to detect and scan barcodes for collection of books
- A RFID reader that is able to allow for collection of books, as well as settling loans
- A loan calculation system that calculates the loan upon returning of a book
- A timeout system that prevents the machine from being stuck during a payment operation
- A Servo motor to dispense the books
- A LED as an indicator of the dispensing of books
- A daemon that unreserves books that have been reserved for more than 5 days without collection
- Integration with MongoDB via API calls that sync the Raspberry Pi with the library data.

## Other details
- The front end was developed using react-native. However, due to CORS error, is unable to run on the web browser.
- The repo includes `mongoDBControl.py` which is used for administrative control such as resetting the database
- The Raspberry Pi system will not run without the proper API key for MongoDB. The API key is read by the program via `.env` files but is not included in the repository.
- Find the Frontend here:

[![Leroy-Hong/SP_DevOps_MiniProject_GroupD_Frontend - GitHub](https://gh-card.dev/repos/Leroy-Hong/SP_DevOps_MiniProject_GroupD_Frontend.svg)](https://github.com/Leroy-Hong/SP_DevOps_MiniProject_GroupD_Frontend)
# Execution
The following is how to use the project:
## Using Docker to run main.py
1. cd into the src folder
```bash
cd src
```
2. Build the image
```bash
docker build -t myapp . .
```
3. Run the container
```bash
docker run --privileged -v HOST_DIRECTORY:/app/images/ -e APIKEY='YOURKEY' myapp
```
4. Run cameraExtension.py to make use of the barcode scanning feature
```bash
python -u cameraExtension.py
```
