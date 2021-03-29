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

    # Fetch Saved Project Number
    pre_url = "https://intranet.hbtn.io/projects/"
    PROJ_NUM = ''
    try:
        with open("holberton_login.txt", mode='r', encoding='utf-8') as f:
            read = f.read().splitlines()
            try:
                PROJ_NUM = read[2]
                if PROJ_NUM == '':
                    PROJ_NUM = str(input("Enter project's URL or project number: "))
                    print("The script will assume you want to check this project everytime you run it today. This value will reset at midnight.")
            except:
                PROJ_NUM = str(input("Enter project's URL or project number: "))
                print("The script will assume you want to check this project everytime you run it today. This value will reset at midnight.")
            if pre_url not in PROJ_NUM:
                PROJ_NUM = pre_url + PROJ_NUM
    except:
        PROJ_NUM = str(input("Enter project's URL or project number: "))
        if pre_url not in PROJ_NUM:
                    PROJ_NUM = pre_url + PROJ_NUM

    # Save info to login file
    with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
        f.write(username + '\n' + password + '\n' + PROJ_NUM)

    HOME = "https://intranet.hbtn.io/"
    URL = PROJ_NUM
    # create a new Chrome session
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=PATH, chrome_options=options)
    # driver.implicitly_wait(30)
    # driver.maximize_window()

    # Navigate to the application home page
    driver.get("https://intranet.hbtn.io/auth/sign_in")

    # Sign In
    username_text = driver.find_element_by_id("user_login")
    password_text = driver.find_element_by_id("user_password")

    # Enter Login
    print("Attempting to login as " + username)
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
        print("Project " + PROJ_NUM + " is not a project")
        driver.quit()
        exit(1)
    try:
        print("Project selected: " + project_name.text + "\n")
    except:
        print("Could not get project name...\n")
    check_code_button = driver.find_elements_by_xpath("//button[contains(text(),'Check your code')]")
    task_box = driver.find_elements_by_class_name("task_correction_modal")
    task_card = driver.find_elements_by_class_name("task-card")
    start_test_button = driver.find_elements_by_xpath("//button[contains(text(),'Start a new test')]")
    wait = WebDriverWait(driver, timeout=10)

    # Check if all tasks can check code, start test, and close the task.

    # ONLY WORKS IF QA REVIEW IS FULLY AUTOMATED
    if len(check_code_button) == len(task_box) == len(start_test_button) == len(task_card):
        for count in range(0, len(start_test_button)):
            check_code_button[count].click()
            wait.until(EC.visibility_of(start_test_button[count]))
            start_test_button[count].click()
            close_button = task_box[count].find_element_by_class_name('close')
            close_button.click()
            wait.until(EC.invisibility_of_element(close_button))
            b = "Running Tests [" + "." * count + " " * (len(task_box) - count - 1) + "]"
            print(b, end="\r")
        print("\nRan {:s} tests".format(str(len(start_test_button))))

        total = 0
        earned = 0
        commit_id = "N/A"

    # Check running tests
        for count in range(0, len(task_box)):
            print(task_card[count].find_element_by_class_name("panel-title").text, end='     ')
            print("*"+task_card[count].find_element_by_class_name("label").text.upper()+"*")
            check_code_button[count].click()
            wait.until(EC.visibility_of(start_test_button[count]))
            result_box = task_box[count].find_element_by_class_name("result")
            req_box = result_box.find_elements_by_class_name("requirement")
            check_box = result_box.find_elements_by_class_name("code")
            if count == 0:
                commit_id = result_box.find_elements_by_tag_name("code")[0].text
            total_temp = 0
            earned_temp = 0
            check_mark = "✔️"
            x_mark = "❌"

            for num in range(0, len(req_box)):
                total_temp += 1
                class_names = req_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    print("{}:{}  ".format(req_box[num].text, check_mark), end='')
                elif "fail" in class_names:
                    print("{}:{}  ".format(req_box[num].text, x_mark), end='')
                else:
                    print("unknown")
            if total_temp > 0:
                print()
            for num in range(0, len(check_box)):
                total_temp += 1
                class_names = check_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    print("{}:{}  ".format(check_box[num].text, check_mark), end='')
                elif "fail" in class_names:
                    print("{}:{}  ".format(check_box[num].text, x_mark), end='')
                else:
                    print("unknown")
            if total_temp > 0:
                print()
            print()
            total += total_temp
            earned += earned_temp
            close_button = task_box[count].find_element_by_class_name('close')
            close_button.click()
            wait.until(EC.invisibility_of_element(close_button))
        print("Check: {}/{}".format(earned, total))
        print("Used commit id: " + commit_id)
        # print("grades")

        # driver.get(HOME)

        # grade_percent = project_page.find_elements_by_class_name("project_progress_percentage")
        # project_name = project_page.find_elements_by_tag_name("code")

        # for a in range(0, len(grade_percent)):
        #     print(grade_percent[a].text)
        #     print("Project {}: {}".format(project_name[a].text, grade_percent[a].text))
    else:
        print("Checker is not out yet silly.")
    time.sleep(2)
    driver.quit()
