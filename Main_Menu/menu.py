import configparser
import os
import subprocess
import eel
import mysql.connector
import hashlib
from win32api import GetSystemMetrics
from datetime import date

file_path = "../config.cfg"
prop=""
if not os.path.exists(file_path):
    subprocess.run(['python', '../SQL/getSQLpassword.py'])

config = configparser.ConfigParser()
config.read(file_path)
try:
    mydb = mysql.connector.connect(
        host=config.get('mysql', 'host'),
        user=config.get('mysql', 'user'),
        password=config.get('mysql', 'password'),
        port=3306,
        database=config.get('mysql', 'database')
    )
except mysql.connector.Error as error:
    print("Database Connection Failed!")
    quit()
    mydb.close()

# todo get profit from manager gui (expenses, total salaries) and matplotlib
# todo manager request items from suppliers
# todo order function

@eel.expose
def signup(firstname, lastname, email, username, phonenumber, password):
    if not (firstname and lastname and email and username and phonenumber and password):
        return "Please fill all the fields."

    if not len(username.split()) == 1:
        return "Username cannot have spaces."

    if not ('@' in email and '.' in email.split('@')[1]):
        return "Enter the email correctly."

    mycursor = mydb.cursor()
    mycursor.execute("SELECT EXISTS(SELECT * FROM Account WHERE username = %s)", (username,))
    result = mycursor.fetchone()[0]

    if result == 1:
        return "Username already exists."

    mycursor = mydb.cursor()
    mycursor.execute("SELECT EXISTS(SELECT * FROM Account WHERE email = %s)", (email,))
    result = mycursor.fetchone()[0]

    if result == 1:
        return "Email already exists."

    mycursor = mydb.cursor()
    mycursor.execute("SELECT EXISTS(SELECT * FROM Employee WHERE PhoneNumber = %s)", (phonenumber,))
    result = mycursor.fetchone()[0]

    if result == 1:
        return "Phone number already exists."

    if not len(password) >= 8:
        return "Password must be at least 8 characters long."
    elif not any(char.isdigit() for char in password):
        return "Password must contain at least 1 digit."
    elif not any(char.islower() for char in password):
        return "Password must contain at least 1 lowercase character."
    elif not any(char.isupper() for char in password):
        return "Password must contain at least 1 uppercase character."

    encrypted_password = hashlib.sha256(password.encode()).hexdigest()
    print(phonenumber)
    print(firstname)
    # Add an Employee
    try:
        query = "INSERT INTO Employee (Firstname, Lastname, Salary, PhoneNumber)" \
                "VALUES (\"" + firstname + "\", \"" + lastname + "\", 500, \"" + phonenumber + "\");"
        cursor = mydb.cursor()
        cursor.execute(query)
        mydb.commit()
        print("Employee "+firstname+" "+lastname+" was added.")
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")
        return "PhoneNumber is already in use"

    # add an account for the employee
    try:
        query = "INSERT INTO Account VALUES (\"" + username + "\", \"" + encrypted_password + "\", \"" + \
                email + "\", False, " + "(select EmpId from Employee where PhoneNumber = \"" + phonenumber + "\"));"
        cursor = mydb.cursor()
        cursor.execute(query)
        mydb.commit()
        print(username+" Account was created Successfully!")
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")
        return "Username or email may be already in use."
    return "Signed up Successfully"


@eel.expose
def login(username_email, password):
    mycursor = mydb.cursor()

    # Check if the email has "@"
    if '@' in username_email and '.' in username_email.split('@')[1]:
        # Check if the email is found in the Account table
        mycursor.execute("SELECT * FROM Account WHERE email = %s", (username_email,))
    else:
        # Check if the username is found in the Account table
        mycursor.execute("SELECT * FROM Account WHERE username = %s", (username_email,))

    account = mycursor.fetchone()
    # If the account exists
    if account:
        # Encrypt the password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        # Get the password from the Account table
        stored_password = account[1]

        # Check if the passwords match
        if hashed_password == stored_password:
            query = "Select firstname, lastname from Employee as e join Account as acc on e.empId=acc.empId where " \
                   "username=\""+account[0]+"\" "
            cursor = mydb.cursor()
            cursor.execute(query)
            fullname = cursor.fetchone()
            global prop
            prop = fullname[0]+" "+fullname[1]
            return "Logging In."
        else:
            return "Incorrect Username/Email or Password."
    else:
        return "Account doesn't exist, consider Signing Up?"


@eel.expose
def addOrder(qrCode, quantity, employeeReference):
    if len(qrCode) != len(quantity):
        return "Please select a quantity for each item"
    #check if all items are present
    for item, itemQuantity in zip(qrCode, quantity):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT EXISTS(SELECT qrcode FROM item WHERE qrcode = %s)", (item,))
        result = mycursor.fetchone()[0]
        if result != 1:
            return "The item '"+item+"' doesn't exist."
        mycursor = mydb.cursor()
        mycursor.execute("SELECT leftAmount FROM  WHERE qrcode = %s)", (item,))
        result = mycursor.fetchone()[0]
        if result < itemQuantity:
            return "Requested amount of '"+item+"' is not available. Available amount is "+result
    # Create the order
    currentDate = str(date.today())
    try:
        query = "Insert into order(date,price,isOnline) values(\"" + currentDate + "\"," + 1 + ",true)"
        cursor = mydb.cursor()
        cursor.execute(query)
        mydb.commit()
        print("New Order created Successfully!!")
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")

    # TO DO grab the order id to insert it on each Order-Item relation

    # Add the items into the order
    for item, itemQuantity in zip(qrCode, quantity):
        try:
            query = "Insert into Order_Item(OrderId,barCode,quantity) values(\"" +  + "\",\"" + item + "\",\""+quantity+"\")"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            print("New Order created Successfully!!")
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")







@eel.expose
def passProps():
    return prop


@eel.expose
def routing(newpage):
    eel.show(newpage)


@eel.expose
def getProps(props):
    global prop
    prop = props


page = "menu.html"

eel.init("Menu")
eel.start(page, size=(GetSystemMetrics(0), GetSystemMetrics(1)))
