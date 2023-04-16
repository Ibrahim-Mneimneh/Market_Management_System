import tkinter as tk
import hashlib
import subprocess

root = tk.Tk()
root.title("Login")
# root.geometry("220x280")

# Centering the window on the screen
window_width = 220
window_height = 280
x = int(int(root.winfo_screenwidth() / 2) - int(window_width / 2))
y = int(int(root.winfo_screenheight() / 2) - int(window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Preventing window resizing
root.resizable(width=False, height=False)


def authenticate():
    def message(message="Please fill all the fields!", color='red'):
        # Destroy previous message label
        widgets = root.grid_slaves(row=4, column=0)
        for widget in widgets:
            widget.destroy()

        # Create a label widget if the fields are not all filled
        tk.Label(root, text=message, fg=color).grid(row=4, column=0, columnspan=3)

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
            message("Username or password incorrect.")
            return

        # TODO Get sha256 pass from MySQL and compare it to passwordvar.get()
        sqlpassword = ""  # Store it here
        if not passwordvar.get() == sqlpassword:
            message("Username or password incorrect.")
            return

        # Create a label widget to display registration success message
        message(message="Login Successful!", color='green')
    else:
        message()


def registerpopup():
    # Close window
    root.destroy()
    # Run register.py
    subprocess.run(["python", "register.py"])


# Heading
tk.Label(root, text="Login", font="Arial 15 bold").grid(row=0, column=0, columnspan=10, pady=10)
tk.Label(root, text="").grid(row=4, column=0, columnspan=3)

# Field Name
username = tk.Label(root, text="Username")
password = tk.Label(root, text="Password")
register = tk.Label(root, text="Don't have an account? Register now.")

# Packing Fields
username.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password.grid(row=2, column=0, padx=10, pady=10, sticky="w")
register.grid(row=5, column=0, columnspan=10, padx=10, pady=10, sticky="w")

# Variables for storing data
usernamevar = tk.StringVar()
passwordvar = tk.StringVar()

# Creating entry field
usernameentry = tk.Entry(root, textvariable=usernamevar)
passwordentry = tk.Entry(root, show='*', textvariable=passwordvar)

# Packing entry field
usernameentry.grid(row=1, column=2, pady=10, sticky="e")
passwordentry.grid(row=2, column=2, pady=10, sticky="e")

# Login button
tk.Button(text="Login", command=authenticate).grid(row=3, column=0, columnspan=10, pady=10)

# Register button
tk.Button(text="Register", command=registerpopup).grid(row=6, column=0, columnspan=10)

root.mainloop()
