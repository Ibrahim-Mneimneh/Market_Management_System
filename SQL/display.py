import configparser
import hashlib
import subprocess
import customtkinter
import mysql.connector
import codecs
import os
import atexit


def on_exit():
    print("Program is exiting!")
    file_path = "../SQL/sqlpassword.txt"
    if os.path.exists(file_path):
        os.remove(file_path)
        print("File removed!")
    else:
        print("File does not exist.")


atexit.register(on_exit)

sqlpassword = ""


def readpassword():
    global sqlpassword
    file_path = "../SQL/sqlpassword.txt"
    if os.path.exists(file_path):
        if os.path.getsize(file_path) > 0:
            with open(file_path, "r") as f:
                sqlpassword = codecs.decode(f.read(), 'rot13')
                return True
        else:
            print("File is empty.")
            subprocess.run(['python', '../SQL/getSQLpassword.py'])
    else:
        print("File does not exist.")
        subprocess.run(['python', '../SQL/getSQLpassword.py'])
    return False


while not readpassword():
    readpassword()

    # result = subprocess.run(['python', '../SQL/getSQLpassword.py'], capture_output=True, text=True)
    # sqlpassword = result.stdout.strip()
    # sqlpassword = codecs.decode(result_output, 'rot13')

    # try:
    #     mydb = mysql.connector.connect(
    #         host="localhost",
    #         user="root",
    #         password=sqlpassword,
    #         port=3306,
    #         database="mms"
    #     )
    # except mysql.connector.Error as error:
    #     print("Database Connection Failed!")
    #     quit()
    #     mydb.close()

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

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("Register")
# root.geometry("300x450")

