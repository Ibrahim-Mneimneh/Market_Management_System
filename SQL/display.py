import os
import subprocess
import mysql.connector
from tkinter import *
from tkinter import ttk
import customtkinter
import csv
import configparser
from tkinter import filedialog
import smtplib
import ssl
from email.message import EmailMessage

file_path = "../config.cfg"

if not os.path.exists(file_path):
    subprocess.run(['python', '../SQL/SQLprompt.py'])


def displayEntity(entity_input, username):
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

    def export_to_csv_email():
        # Fetch data from the table
        mycursor.execute("SELECT * FROM " + entity)
        data = mycursor.fetchall()
        # Get the column names
        mycursor.execute("SHOW COLUMNS FROM " + entity)
        columns = [col[0] for col in mycursor.fetchall()]
        # Define a file path and name to save the CSV file
        browse_path = filedialog.asksaveasfilename(defaultextension=".csv", initialfile=entity,
                                                   filetypes=[("CSV files", "*.csv")])
        # Export data to CSV
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

            # Define the email sender and receiver
            email_sender = config.get('email', 'email_sender')
            email_password = config.get('email', 'email_password')
            query = f"SELECT email FROM Account WHERE username='{username}'"
            cursor = mydb.cursor()
            cursor.execute(query)
            row = cursor.fetchone()
            email_receiver = row[0]
            # Set the subject and body of the email
            subject = entity + ' CSV Export'
            body = "As requested, here is the CSV of the " + entity + " entity you exported."
            # Define the file path and name to attach to the email
            attachment_file_path = os.path.join(os.path.dirname(browse_path), entity + '.csv')
            # Set up the email message with attachment
            em = EmailMessage()
            em['From'] = email_sender
            em['To'] = email_receiver
            em['Subject'] = subject
            em.set_content(body)
            # Open and attach the CSV file to the email
            with open(attachment_file_path, 'rb') as file:
                file_data = file.read()
                em.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=entity + '.csv')
            # Send the email
            # Add SSL (layer of security)
            context = ssl.create_default_context()
            # Log in and send the email
            with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
                smtp.login(email_sender, email_password)
                smtp.sendmail(email_sender, email_receiver, em.as_string())

            print("Email Sent!")


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

    # Create a button for exporting the table to a CSV file
    pdf_button = customtkinter.CTkButton(button_frame, text="Export to CSV and Send Email", command=export_to_csv_email)
    pdf_button.pack(side=LEFT, padx=10)

    # Create a button for removing selected row(s)
    remove_button = customtkinter.CTkButton(button_frame, text="Remove Row", command=lambda: remove_row(tree))
    remove_button.pack(side=LEFT, padx=10)

    mycursor.execute("SELECT COUNT(*) FROM " + entity)
    count = mycursor.fetchone()[0]

    # Create a label widget to display the number of rows
    count_label = customtkinter.CTkLabel(master=root, text=f"Records count: {count}")
    count_label.pack()

    # Create a Frame to hold the Treeview widget and scrollbar
    frame = customtkinter.CTkFrame(root)
    frame.pack(padx=10, fill=BOTH, expand=True)

    # Create a Treeview widget to display the data
    tree = ttk.Treeview(frame, show='headings')
    tree.pack(side=LEFT, fill=BOTH, expand=True)

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


displayEntity("Employee", 'zouheirn')
