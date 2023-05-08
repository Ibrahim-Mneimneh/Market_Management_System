import configparser
import os
import subprocess
import eel
import mysql.connector
import hashlib
from win32api import GetSystemMetrics
from datetime import date
from SQL.display import displayEntity

file_path = "../config.cfg"
prop = ""
if not os.path.exists(file_path):
    subprocess.run(['python', '../SQL/SQLprompt.py'])

config = configparser.ConfigParser()
config.read(file_path)
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        port=3306,
        database="mms"
    )
except mysql.connector.Error as error:
    print("Database Connection Failed!")
    quit()
    mydb.close()


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
        print("Employee " + firstname + " " + lastname + " was added.")
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
        print(username + " Account was created Successfully!")
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

            global prop
            prop = account[0]
            print(account[0] + " just logged in!")
            # check if the employee is an admin
            is_manager = account[3]
            if is_manager:
                print("Manager " + account[0] + " just logged in!")
                return "Logging Manager In."
            return "Logging In."
        else:
            return "Incorrect Username/Email or Password."
    else:
        return "Account doesn't exist, consider Signing Up?"


@eel.expose
def add_order(qrCode, quantity, empUsername, promoCode, isOnline):
    if len(qrCode) == 0:
        return "Please add an item."
    # check if all items are present with requested quantities
    for item, itemQuantity in zip(qrCode, quantity):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT EXISTS(SELECT barCode FROM Item WHERE barCode =" + item + ");")
        result = mycursor.fetchone()[0]
        if result != 1:
            return "The item '" + item + "' doesn't exist."
        mycursor = mydb.cursor()
        query = "SELECT leftAmount FROM Item WHERE barCode = " + item + ";"
        mycursor.execute(query)
        result = mycursor.fetchone()[0]
        if result < int(itemQuantity) or int(itemQuantity) == 0:
            return "Requested amount of '" + item + "' is " + str(
                itemQuantity) + " not available. Available amount is " + result
    # Create the order, we need to grab the employee's ID first
    currentDate = str(date.today())
    try:
        query = "Select e.empId from Employee as e join Account as acc on e.empId=acc.empId where username=\"" + empUsername + "\";"
        cursor = mydb.cursor()
        cursor.execute(query)
        empId = cursor.fetchone()
        print("EmpId: " + str(empId[0]))
        if promoCode == "":
            query = "Insert into orders(date,price,isOnline,EmpId) values(\"" + currentDate + "\",1," + str(
                isOnline) + "," + str(
                empId[0]) + ");"
            # add promo code
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
        else:
            query = "Insert into orders(date,price,isOnline,EmpId,promoCode) values(\"" + currentDate + "\",1," + str(
                isOnline) + "," + str(
                empId[0]) + ",\"" + promoCode + "\");"
            # add promo code
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()

        print("New Order created Successfully!!")
    except mysql.connector.IntegrityError as error:
        print("Couldn't place Order! 0")

    # Grab the order id to insert it on each Order-Item relation
    query = "select distinct(last_insert_id()) from Item;"
    cursor = mydb.cursor()
    cursor.execute(query)
    order_id = cursor.fetchone()
    print(str(order_id[0]))
    # Add the items into the order
    for item, itemQuantity in zip(qrCode, quantity):
        try:
            query = "Insert into item_Order(OrderId,barCode,quantity) values(" + str(
                order_id[0]) + "," + item + "," + str(itemQuantity) + ");"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            print("Item of QRcode " + item + " was added successfully!!")
        except mysql.connector.IntegrityError as error:
            return "Couldn't place Order!"
        # Update the quantity of the item
        try:
            query = "Update item set leftAmount=leftAmount-" + str(itemQuantity) + " where barCode=" + item
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            print("Updated " + item + " item's quantity successfully!!")
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")
    # After Updating the quantity of each product we update the price of the order
    try:
        query = "Update orders set price=(select sum(i.Price*io.quantity) from item as i join item_order as io on i.Barcode=io.barcode where orderId=" + str(
            order_id[0]) + ") where orderId=" + str(order_id[0]) + ";"
        cursor = mydb.cursor()
        cursor.execute(query)
        mydb.commit()
        print("Order number " + str(order_id[0]) + " price was updated successfully!!")
        return "Order created Successfully!"
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")


