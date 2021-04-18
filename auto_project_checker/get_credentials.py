#!/usr/bin/python3
import os, sys

def check_credentials():
    if os.path.isfile("holberton_login.txt") is False:
        with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
            f.write('')
        welcome = ("\nWelcome to auto project checker! Project was created so you"
                " can run the checker without clicking the 'Check code button'"
                " everytime. You have the option to enter your holberton crede"
                "ntials which will be saved in another file named 'holberton_l"
                "ogin.txt'. As long as this file exists at the root directory,"
                " you should be good to go running this script. If you DO NOT "
                "want your credentials saved, just press enter when"
                " prompted.\n")
        print(welcome)
        return False
    else:
        return True
def get_username():
    """reads from holberton_login"""
    password = ''
    proj_num = ''
    substring = "@holbertonschool.com"
    if check_credentials() == True:
        with open("holberton_login.txt", mode='r', encoding='utf-8') as openfile:
            read = openfile.read().splitlines()
            try:
                username = read[0]
                print("Found username")
                try:
                    password = read[1]
                    proj_num = read[2]
                except:
                    pass
                if substring not in username and username != '':
                    print("Invalid Username")
                    username = input("Enter Holberton Email: ")
                else:
                    print("Found username")
            except:
                username = input("Enter Holberton Email: ")
    else:
        username = input("Enter Holberton Email: ")
    with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n' + proj_num + '\n')
    return username

def get_password():
    username = ''
    proj_num = ''
    if check_credentials() == True:
        with open("holberton_login.txt", mode='r', encoding='utf-8') as openfile:
            read = openfile.read().splitlines()
            try:
                password = read[1]
                print("Found password")
                try:
                    username = read[0]
                    proj_num = read[2]
                except:
                    pass
            except:
                password = input("Enter Password: ")
    else:
        password = input("Enter Password: ")
    with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n' + proj_num + '\n')
    return password

def get_proj_num():
    password = ''
    username = ''
    pre_url = "https://intranet.hbtn.io/projects/"
    pre_url2 = "http://intranet.hbtn.io/projects/"
    if check_credentials() == True:
        with open("holberton_login.txt", mode='r', encoding='utf-8') as openfile:
            read = openfile.read().splitlines()
            try:
                proj_num = read[2]
                if pre_url in proj_num or pre_url2 in proj_num:
                    proj_num = proj_num.split("/")[-1]
                    print("Found project URL")
                elif proj_num == '':
                    proj_num = input("Enter project URL or number: ")
                try:
                    username = read[0]
                    password = read[1]
                except:
                    pass
            except:
                proj_num = input("Enter project URL or number: ")
    else:
        password = input("Enter project URL or number: ")
    with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n' + proj_num + '\n')
    return proj_num