#!/usr/bin/python3
from checker import run_checker
from helper_functions import *
import os, sys
import getpass
def run():
    check_credentials()
    username = get_username()
    password = get_password()
    flags = get_flags()
    files = get_files_changed()
    run_checker(username, password, flags, files)
