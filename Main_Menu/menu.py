import eel
import os
import mysql.connector
import hashlib


@eel.expose
def login():
    os.system("py login.py")


@eel.expose
def signup(sqlpassword, firstname, lastname, email, username, phoneNumber, password):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=sqlpassword,
            port=3306,
            database="mms")
    except mysql.connector.Error as error:
        print("Database Connection Failed!")
        quit()
        mydb.close()

    if not len(password) >= 8:
        print("Password must be at least 8 characters long.")
    elif not any(char.isdigit() for char in password):
        print("Password must contain at least 1 digit.")
    elif not any(char.isupper() for char in password):
        print("Password must contain at least 1 uppercase character.")
    encrypted_password = hashlib.sha256(password.encode()).hexdigest()

    # Add an Employee
    try:
        query = "INSERT INTO Employee (Firstname, Lastname, Salary, PhoneNumber)" \
                "VALUES (\"" + firstname + "\", \"" + lastname + "\", 500, \"" + phoneNumber + "\");"
        cursor = mydb.cursor()
        cursor.execute(query)
        mydb.commit()
        print(cursor.rowcount, "rows were added to the database!")
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")

    # add an account for the employee
    try:
        query = "INSERT INTO Account VALUES (\"" + username + "\", \"" + encrypted_password + "\", \"" + \
                email + "\", False, " + "(select EmpId from Employee where PhoneNumber = \"" + phoneNumber + "\"));"
        cursor = mydb.cursor()
        cursor.execute(query)
        mydb.commit()
        print(cursor.rowcount, "rows were added to the database!")
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")
    print("Signed up Successfully")


@eel.expose
def routing(newpage):
    eel.show(newpage)


page = "menu.html"

eel.init("Menu")
eel.start(page)
