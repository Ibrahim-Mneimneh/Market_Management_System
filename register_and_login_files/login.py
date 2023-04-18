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

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("Login")
# root.geometry("220x280")

# Centering the window on the screen
window_width = 230
window_height = 310
x = int(int(root.winfo_screenwidth() / 2) - int(window_width / 2))
y = int(int(root.winfo_screenheight() / 2) - int(window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Preventing window resizing
root.resizable(width=False, height=False)


def authenticate():
    def message(m="Please fill all the fields!", color='red'):
        # Destroy previous message label
        widgets = root.grid_slaves(row=4, column=0)
        for widget in widgets:
            widget.destroy()

        # Create a label widget if the fields are not all filled
        customtkinter.CTkLabel(master=root, text=m, text_color=color).grid(row=4, column=0, columnspan=3)

    # Check if all entry fields are filled
    if usernamevar.get() and passwordvar.get():
        # Check if username is one word
        if not len(usernamevar.get().split()) == 1:
            message("Username cannot have spaces.")
            return

        encrypted_password = hashlib.sha256(passwordvar.get().encode()).hexdigest()

        # TODO Get username from MySQL and compare it to usernamevar.get()
        sqlusername = ""  # Store it here
        if not usernamevar.get() == sqlusername:
            message("Incorrect username or password.")
            return

        # TODO Get sha256 pass from MySQL and compare it to passwordvar.get()
        sqlpassword = ""  # Store it here
        if not passwordvar.get() == sqlpassword:
            message("Incorrect username or password.")
            return

        # Create a label widget to display login success message
        message(m="Login Successful!", color='green')
    else:
        message()


def registerpopup():
    # Close window
    root.destroy()
    # Run register.py
    subprocess.run(["python", "register.py"])


# Heading
customtkinter.CTkLabel(root, text="Login", font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=10, pady=10)
customtkinter.CTkLabel(root, text="").grid(row=4, column=0, columnspan=3)

# Field Name
username = customtkinter.CTkLabel(root, text="Username")
password = customtkinter.CTkLabel(root, text="Password")
register = customtkinter.CTkLabel(root, text="Don't have an account? Register now.")

# Packing Fields
username.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password.grid(row=2, column=0, padx=10, pady=10, sticky="w")
register.grid(row=5, column=0, columnspan=10, padx=10, pady=10, sticky="w")

# Variables for storing data
usernamevar = customtkinter.StringVar()
passwordvar = customtkinter.StringVar()

# Creating entry field
usernameentry = customtkinter.CTkEntry(root, textvariable=usernamevar)
passwordentry = customtkinter.CTkEntry(root, show='*', textvariable=passwordvar)

# Packing entry field
usernameentry.grid(row=1, column=2, pady=10, sticky="e")
passwordentry.grid(row=2, column=2, pady=10, sticky="e")

# Login button
customtkinter.CTkButton(master=root, text="Login", command=authenticate).grid(row=3, column=0, columnspan=10, pady=10)

# Register button
customtkinter.CTkButton(master=root, text="Register", command=registerpopup).grid(row=6, column=0, columnspan=10)

root.mainloop()
