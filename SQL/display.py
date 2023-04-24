import os
import subprocess
import mysql.connector
from tkinter import *
from tkinter import ttk
import customtkinter
import csv
import configparser
from tkinter import filedialog

file_path = "../config.cfg"

if not os.path.exists(file_path):
    subprocess.run(['python', '../SQL/SQLprompt.py'])


def displayEntity(entity_input):
    entity = entity_input

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

    # Create cursor
    mycursor = mydb.cursor()

    # Create a Tkinter window
    root = customtkinter.CTk()

    customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
    customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

    # # Maximize the window
    # root.state('zoomed')

    # Set title
    root.title(entity + " Table View")

    def export_to_csv():
        # Fetch data from the table
        mycursor.execute("SELECT * FROM " + entity)
        data = mycursor.fetchall()

        # Get the column names
        mycursor.execute("SHOW COLUMNS FROM " + entity)
        columns = [col[0] for col in mycursor.fetchall()]

        browse_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=entity,
                                                   filetypes=[("CSV files", "*.csv")])

        if not browse_path == '':
            # Open a CSV file for writing
            with open(browse_path, mode='w', newline='') as csv_file:
                # Create a CSV writer object
                writer = csv.writer(csv_file)

                # Write the column names to the CSV file
                writer.writerow(columns)

                # Write the data to the CSV file
                for row in data:
                    writer.writerow(row)

            # Close the CSV file
            csv_file.close()

    def remove_row(tree):
        # Get the selected row(s)
        selected_rows = tree.selection()

        # Loop through each selected row and print the first column value
        for row in selected_rows:
            # TODO Remove query
            values = tree.item(row, 'values')
            print(values[0])

    # Create a Frame to hold the buttons
    button_frame = customtkinter.CTkFrame(root)
    button_frame.pack(side=TOP)

    # Create a button for exporting the table to a CSV file
    pdf_button = customtkinter.CTkButton(button_frame, text="Export to CSV", command=export_to_csv)
    pdf_button.pack(side=LEFT, padx=10)

    # Create a Frame to hold the Treeview widget and scrollbar
    frame = customtkinter.CTkFrame(root)
    frame.pack(pady=10, padx=10, fill=BOTH, expand=True)

    # Create a Treeview widget to display the data
    tree = ttk.Treeview(frame, show='headings')
    tree.pack(side=LEFT, fill=BOTH, expand=True)

    # Create a button for removing selected row(s)
    remove_button = customtkinter.CTkButton(button_frame, text="Remove Row", command=lambda: remove_row(tree))
    remove_button.pack(side=LEFT, padx=10)

    # Create a scrollbar
    # scrollbar = customtkinter.CTkScrollbar(master = frame, orientation="vertical", command=tree.yview)
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL, command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)
    tree.configure(yscrollcommand=scrollbar.set)

    try:
        # Get all data from the table
        mycursor.execute("SELECT * FROM " + entity)

        # Fetch all data
        data = mycursor.fetchall()
    except:
        print("Table not found.")
        quit()

    # Define columns
    columns = [i[0] for i in mycursor.description]
    tree["columns"] = columns

    # Set column headings
    for col in columns:
        tree.column(col, width=100, anchor=CENTER)
        tree.heading(col, text=col, anchor=CENTER)

    # Insert data into the Treeview widget
    for row in data:
        tree.insert("", END, values=row)

    # Execute the Tkinter event loop
    root.mainloop()

    # Close the database connection
    mydb.close()

