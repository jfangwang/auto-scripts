#!/usr/bin/python3
import os, sys
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from datetime import date
import time

def run_checker(user, passwd):
    # Credentials
    username = user
    password = passwd

    # get the path of ChromeDriverServer
    PATH = os.getcwd() + '\\auto_project_checker\\chromedriver.exe'
    print(PATH)
    PROJ_NUM = str(input("Enter project's URL or project number: "))
    URL = "https://intranet.hbtn.io/projects/" + PROJ_NUM
    HOME = "https://intranet.hbtn.io/"
    # create a new Chrome session
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)
    # driver.implicitly_wait(30)
    # driver.maximize_window()

    # Navigate to the application home page
    driver.get("https://intranet.hbtn.io/auth/sign_in")

    # Sign In
    username_text = driver.find_element_by_id("user_login")
    password_text = driver.find_element_by_id("user_password")

    # Enter Login
    print("Attempting to log into " + username)
    username_text.clear()
    username_text.send_keys(username)
    password_text.clear()
    password_text.send_keys(password)
    login_button = driver.find_element_by_name("commit")
    login_button.click()

    timeout = 1
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'student-home'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        print("Invalid Credentials")
        username = input("Re-enter Username: ")
        password = input("Re-enter Password: ")
        with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
            f.write(username + '\n' + password + '\n')
        driver.quit()
        run_checker(username, password)
        exit(1)

    print("\nLOGIN SUCCESSFUL\n")
    driver.get(URL)

    try:
        project_page = driver.find_element_by_xpath("//article")
        project_name = project_page.find_element_by_xpath("//h1")
    except:
        print("Project number " + PROJ_NUM + " does not exist")
        driver.quit()
        exit(1)
    try:
        print("Project selected: " + project_name.text + "\n")
    except:
        print("Could not get project name...\n")

    check_code_button = driver.find_elements_by_xpath("//button[contains(text(),'Check your code')]")
    header = driver.find_elements_by_class_name("task_correction_modal")
    start_test_button = driver.find_elements_by_xpath("//button[contains(text(),'Start a new test')]")

    # Check if all tasks can check code, start test, and close the task.

    if len(check_code_button) == len(header) == len(start_test_button):

        for count in range(0, len(start_test_button)):
            # Temporary, have to implement WebDriverWait() for faster performance
            sleep_num = 0.5
            driver.implicitly_wait(sleep_num)
            time.sleep(sleep_num)
            check_code_button[count].click()
            # print("check code button clicked")
            driver.implicitly_wait(sleep_num)
            time.sleep(sleep_num)
            start_test_button[count].click()
            # print("start test button clicked")
            close_button = header[count].find_element_by_class_name('close')
            close_button.click()
            # print("close button clicked")
            b = "Running Tests [" + "." * count + " " * (len(header) - count - 1) + "]"
            print (b, end="\r")
        print("\nRan {:s} tests".format(str(count)))
    else:
        print("This is a weird webpage, developer must write better code and optimize me.")

    # print("grades")

    # driver.get(HOME)

    # grade_percent = project_page.find_elements_by_class_name("project_progress_percentage")
    # project_name = project_page.find_elements_by_tag_name("code")

    # for a in range(0, len(grade_percent)):
    #     print(grade_percent[a].text)
    #     print("Project {}: {}".format(project_name[a].text, grade_percent[a].text))
    time.sleep(5)
    driver.quit()
    print("Bye Bye!")