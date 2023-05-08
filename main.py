import os
import subprocess

# Get the path to the directory containing the menu.py file
menu_directory = os.path.join(os.getcwd(), 'Main_Menu')

# Change the current working directory to the menu directory
os.chdir(menu_directory)

# Use subprocess to run the menu.py script
subprocess.run(['python', 'menu.py'])

# Change the current working directory back to the original directory
os.chdir('..')
