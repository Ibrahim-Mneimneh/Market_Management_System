import configparser

import eel
import mysql.connector
import hashlib


@eel.expose
def signup(sqlpassword, firstname, lastname, email, username, phonenumber, password):
    config = configparser.ConfigParser()
    config.read('../config.cfg')

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

    if not len(password) >= 8:
        return "Password must be at least 8 characters long."
    elif not any(char.isdigit() for char in password):
        return "Password must contain at least 1 digit."
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
        print(cursor.rowcount, "rows were added to the database!")
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
        print(cursor.rowcount, "rows were added to the database!")
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")
        return "Username or email may be already in use."
    return"Signed up Successfully"


@eel.expose
def login(sqlPassword, username_email, password):
    try:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password=sqlPassword,
            port=3306,
            database="mms")
    except mysql.connector.Error as error:
        print("Database Connection Failed!")
        quit()
        mydb.close()

    if ".com" in username_email:
        try:
            query = "SELECT username from Account where email=\"" + username_email + "\""
            cursor = mydb.cursor()
            cursor.execute(query)
            empUsername = cursor.fetchall()
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")
            return "Username/Email doesn't exist please make sure to sign up."
        try:
            query = "SELECT password from Account where email=\"" + username_email + "\""
            cursor = mydb.cursor()
            cursor.execute(query)
            dbpass = cursor.fetchall()
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")
            return "Incorrect username/email or password"
        if str(dbpass[0][0]) == hashlib.sha256(password.encode()).hexdigest():
            return "Logging In."
        else:
            return "Incorrect username/email or password"
    else:
        try:
            query = "SELECT username from Account where username=\"" + username_email + "\""
            cursor = mydb.cursor()
            cursor.execute(query)
            empUsername = cursor.fetchall()
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")
            return "Username/Email doesn't exist please make sure to sign up."
        try:
            query = "SELECT password from Account where username=\"" + username_email + "\""
            cursor = mydb.cursor()
            cursor.execute(query)
            dbpass = cursor.fetchall()
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")
            return "Incorrect username/email or password"
        if str(dbpass[0][0]) == hashlib.sha256(password.encode()).hexdigest():
            return "Logging In."
        else:
            return "Incorrect username/email or password"


@eel.expose
def routing(newpage):
    eel.show(newpage)


page = "menu.html"

eel.init("Menu")
eel.start(page)