@eel.expose
def add_delivery_order(qrCode, quantity, empUsername, promoCode, firstname, lastname, phoneNumber, address):
    # use add order to add an order
    result = add_order(qrCode, quantity, empUsername, promoCode, True)
    if result == "Order created Successfully!":
        try:
            query = "select distinct(last_insert_id()) from Item;"
            cursor = mydb.cursor()
            cursor.execute(query)
            order_id = cursor.fetchone()
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")
            return "Failed to link customer to his order."
        try:
            query = "Insert into customer(firstname,lastname,phoneNumber,address,orderId) values(\"" + firstname + "\",\"" + lastname + \
                    "\",\"" + phoneNumber + "\",\"" + address + "\"," + str(order_id[0]) + ")"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            print("Customer " + firstname + " " + lastname + "'s order was added Successfully!")
            return "Customer's order was added Successfully!"
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")
    else:
        return "Order failed! Please try again!"


def price(barcode):
    try:
        query = "select price from Item where barcode=" + barcode
        cursor = mydb.cursor()
        cursor.execute(query)
        price = cursor.fetchone()
        if price:
            print(price[0])
            return str(price[0]) + ""
        else:
            print("Price not found!")
            return "Price not found!"
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")
        return "Item not found!"


def name(barcode):
    try:
        query = "select name from Item where barcode=" + barcode
        cursor = mydb.cursor()
        cursor.execute(query)
        name = cursor.fetchone()
        if name:
            print(name[0])
            return name[0] + ""
        else:
            print("Item not found!")
            return "Item not found!"
    except mysql.connector.IntegrityError as error:
        print("Couldn't insert the record to the database, an integrity constraint failed!")
        return "Item not found!"


# takes a manager's username and returns an array of empIds
def getEmpUnder(username):
    try:
        mycursor = mydb.cursor()
        mycursor.execute("SELECT EmpId FROM account WHERE username = \"" + str(username) + "\"")
        manId = mycursor.fetchone()[0]
        # Check if manId is a manager
        mycursor.execute("SELECT EmpId FROM Employee WHERE EmpId =\"" + str(manId) + "\";")
        result = mycursor.fetchone()
    except:
        return "manId is not a manger."
    if result is None:
        return "manId is not a manager."

    # Get the employee ids under the manager
    mycursor.execute("SELECT EmpId FROM Employee WHERE managerId = %s", (manId,))
    result = mycursor.fetchall()
    empIds = [row[0] for row in result]
    return empIds


@eel.expose
def getEmpOrderNum(username):
    empIds = getEmpUnder(username)
    if empIds == "manId is not a manager.":
        return "manId is not a manager."
    empOrderNum = []
    try:
        cursor = mydb.cursor()
        for empId in empIds:
            query = "SELECT count(*) FROM orders WHERE EmpId=" + str(empId) + ";"
            cursor.execute(query)
            empOrderNum.append(cursor.fetchone()[0])

    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."
    if empOrderNum:
        return empOrderNum
    else:
        return False


@eel.expose
def getEmpNames(username):
    empIds = getEmpUnder(username)
    if empIds == "manId is not a manager.":
        return "manId is not a manager."
    fullnames = []
    try:
        cursor = mydb.cursor()
        for empId in empIds:
            cursor.execute("SELECT Firstname, Lastname FROM Employee WHERE EmpId=" + str(empId) + ";")
            result = cursor.fetchone()
            fullnames.append(result[0] + " " + result[1])
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."
    if fullnames:
        return fullnames
    else:
        return False


