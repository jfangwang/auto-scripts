#!/usr/bin/python3
from checker import run_checker
# Retrieving Email and Password
try:
    with open("holberton_login.txt", mode='r', encoding='utf-8') as openfile:
        read = openfile.read().splitlines()
        try:
            username = read[0]
            print("Found username")
        except:
            username = input("Enter Holberton Email: ")
        try:
            password = read[1]
            print("Found password")
        except:
            password = input("Enter Password: ")
except:
    welcome = "\nWelcome to auto project checker! Project was created so you\
    can run the checker without clicking the 'Check code button' everytime.\
    Next, you have the option to enter your holberton credentials which will\
    be saved in another file named 'holberton_login.txt'. As long as this\
    file exists at the root directory, you should be good to go running this\
    script.If you DO NOT want your credentials saved, just press enter when\
    prompted.\n"
    print(welcome)
    username = input("Holberton Email: ")
    password = input("Password: ")
    with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n')
finally:
    run_checker(username, password)