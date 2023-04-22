import customtkinter
import mysql.connector
import configparser


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("SQL Connection")
# root.geometry("300x450")

# Centering the window on the screen
window_width = 230
window_height = 320
x = int(int(root.winfo_screenwidth() / 2) - int(window_width / 2))
y = int(int(root.winfo_screenheight() / 2) - int(window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Preventing window resizing
root.resizable(width=False, height=False)


def getvals():
    def message(m="Please fill all the fields!", color='red'):
        # Destroy previous message label
        widgets = root.grid_slaves(row=6, column=0)
        for widget in widgets:
            widget.destroy()

        # Create a label widget if the fields are not all filled
        customtkinter.CTkLabel(master=root, text=m, text_color=color).grid(row=6, column=0, columnspan=3)

    # Check if all entry fields are filled
    if uservar.get() and passwordvar.get() and hostvar.get() and databasevar.get():
        try:
            mydb = mysql.connector.connect(
                host=hostvar.get(),
                user=uservar.get(),
                password=passwordvar.get(),
                port=3306,
                database=databasevar.get()
            )
        except mysql.connector.Error as error:
            message("Database Connection Failed!")
            return

        config = configparser.ConfigParser()
        config['mysql'] = {
            'user': uservar.get(),
            'password': passwordvar.get(),
            'host': hostvar.get(),
            'database': databasevar.get()
        }

        with open('../config.cfg', 'w') as configfile:
            config.write(configfile)

        # Create a label widget to display registration success message
        message(m="Connection Successful!", color='green')
    else:
        message()


# Heading
customtkinter.CTkLabel(root, text="SQL Connection", font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=10, pady=10)
customtkinter.CTkLabel(root, text="").grid(row=6, column=0, columnspan=3)

# Field Name
user = customtkinter.CTkLabel(root, text="User")
password = customtkinter.CTkLabel(root, text="Password")
host = customtkinter.CTkLabel(root, text="Host")
database = customtkinter.CTkLabel(root, text="Database")


# Packing Fields
user.grid(row=1, column=0, padx=10, pady=10, sticky="w")
password.grid(row=2, column=0, padx=10, pady=10, sticky="w")
host.grid(row=3, column=0, padx=10, pady=10, sticky="w")
database.grid(row=4, column=0, padx=10, pady=10, sticky="w")

# Variables for storing data
uservar = customtkinter.StringVar()
passwordvar = customtkinter.StringVar()
hostvar = customtkinter.StringVar()
databasevar = customtkinter.StringVar()

# Creating entry field
userentry = customtkinter.CTkEntry(root, textvariable=uservar)
passwordentry = customtkinter.CTkEntry(root, show='*', textvariable=passwordvar)
hostentry = customtkinter.CTkEntry(root, textvariable=hostvar)
databaseentry = customtkinter.CTkEntry(root, validate="key", textvariable=databasevar)

# Packing entry fields
userentry.grid(row=1, column=2, pady=10, sticky="e")
passwordentry.grid(row=2, column=2, pady=10, sticky="e")
hostentry.grid(row=3, column=2, pady=10, sticky="e")
databaseentry.grid(row=4, column=2, pady=10, sticky="e")

# Connect button
customtkinter.CTkButton(master=root, text="Connect", command=getvals).grid(row=5, column=0, columnspan=3, pady=10)


root.mainloop()