@eel.expose
def getEmpSalaries(username):
    empIds = getEmpUnder(username)
    if empIds == "manId is not a manager.":
        return "manId is not a manager."
    salaries = []
    try:
        cursor = mydb.cursor()
        for empId in empIds:
            cursor.execute("SELECT salary FROM Employee WHERE EmpId=" + str(empId) + ";")
            result = cursor.fetchone()
            salaries.append(int(result[0]))
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."
    if salaries:
        return salaries
    else:
        return False


def promote(username, empId):
    cursor = mydb.cursor()
    query = "select isMan from Account where empId = " + str(empId) + ";"
    cursor.execute(query)
    result = cursor.fetchone()

    if result is not None and result[0] == 1:
        # empId is already a manager
        return str(empId) + " is already a manager"

    query = "UPDATE Account SET isMan = 1 WHERE empId = " + str(empId) + ";"
    cursor.execute(query)

    empIds = getEmpUnder(username)
    for id in empIds:
        query = "UPDATE Employee SET managerId = %s WHERE EmpId = %s"
        param = (str(empId), str(id))
        cursor.execute(query, param)

    query = "update Employee set managerId = (select empId from Account where username = \"" + username + "\") where EmpId = " + str(
        empId) + ";"
    cursor.execute(query)

    mydb.commit()
    cursor.close()
    return str(empId) + " is now a manager!"

def getItemBarcode():
    barcodes = []
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT barcode FROM item order by name ;")
        result = cursor.fetchall()
        barcodes = [row[0] for row in result]
        return barcodes
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."


@eel.expose
def getItemNames():
    itemBarcodes= getItemBarcode()
    itemNames = []
    try:
        cursor = mydb.cursor()
        for item in itemBarcodes:
            cursor.execute("SELECT name from item where barcode=\""+str(item)+"\";")
            result = cursor.fetchone()
            itemNames.append(result[0])
        return itemNames
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."


@eel.expose
def getItemPrice():
    itemBarcodes= getItemBarcode()
    itemPrices = []
    try:
        cursor = mydb.cursor()
        for item in itemBarcodes:
            cursor.execute("SELECT price from item where barcode=\""+str(item)+"\";")
            result = cursor.fetchone()
            itemPrices.append(float(result[0]))
        return itemPrices
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

@eel.expose
def getItemQuantity():
    itemBarcodes= getItemBarcode()
    itemQunatities = []
    try:
        cursor = mydb.cursor()
        for item in itemBarcodes:
            cursor.execute("SELECT leftAmount from item where barcode=\""+str(item)+"\";")
            result = cursor.fetchone()[0]
            itemQunatities.append(int(result))
        return itemQunatities
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

def filterBarcode(leftAmount):
    barcodes = []
    try:
        cursor = mydb.cursor()
        cursor.execute("SELECT barcode FROM item where leftAmount<="+str(leftAmount)+" order by leftAmount;")
        result = cursor.fetchall()
        barcodes = [row[0] for row in result]
        return barcodes
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."


@eel.expose
def filterItemName(leftAmount):
    itemBarcodes= filterBarcode(leftAmount)
    itemNames = []
    try:
        cursor = mydb.cursor()
        for item in itemBarcodes:
            cursor.execute("SELECT name from item where barcode=\""+str(item)+"\";")
            result = cursor.fetchone()[0]
            itemNames.append(result)
        return itemNames
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

@eel.expose
def filterItemQuantity(leftAmount):
    itemBarcodes= filterBarcode(leftAmount)
    itemQunatities = []
    try:
        cursor = mydb.cursor()
        for item in itemBarcodes:
            cursor.execute("SELECT leftAmount from item where barcode=\""+str(item)+"\";")
            result = cursor.fetchone()[0]
            itemQunatities.append(int(result))
        return itemQunatities
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

