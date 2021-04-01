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
from datetime import datetime
import time


def run_checker(user, passwd):
    # Credentials
    username = user
    password = passwd

    # get the path of ChromeDriverServer
    # Pathing on windows
    PATH_win = os.getcwd() + '\\chromedriver.exe'
    #Pathing on Linux
    PATH_lin = './chromedriver'
    # Fetch Saved Project Number
    pre_url = "https://intranet.hbtn.io/projects/"
    pre_url2 = "http://intranet.hbtn.io/projects/"
    PROJ_NUM = ''
    save = True
    try:
        with open("holberton_login.txt", mode='r', encoding='utf-8') as f:
            read = f.read().splitlines()
            try:

                PROJ_NUM = read[2]
                if PROJ_NUM == '' and username == '' and password == '':
                    print("The script will not save username, password, but will save the project URL")
                    PROJ_NUM = str(input("Enter project's URL or project number: "))
                    save = False
                elif PROJ_NUM== '':
                    print("The script will assume you want to check this project everytime you run it. To change it, go to your holberton_login.txt and change line #3")
                    PROJ_NUM = str(input("Enter project's URL or project number: "))
                else:
                    pass
            except:
                print("The script will assume you want to check this project everytime you run it. To change it, go to your holberton_login.txt and change line #3")
                PROJ_NUM = str(input("Enter project's URL or project number: "))
    except:
        PROJ_NUM = str(input("Enter project's URL or project number: "))
    if pre_url in PROJ_NUM or pre_url2 in PROJ_NUM:
        pass
    else:
        PROJ_NUM = pre_url + PROJ_NUM

    # Save info to login file
    if save:
        with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
            f.write(username + '\n' + password + '\n' + PROJ_NUM)
    else:
        with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
            f.write('' + '\n' + '' + '\n' + PROJ_NUM)

    HOME = "https://intranet.hbtn.io/"
    URL = PROJ_NUM
    # create a new Chrome session
    options = Options()
    # options.add_argument('--headless')
    # options.add_argument('--disable-gpu')
    try:
        driver = webdriver.Chrome(executable_path=PATH_lin, chrome_options=options)
        print("Chrome driver found on Linux machine.")
    except:
        try:
            driver = webdriver.Chrome(executable_path=PATH_win, chrome_options=options)
            print("Chrome driver found on Windows machine")
        except:
            print("Check if chromedriver or chromedriver.exe is in this directory")
            exit(1)
    # driver.implicitly_wait(30)
    # driver.maximize_window()

    # Navigate to the application home page
    driver.get("https://intranet.hbtn.io/auth/sign_in")

    # Sign In
    username_text = driver.find_element_by_id("user_login")
    password_text = driver.find_element_by_id("user_password")

    # Prompt if username and password is empty
    if username == '' and password == '':
        print("Username and Password will not be saved. To save it, paste in your username and password on separate line #1 and #2 in your holberton_login.txt file")
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        save = False

    # Tracking runtime
    start_time = datetime.now()

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
        if save == True:
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

    before_tests_time = datetime.now()
    login_time = before_tests_time - start_time
    # Check if all tasks can check code, start test, and close the task. testing...
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

        task_type = "mandatory"
        man_total = 0
        man_earned = 0
        adv_total = 0
        adv_earned = 0
        commit_id = "N/A"
        max_width = 103

        # Check the results
        print()
        for count in range(0, len(task_box)):
            task_name = task_card[count].find_element_by_class_name("panel-title").text
            task_type = task_card[count].find_element_by_class_name("label").text
            print("-" * max_width)
            print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) + task_type.upper()+" |")
            print("-" * max_width)
            check_code_button[count].click()
            try:
                wait.until(EC.visibility_of(start_test_button[count]))
            except:
                print("[DEBUG] Dipping out, checker is taking too long to load...")
                pass
            result_box = task_box[count].find_element_by_class_name("result")
            req_box = result_box.find_elements_by_class_name("requirement")
            check_box = result_box.find_elements_by_class_name("code")
            if count == 0:
                commit_id = result_box.find_elements_by_tag_name("code")[0].text
            total_temp = 0
            earned_temp = 0
            check_mark = "[+]"
            x_mark = "[ ]"
    # Going throught each check in the task
            # Requirement Checks
            for num in range(0, len(req_box)):
                total_temp += 1
                class_names = req_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    output_text = "{}:{}  ".format(req_box[num].text, check_mark)
                    print(output_text, end='')
                elif "fail" in class_names:
                    output_text = "{}:{}  ".format(req_box[num].text, x_mark)
                    print(output_text, end='')
                else:
                    print("unknown")
            if total_temp > 0:
                print()
            # Code Checks
            for num in range(0, len(check_box)):
                total_temp += 1
                class_names = check_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    output_text = "{}:{}  ".format(check_box[num].text, check_mark)
                    print(output_text, end='')
                elif "fail" in class_names:
                    output_text = "{}:{}  ".format(check_box[num].text, x_mark)
                    print(output_text, end='')
                else:
                    print("unknown")
            if total_temp > 0:
                print()
            if "mandatory" in task_type:
                man_total += total_temp
                man_earned += earned_temp
            else:
                adv_total += total_temp
                adv_earned += earned_temp
            if earned_temp != total_temp:
                print("**Missing {:d}**".format(total_temp - earned_temp))
            else:
                print("All good!")
            print()
            close_button = task_box[count].find_element_by_class_name('close')
            close_button.click()
            wait.until(EC.invisibility_of_element(close_button))
        print("Mandatory: {}/{}".format(man_earned, man_total))
        print("Advanced: {}/{}".format(adv_earned, adv_total))
        print("Total: {:d}/{:d}".format(man_earned + adv_earned, man_total + adv_total))
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
    end_time = datetime.now()
    check_tests_time = end_time - before_tests_time
    runtime = end_time - start_time

    print("This script ran in {} seconds. Took {}s to login, {}s to check the results".format(str(runtime.total_seconds()),
                                                                                              str(login_time.total_seconds()),
                                                                                              str(check_tests_time.total_seconds())
                                                                                              ))
    print()
    # time.sleep(15)
    driver.quit()
