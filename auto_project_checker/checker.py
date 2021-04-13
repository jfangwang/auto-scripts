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
    PATH_lin = 'chromedriver'
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

    timeout = 600
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
    task_popup = driver.find_elements_by_class_name("task_correction_modal")
    task_box = driver.find_elements_by_class_name("task-card")
    start_test_button = driver.find_elements_by_xpath("//button[contains(text(),'Start a new test')]")
    # Change timeout(seconds) to change the wait duration for results to load from checker.
    wait = WebDriverWait(driver, timeout)

    before_tests_time = datetime.now()
    login_time = before_tests_time - start_time
    # Check if all tasks can check code, start test, and close the task. testing...
    # ONLY WORKS IF QA REVIEW IS FULLY AUTOMATED
    if len(check_code_button) == len(task_popup) == len(start_test_button) and len(check_code_button) > 0:
    # if len(check_code_button) == len(start_test_button):
        for count in range(0, len(start_test_button)):
            check_code_button[count].click()
            wait.until(EC.visibility_of(start_test_button[count]))
            start_test_button[count].click()
            close_button = task_popup[count].find_element_by_class_name('close')
            close_button.click()
            wait.until(EC.invisibility_of_element(close_button))
            b = "Starting tests [" + "." * count + " " * (len(task_popup) - count - 1) + "]"
            print(b, end="\r")
        print("\nClicked {:s} buttons".format(str(len(start_test_button))))
        task_type = "mandatory"
        man_total = 0
        man_earned = 0
        adv_total = 0
        adv_earned = 0
        commit_id = 0
        col, row = os.get_terminal_size()
        max_width = col
        # Check the results
        # Click every task and check
        print()
        # for count in range(0, len(check_code_button)):
        count = 0
        show_score = True
        for task_count in range(0, len(task_box)):
            new_line_count = 0
            output_length = 0
            results_loaded = True
            task_name = task_box[task_count].find_element_by_class_name("panel-title").text
            task_type = task_box[task_count].find_element_by_class_name("label").text
            print("-" * max_width)
            # print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) + task_type.upper()+" |")
            if "advanced" in task_type:
                print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) +"\033[5;30;45m"+ task_type.upper()+"\033[0m |")
            else:
                print("| " + task_name + (" " * (max_width-len(task_name)-len(task_type)-4)) +task_type.upper()+" |")
            print("-" * max_width)

            # Checks if task box has a check code button
            button_list = task_box[task_count].find_elements_by_tag_name("button")
            has_check_code_button = False
            for item in button_list:
                if "Check your code" in item.text:
                    has_check_code_button = True
            if has_check_code_button == False:
                sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                notice = "   \033[5;30;43mMANUAL QA REVIEW\033[0m"
                if "advanced" in task_type:
                    print("| " + task_name + notice + (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) +"\033[5;30;45m"+task_type.upper()+"\033[0m |")
                else:
                    print("| " + task_name + notice + (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) + task_type.upper()+" |")
                print("-" * max_width)
                continue

            check_code_button[count].click()
            try:
                # wait.until(EC.visibility_of(start_test_button[count]))
                ascii_animation = [
                    '...',
                    'o..',
                    'Oo.',
                    'oOo',
                    '.oO',
                    '..o',
                    '...'
                ]
                counter = 0
                results_loaded = False
                wait = WebDriverWait(driver, 0.7)
                while counter < timeout and results_loaded == False:
                    try:
                        wait.until(EC.visibility_of(start_test_button[count]))
                        results_loaded = True
                    except KeyboardInterrupt:
                        sys.exit(1)
                    except:
                        for a in range(0, len(ascii_animation)):
                            print("Checker is loading {}".format(ascii_animation[a]), end="\r")
                            time.sleep(0.3/len(ascii_animation))
                        new_line_count = 1
                    counter += 1
                if results_loaded == False:
                    start_test_button[count].click()
            except:
                results_loaded = False
            wait = WebDriverWait(driver, timeout)
            result_box = task_popup[count].find_element_by_class_name("result")
            req_box = result_box.find_elements_by_class_name("requirement")
            check_box = result_box.find_elements_by_class_name("code")
            if count == commit_id:
                try:
                    commit_id = result_box.find_elements_by_tag_name("code")[0].text
                except:
                    commit_id += 1
                    pass
            total_temp = 0
            earned_temp = 0
            code_check_mark = "\033[5;30;42m"+"[+]"+"\033[0m"
            code_x_mark = "\033[5;30;41m"+"[-]"+"\033[0m"
            req_check_mark = "\033[5;32;40m"+"[+]"+"\033[0m"
            req_x_mark = "\033[5;31;40m"+"[-]"+"\033[0m"
            # Going throught each check in the task
            # Requirement Checks
            output_length = 0
            for num in range(0, len(req_box)):
                total_temp += 1
                class_names = req_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    output_text = "{}:{} ".format(req_box[num].text, req_check_mark)
                elif "fail" in class_names:
                    output_text = "{}:{} ".format(req_box[num].text, req_x_mark)
                else:
                    print("unknown")
                    pass
                output_length += len(output_text) - 14
                if output_length > max_width:
                    print("\n")
                    new_line_count += 1
                    output_length = len(output_text)
                print(output_text, end='')
            if total_temp > 0:
                print()
                new_line_count += 1
            # Code Checks
            output_length = 0
            for num in range(0, len(check_box)):
                total_temp += 1
                class_names = check_box[num].get_attribute("class")
                if "success" in class_names:
                    earned_temp += 1
                    output_text = "{}:{} ".format(check_box[num].text, code_check_mark)
                elif "fail" in class_names:
                    output_text = "{}:{} ".format(check_box[num].text, code_x_mark)
                else:
                    print("unknown")
                    pass
                output_length += len(output_text) - 14
                if output_length > max_width:
                    print()
                    new_line_count += 1
                    output_length = len(output_text)
                print(output_text, end='')
            if total_temp > 0:
                print()
                new_line_count += 1
            if "mandatory" in task_type:
                man_total += total_temp
                man_earned += earned_temp
            else:
                adv_total += total_temp
                adv_earned += earned_temp
            if earned_temp != total_temp:
                print("**Missing {:d}**".format(total_temp - earned_temp))
            elif results_loaded == False:
                # If results did not load
                sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                notice = "    \033[5;30;44mCHECKER TOOK TOO LONG\033[0m"
                if "advanced" in task_type:
                    print("| " + task_name +notice+ (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) +"\033[5;30;45m"+task_type.upper()+"\033[0m |")
                else:
                    print("| " + task_name +notice+ (" " * (max_width-len(task_name)-len(task_type)-len(notice)+14-4)) + task_type.upper()+" |")
                print("-" * max_width)
                show_score = False
            else:
                # Every check is correct
                sys.stdout.write("\033[F" * (new_line_count + 3))
                print("-" * max_width)
                if "advanced" in task_type:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +"\033[5;30;45m"+ task_type.upper()+"\033[0m |")
                else:
                    print("| \033[5;30;42m" + task_name +"\033[0m"+ (" " * (max_width-len(task_name)-len(task_type)-4)) +task_type.upper()+" |")
                print("-" * max_width)
            close_button = task_popup[count].find_element_by_class_name('close')
            wait.until(EC.visibility_of(close_button))
            close_button.click()
            wait.until(EC.invisibility_of_element(close_button))
            count += 1
        if commit_id == len(task_box):
            commit_id = "Not Found"
        print('\n\n')
        if show_score == False:
            print("\033[5;30;44mSCORES ARE NOT COMPLETE, CHECK ONLINE FOR COMPLETE SCORE\033[0m")
        print("Mandatory: {}/{}".format(man_earned, man_total))
        print("Advanced: {}/{}".format(adv_earned, adv_total))
        print("Total: {:d}/{:d}".format(man_earned + adv_earned, man_total + adv_total))
        print("Used commit id: " + commit_id)
    elif len(check_code_button) == 0:
        print("=============================")
        print("Checker is not out yet silly.")
        print("=============================")
    else:
        print("This script is unable to run this project.")
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