@eel.expose
def filterItemPrice(leftAmount):
    itemBarcodes= filterBarcode(leftAmount)
    itemPrices = []
    try:
        cursor = mydb.cursor()
        for item in itemBarcodes:
            cursor.execute("SELECT price from item where barcode=\""+str(item)+"\";")
            result = cursor.fetchone()[0]
            itemPrices.append(float(result))
        return itemPrices
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."


def filterSupplierIds(leftAmount):
    itemBarcodes = filterBarcode(leftAmount)
    itemSupplierId = []
    try:
        cursor = mydb.cursor()
        for item in itemBarcodes:
            cursor.execute("SELECT supplierId from Item_supplier where barcode=\"" + str(item) + "\" and price= (select min(price) from Item_Supplier where barcode=\"" + str(item) + "\");")
            result = cursor.fetchone()
            if result:
                itemSupplierId.append(result[0])
            else:
                itemSupplierId.append("There is no current supplier!")
        return itemSupplierId
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

@eel.expose
def filterSupplierName(leftAmount):
    supplierIds = filterSupplierIds(leftAmount)
    itemSupplierName = []
    try:
        cursor = mydb.cursor()
        for supplierId in supplierIds:
            if supplierId != "There is no current supplier!":
                cursor.execute("SELECT name from supplier where supplierId=" + str(supplierId) + " ;")
                result = cursor.fetchone()
                if result:
                    itemSupplierName.append(result[0])
                else:
                    itemSupplierName.append("There is no current supplier!")
            else:
                itemSupplierName.append("There is no current supplier!")
        return itemSupplierName
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

@eel.expose
def filterSupplyPrice(leftAmount):
    supplierIds = filterSupplierIds(leftAmount)
    itemSupplyPrice = []
    try:
        cursor = mydb.cursor()
        for supplierId in supplierIds:
            if supplierId != "There is no current supplier!":
                cursor.execute("SELECT price*supplyAmount from item_supplier where supplierId="+str(supplierId)+";")
                result = cursor.fetchone()
                if result:
                    itemSupplyPrice.append(float(result[0]))
                else:
                    itemSupplyPrice.append("There is no current supplier!")
            else:
                itemSupplyPrice.append("There is no current supplier!")
        return itemSupplyPrice
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

@eel.expose
def filterSupplyQuantity(leftAmount):
    supplierIds = filterSupplierIds(leftAmount)
    itemSupplyQuantity = []
    try:
        cursor = mydb.cursor()
        for supplierId in supplierIds:
            if supplierId != "There is no current supplier!":
                cursor.execute("SELECT supplyAmount from item_supplier where supplierId="+str(supplierId)+";")
                result = cursor.fetchone()
                if result:
                    itemSupplyQuantity.append(int(result[0]))
                else:
                    itemSupplyQuantity.append("There is no current supplier!")
            else:
                itemSupplyQuantity.append("There is no current supplier!")
        return itemSupplyQuantity
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."


@eel.expose
def filterSupplierNumber(leftAmount):
    supplierIds = filterSupplierIds(leftAmount)
    itemSupplyQuantity = []
    try:
        cursor = mydb.cursor()
        for supplierId in supplierIds:
            if supplierId != "There is no current supplier!":
                cursor.execute("SELECT phoneNumber from supplier where supplierId="+str(supplierId)+";")
                result = cursor.fetchone()
                if result:
                    itemSupplyQuantity.append(result[0])
                else:
                    itemSupplyQuantity.append("There is no current supplier!")
            else:
                itemSupplyQuantity.append("There is no current supplier!")
        return itemSupplyQuantity
    except mysql.connector.IntegrityError as error:
        return "Failed to connect to the database."

@eel.expose
def display(entity,username):
    displayEntity(entity,username)

@eel.expose
def getName(barcode):
    item_name = name(barcode)
    return item_name


@eel.expose
def getPrice(barcode):
    item_price = price(barcode)
    return item_price


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


page = "stocks.html"

eel.init("Menu")
eel.start(page, size=(GetSystemMetrics(0), GetSystemMetrics(1)))
