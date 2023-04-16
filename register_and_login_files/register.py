import tkinter as tk
import hashlib

root = tk.Tk()
root.title("MMS - Registration")
root.geometry("300x370")

# Centering the window on the screen
window_width = root.winfo_reqwidth()
window_height = root.winfo_reqheight()
position_right = int(root.winfo_screenwidth() / 2 - window_width / 2)
position_down = int(root.winfo_screenheight() / 2 - window_height / 2)
root.geometry("+{}+{}".format(position_right, position_down))

# Preventing window resizing
root.resizable(width=False, height=False)


def getvals():
    def message(message = "Please fill all the fields!", color = 'red'):
        # Destory previous message label
        widgets = root.grid_slaves(row=8, column=0)
        for widget in widgets:
            widget.destroy()

        # Create a label widget if the fields are not all filled
        tk.Label(root, text=message, fg=color).grid(row=8, column=0, columnspan=3)

    # Check if all entry fields are filled
    if namevar.get() and usernamevar.get() and phonevar.get() and addressvar.get() and passwordvar.get() and repeatpasswordvar.get():

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

        # Insert namevar.get(), usernamevar.get(), phonevar.get(), addressvar.get(), encrypted_password into MySQL
        # TODO

        # Create a label widget to display registration success message
        message(message="Registration Successful!", color='green')
    else:
        message()


# Heading
tk.Label(root, text="Registration", font="Arial 15 bold").grid(row=0, column=0, columnspan=10, pady=10)

# Field Name
name = tk.Label(root, text="Full Name")
username = tk.Label(root, text="Username")
password = tk.Label(root, text="Password")
repeatpassword = tk.Label(root, text="Repeat Password")
phone = tk.Label(root, text="Phone Number")
address = tk.Label(root, text="Address")

# Packing Fields
name.grid(row=1, column=0, padx=10, pady=10, sticky="w")
username.grid(row=2, column=0, padx=10, pady=10, sticky="w")
password.grid(row=3, column=0, padx=10, pady=10, sticky="w")
repeatpassword.grid(row=4, column=0, padx=10, pady=10, sticky="w")
phone.grid(row=5, column=0, padx=10, pady=10, sticky="w")
address.grid(row=6, column=0, padx=10, pady=10, sticky="w")

# Variables for storing data
namevar = tk.StringVar()
usernamevar = tk.StringVar()
passwordvar = tk.StringVar()
repeatpasswordvar = tk.StringVar()
phonevar = tk.StringVar()
addressvar = tk.StringVar()
# checkvalue = tk.IntVar()

# Creating entry field
nameentry = tk.Entry(root, textvariable=namevar)
usernameentry = tk.Entry(root, textvariable=usernamevar)
passwordentry = tk.Entry(root, show='*', textvariable=passwordvar)
repeatpasswordentry = tk.Entry(root, show='*', textvariable=repeatpasswordvar)
phoneentry = tk.Entry(root, validate="key", textvariable=phonevar)
# Limit the entry to only numbers
phoneentry.configure(validatecommand=(phoneentry.register(lambda char: char.isdigit() or char == ""), "%S"))
addressentry = tk.Entry(root, textvariable=addressvar)

# Packing entry fields
nameentry.grid(row=1, column=2, pady=10, sticky="e")
usernameentry.grid(row=2, column=2, pady=10, sticky="e")
passwordentry.grid(row=3, column=2, pady=10, sticky="e")
repeatpasswordentry.grid(row=4, column=2, pady=10, sticky="e")
phoneentry.grid(row=5, column=2, pady=10, sticky="e")
addressentry.grid(row=6, column=2, pady=10, sticky="e")

# Creating Checkbox
# checkbtn = tk.Checkbutton(text="Remember Me?", variable=checkvalue)
# checkbtn.grid(row=6, column=3)

# Register button
tk.Button(text="Register", command=getvals).grid(row=7, column=1, pady=10)

root.mainloop()