# Centering the window on the screen
window_width = 420
window_height = 510
x = int(int(root.winfo_screenwidth() / 2) - int(window_width / 2))
y = int(int(root.winfo_screenheight() / 2) - int(window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Preventing window resizing
root.resizable(width=False, height=False)


def getvals():
    def message(m="Please fill all the fields!", color='red'):
        # Destroy previous message label
        widgets = root.grid_slaves(row=9, column=0)
        for widget in widgets:
            widget.destroy()

        # Create a label widget if the fields are not all filled
        customtkinter.CTkLabel(master=root, text=m, text_color=color).grid(row=9, column=0, columnspan=3)

    # Check if all entry fields are filled
    if namevar.get() and usernamevar.get() and phonevar.get() and passwordvar.get() and repeatpasswordvar.get() and emailvar.get():

        # Check if there is a space in the name
        if not (' ' in namevar.get() and namevar.get().index(' ') != 0 and namevar.get().index(' ') != len(
                namevar.get()) - 1):
            message("Enter your full name correctly.")
            return

        # Check if username is one word
        if not len(usernamevar.get().split()) == 1:
            message("Username cannot have spaces.")
            return

        # Password conditions
        if not passwordvar.get() == repeatpasswordvar.get():
            message("Passwords do not match.")
            return
        elif not len(passwordvar.get()) >= 8:
            message("Password must be at least 8 characters long.")
            return
        elif not any(char.isdigit() for char in passwordvar.get()):
            message("Password must contain at least 1 digit.")
            return
        elif not any(char.islower() for char in passwordvar.get()):
            message("Password must contain at least 1 lowercase character.")
            return
        elif not any(char.isupper() for char in passwordvar.get()):
            message("Password must contain at least 1 uppercase character.")
            return

        encrypted_password = hashlib.sha256(passwordvar.get().encode()).hexdigest()

        # TODO Check if username and email already exist

        # Add an Employee TODO add managerid too
        try:
            fname, lname = namevar.get().split()
            query = "INSERT INTO Employee (Firstname, Lastname, Salary, PhoneNumber)" \
                    "VALUES (\"" + fname + "\", \"" + lname + "\", 500, \"" + phonevar.get() + "\");"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            print(cursor.rowcount, "rows were added to the database!")
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")

        # Add an Account for the Employee
        try:
            # TODO Check if admin (check first 5 letters == "Admin")
            query = "INSERT INTO Account VALUES (\"" + usernamevar.get() + "\", \"" + encrypted_password + "\", \"" + \
                    emailvar.get() + "\", False, " + "(select EmpId from Employee where PhoneNumber = \"" + phonevar.get() + "\"));"
            cursor = mydb.cursor()
            cursor.execute(query)
            mydb.commit()
            print(cursor.rowcount, "rows were added to the database!")
        except mysql.connector.IntegrityError as error:
            print("Couldn't insert the record to the database, an integrity constraint failed!")

        # TODO Add SMTP email

        # Create a label widget to display registration success message
        message(m="Registration Successful!", color='green')
    else:
        message()


def loginpopup():
    # Close window
    root.destroy()
    # Run login.py
    subprocess.run(["python", "../register_and_login_files/login.py"])


# Heading
customtkinter.CTkLabel(root, text="Register", font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=10, pady=10)
customtkinter.CTkLabel(root, text="").grid(row=9, column=0, columnspan=3)

# Field Name
name = customtkinter.CTkLabel(root, text="Full Name")
username = customtkinter.CTkLabel(root, text="Username")
password = customtkinter.CTkLabel(root, text="Password")
repeatpassword = customtkinter.CTkLabel(root, text="Repeat Password")
email = customtkinter.CTkLabel(root, text="Email")
phone = customtkinter.CTkLabel(root, text="Phone Number")
address = customtkinter.CTkLabel(root, text="Address")
login = customtkinter.CTkLabel(root, text="Already have an account? Login now.")

# Packing Fields
name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
username.grid(row=2, column=0, padx=10, pady=10, sticky="w")
password.grid(row=3, column=0, padx=10, pady=10, sticky="w")
repeatpassword.grid(row=4, column=0, padx=10, pady=10, sticky="w")
email.grid(row=5, column=0, padx=10, pady=10, sticky="w")
phone.grid(row=6, column=0, padx=10, pady=10, sticky="w")
login.grid(row=10, column=0, columnspan=10, padx=10, pady=10)

# Variables for storing data
namevar = customtkinter.StringVar()
usernamevar = customtkinter.StringVar()
passwordvar = customtkinter.StringVar()
repeatpasswordvar = customtkinter.StringVar()
emailvar = customtkinter.StringVar()
phonevar = customtkinter.StringVar()

# Creating entry field
nameentry = customtkinter.CTkEntry(root, textvariable=namevar)
usernameentry = customtkinter.CTkEntry(root, textvariable=usernamevar)
passwordentry = customtkinter.CTkEntry(root, show='*', textvariable=passwordvar)
repeatpasswordentry = customtkinter.CTkEntry(root, show='*', textvariable=repeatpasswordvar)
emailentry = customtkinter.CTkEntry(root, textvariable=emailvar)
phoneentry = customtkinter.CTkEntry(root, validate="key", textvariable=phonevar)
# Limit the entry to only numbers
phoneentry.configure(validatecommand=(phoneentry.register(lambda char: char.isdigit() or char == ""), "%S"))

# Packing entry fields
nameentry.grid(row=1, column=2, pady=10, sticky="e")
usernameentry.grid(row=2, column=2, pady=10, sticky="e")
passwordentry.grid(row=3, column=2, pady=10, sticky="e")
repeatpasswordentry.grid(row=4, column=2, pady=10, sticky="e")
emailentry.grid(row=5, column=2, pady=10, sticky="e")
phoneentry.grid(row=6, column=2, pady=10, sticky="e")

# Register button
customtkinter.CTkButton(master=root, text="Register", command=getvals).grid(row=8, column=1, pady=10)

# Login button
customtkinter.CTkButton(master=root, text="Login", command=loginpopup).grid(row=11, column=1)

root.mainloop()
