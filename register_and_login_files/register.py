import hashlib
import subprocess
import customtkinter

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
        widgets = root.grid_slaves(row=8, column=0)
        for widget in widgets:
            widget.destroy()

        # Create a label widget if the fields are not all filled
        customtkinter.CTkLabel(master=root, text=m, text_color=color).grid(row=8, column=0, columnspan=3)

    # Check if all entry fields are filled
    if namevar.get() and usernamevar.get() and phonevar.get() and addressvar.get() and passwordvar.get() and \
            repeatpasswordvar.get():

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

        # TODO Insert namevar.get(), usernamevar.get(), phonevar.get(), addressvar.get(), encrypted_password into MySQL

        # TODO Add SMTP email

        # Create a label widget to display registration success message
        message(m="Registration Successful!", color='green')
    else:
        message()


def loginpopup():
    # Close window
    root.destroy()
    # Run register.py
    subprocess.run(["python", "login.py"])


# Heading
customtkinter.CTkLabel(root, text="Register", font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=10, pady=10)
customtkinter.CTkLabel(root, text="").grid(row=8, column=0, columnspan=3)

# Field Name
name = customtkinter.CTkLabel(root, text="Full Name")
username = customtkinter.CTkLabel(root, text="Username")
password = customtkinter.CTkLabel(root, text="Password")
repeatpassword = customtkinter.CTkLabel(root, text="Repeat Password")
phone = customtkinter.CTkLabel(root, text="Phone Number")
address = customtkinter.CTkLabel(root, text="Address")
login = customtkinter.CTkLabel(root, text="Already have an account? Login now.")

# Packing Fields
name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
username.grid(row=2, column=0, padx=10, pady=10, sticky="w")
password.grid(row=3, column=0, padx=10, pady=10, sticky="w")
repeatpassword.grid(row=4, column=0, padx=10, pady=10, sticky="w")
phone.grid(row=5, column=0, padx=10, pady=10, sticky="w")
address.grid(row=6, column=0, padx=10, pady=10, sticky="w")
login.grid(row=9, column=0, columnspan=10, padx=10, pady=10)

# Variables for storing data
namevar = customtkinter.StringVar()
usernamevar = customtkinter.StringVar()
passwordvar = customtkinter.StringVar()
repeatpasswordvar = customtkinter.StringVar()
phonevar = customtkinter.StringVar()
addressvar = customtkinter.StringVar()

# Creating entry field
nameentry = customtkinter.CTkEntry(root, textvariable=namevar)
usernameentry = customtkinter.CTkEntry(root, textvariable=usernamevar)
passwordentry = customtkinter.CTkEntry(root, show='*', textvariable=passwordvar)
repeatpasswordentry = customtkinter.CTkEntry(root, show='*', textvariable=repeatpasswordvar)
phoneentry = customtkinter.CTkEntry(root, validate="key", textvariable=phonevar)
# Limit the entry to only numbers
phoneentry.configure(validatecommand=(phoneentry.register(lambda char: char.isdigit() or char == ""), "%S"))
addressentry = customtkinter.CTkEntry(root, textvariable=addressvar)

# Packing entry fields
nameentry.grid(row=1, column=2, pady=10, sticky="e")
usernameentry.grid(row=2, column=2, pady=10, sticky="e")
passwordentry.grid(row=3, column=2, pady=10, sticky="e")
repeatpasswordentry.grid(row=4, column=2, pady=10, sticky="e")
phoneentry.grid(row=5, column=2, pady=10, sticky="e")
addressentry.grid(row=6, column=2, pady=10, sticky="e")

# Register button
customtkinter.CTkButton(master=root, text="Register", command=getvals).grid(row=7, column=1, pady=10)

# Login button
customtkinter.CTkButton(master=root, text="Login", command=loginpopup).grid(row=10, column=1)

root.mainloop()