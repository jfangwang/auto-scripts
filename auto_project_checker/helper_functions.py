#!/usr/bin/python3
import os
from sys import argv
import getpass

file_path = "/etc/hbchecker.txt"

def check_credentials():
    if os.path.isfile(file_path) is False:
        with open(file_path, mode='w', encoding='utf-8') as f:
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
        with open(file_path, mode='r', encoding='utf-8') as openfile:
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
    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n' + proj_num + '\n')
    return username

def get_password():
    username = ''
    proj_num = ''
    if check_credentials() == True:
        with open(file_path, mode='r', encoding='utf-8') as openfile:
            read = openfile.read().splitlines()
            try:
                password = read[1]
                if password == '':
                   password =  getpass.getpass("Enter Password: ")
                else:
                    print("Found password")
                try:
                    username = read[0]
                    proj_num = read[2]
                except:
                    pass
            except:
                password =  getpass.getpass("Enter Password: ")
    else:
        password = getpass.getpass("Enter Password: ")
    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n' + proj_num + '\n')
    return password

def get_proj_num():
    password = ''
    username = ''
    pre_url = "https://intranet.hbtn.io/projects/"
    pre_url2 = "http://intranet.hbtn.io/projects/"
    if len(argv) > 1:
        for index in range(1, len(argv)):
            if argv[index].isdecimal():
                return argv[index]
    if check_credentials() == True:
        with open(file_path, mode='r', encoding='utf-8') as openfile:
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
    with open(file_path, mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n' + proj_num + '\n')
    return proj_num

def get_flags():
    flag_list = []
    for index in range(1, len(argv)):
        if "-" in argv[index]:
            for l_idx in range(0, len(argv[index])):
                if "e" in argv[index][l_idx]:
                    flag_list.append("e")
                if "f" in argv[index][l_idx]:
                    flag_list.append("f")
    return flag_list

def get_files_changed():
    """Gets which files were changed"""
    files_list = []
    test = os.popen('git show --name-only')
    repo_location = os.popen('git rev-parse --show-toplevel')
    repo_location = repo_location.readlines()
    repo_location = repo_location[0]
    repo_location = repo_location.replace('\n', '')
    if "Not a git repository" in repo_location:
        files_list.append("Not a git repository")
        return files_list
    files_list.append(repo_location.split('/')[-1])
    output = test.readlines()
    for a in range(6, len(output)):
        files_list.append(output[a].replace('\n', ''))
    return files_list
