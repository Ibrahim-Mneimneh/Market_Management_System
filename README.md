# Market Management System
This project includes multiple Python scripts for a Market Management System. The system allows new users to sign up, and existing users to log in. Once logged in, an employee can create an order (Store Order or Delivery Order). The system is designed to work with a MySQL database.

## Requirements
- Python 3.x
- MySQL Connector Python
- A MySQL Database
+ Requirements are included in ```requirements.txt```

## Installation
- Clone the repository
- Install the required packages using ```pip install -r requirements.txt```
- Create a MySQL database and configure the credentials in ```config.cfg``` (See below)
- Run the python script using main.py

## How to create the MySQL database
- After cloning the repository, you will see ```MMS.sql``` file in the root directory
- Open MySQL Workbench, Select 'Administration' in the 'Navigator' menu
- Select 'Data Import/Restore' 

![image](https://user-images.githubusercontent.com/61628216/236607896-53a44686-7684-4994-8fe3-455c37ea1dd8.png)
- Choose 'Import from Self-Contained File', and specify the file path to ```MMS.sql```

![image](https://user-images.githubusercontent.com/61628216/236608024-0ff7bc07-3515-4532-aeda-6a3e52f12450.png)
- Press 'Start Import', and you are good to go


## How to configure ```config.cfg```
The system will prompt you to create ```config.cfg``` if there isn't one already made. You only have to do this once, but if you want the prompt to appear again, simply delete ```config.cfg```. Next time you run the program, the prompt will appear

![image](https://user-images.githubusercontent.com/61628216/236606239-28f19451-4613-49e0-9d24-20ee91ff9fc6.png)

If you are running MySQL locally, input these:
```
User: root
Password: (your MySQL password)
Host: localhost
Databse: mms
```

If you want to use the email feature,
- [Generate an app password from your Google account](https://support.google.com/mail/answer/185833)
- Edit ```config.cfg``` in a text editor and add these at the end:
```
[email]
email_sender = (your gmail)
email_password = (your generated app password)
```

## ER Diagram
![Market Management System - ER Diagram](https://user-images.githubusercontent.com/61628216/234966292-63740fbe-d928-4ce6-ac11-f3de5a2e2dd2.jpeg)
