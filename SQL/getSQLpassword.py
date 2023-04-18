import customtkinter
import mysql.connector
import codecs

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

root = customtkinter.CTk()
root.title("SQL Password")
# root.geometry("300x450")

# Centering the window on the screen
window_width = 250
window_height = 180
x = int(int(root.winfo_screenwidth() / 2) - int(window_width / 2))
y = int(int(root.winfo_screenheight() / 2) - int(window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Preventing window resizing
root.resizable(width=False, height=False)


def sqlcheck():
    def message(m="Please enter the SQL password!", color='red'):
        # Destroy previous message label
        widgets = root.grid_slaves(row=9, column=0)
        for widget in widgets:
            widget.destroy()

        # Create a label widget if the fields are not all filled
        customtkinter.CTkLabel(master=root, text=m, text_color=color).grid(row=9, column=0, columnspan=3)

    # Check if all entry fields are filled
    if passwordvar.get():

        try:
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password=passwordvar.get(),
                port=3306,
                database="mms"
            )
        except mysql.connector.Error as error:
            message("Database Connection Failed!")
            return

        message(m="Database Connection Success!", color='green')

        root.destroy()
        # print(codecs.encode(passwordvar.get(), 'rot13'))
        # print(passwordvar.get())
        with open("../SQL/sqlpassword.txt", "w") as f:
            # Write the value of the variable to the file
            f.write(codecs.encode(passwordvar.get(), 'rot13'))
    else:
        message()


# Heading
customtkinter.CTkLabel(root, text="Enter SQL Password", font=("Arial", 15, "bold")).grid(row=0, column=0, columnspan=10,
                                                                                         pady=10)

# Variables for storing data
passwordvar = customtkinter.StringVar()

# Creating entry field
passwordentry = customtkinter.CTkEntry(root, show='*', textvariable=passwordvar)

# Packing entry fields
passwordentry.grid(row=3, column=1, pady=10, padx=50, sticky="e")

# Continue button
customtkinter.CTkButton(master=root, text="Continue", command=sqlcheck).grid(row=8, column=1, pady=10)

root.mainloop()
