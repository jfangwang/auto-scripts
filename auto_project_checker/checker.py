#!/usr/bin/python3
import os
import sys
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
import pickle
from get_credentials import *
from create_driver import create_driver_session

PATH_lin = os.getcwd() + '/chromedriver'
PATH_win = os.getcwd() + '\\chromedriver.exe'
print(PATH_lin)
options = Options()
# options.add_argument('--headless')
options.add_experimental_option("detach", True)
options.add_argument('log-level=3')
save = True
# Check Flags
if get_flags() == 'c':
    check_every_task = True


if os.path.isfile("session_info.txt") is False:
    try:
        driver = webdriver.Chrome(executable_path=PATH_win, options=options)
    except:
        try:
            driver = webdriver.Chrome(executable_path=PATH_lin, options=options)
        except Exception as e:
            print(e)
            exit(1)
    executor_url = driver.command_executor._url
    session_id = driver.session_id
    with open("session_info.txt", mode='w', encoding='utf-8') as f:
        f.write(session_id + '\n' + executor_url + '\n')
    # Login
    driver.get("https://intranet.hbtn.io/auth/sign_in")
    username_text = driver.find_element_by_id("user_login")
    password_text = driver.find_element_by_id("user_password")
    username_text.clear()
    username_text.send_keys(get_username())
    password_text.clear()
    password_text.send_keys(get_password())
    login_button = driver.find_element_by_name("commit")
    login_button.click()
    # Invalid Credentials
    try:
        element_present = EC.presence_of_element_located
        ((By.CLASS_NAME, 'student-home'))
        WebDriverWait(driver, 1).until(element_present)
    except TimeoutException:
        print("Invalid Credentials")
        if save is True:
            username = input("Re-enter Username: ")
            password = input("Re-enter Password: ")
            with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
                f.write(username+'\n' + password + '\n' + get_proj_num() +
                        '\n')
        driver.quit()
        os.remove("session_info.txt")
        os.execl(sys.executable, 'python3', __file__, *sys.argv[1:])
        exit(1)
    HOME = "https://intranet.hbtn.io/projects/"
    PROJ_NUM = get_proj_num()
    driver.get(HOME + PROJ_NUM)
    # Checks if given url is a valid project
    try:
        project_page = driver.find_element_by_xpath("//article")
        project_name = project_page.find_element_by_xpath("//h1")
    except:
        print("Project number " + PROJ_NUM + " is not a project")
        driver.quit()
        proj_num = input("Re-enter project URL/Number: ")
        with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
                f.write(get_username() + '\n' + get_password() + '\n' +
                        proj_num + '\n')
        driver.quit()
        os.remove("session_info.txt")
        os.execl(sys.executable, 'python3', __file__, *sys.argv[1:])
        exit(1)
    try:
        print("Project selected: " + project_name.text + "\n")
    except:
        print("Could not get project name...\n")

else:
    # Attempt to open existing session
    with open("session_info.txt", encoding='utf-8', ) as openfile:
        read = openfile.read().splitlines()
    session_id = read[0]
    executor_url = read[1]
    driver = create_driver_session(session_id, executor_url)
    try:
        a = driver.title
        a = a.split("|")[0]
        print(a)
        if driver.current_url.split("/")[-1] != get_proj_num():
            HOME = "https://intranet.hbtn.io/projects/"
            PROJ_NUM = get_proj_num()
            print(HOME + PROJ_NUM)
            driver.get(HOME + PROJ_NUM)
            # Checks if given url is a valid project
            try:
                project_page = driver.find_element_by_xpath("//article")
                project_name = project_page.find_element_by_xpath("//h1")
            except:
                print("Project number " + PROJ_NUM + " is not a project")
                driver.quit()
                proj_num = input("Re-enter project URL/Number: ")
                with open("holberton_login.txt", mode='w', encoding='utf-8') as f:
                    f.write(get_username() + '\n' + get_password() + '\n' +
                            proj_num+'\n')
                driver.quit()
                os.remove("session_info.txt")
                os.execl(sys.executable, 'python3', __file__, *sys.argv[1:])
                exit(1)
            try:
                print("Project selected: " + project_name.text + "\n")
            except:
                print("Could not get project name...\n")
        driver.minimize_window()
        driver.switch_to.window(driver.current_window_handle)
    except Exception as e:
        os.remove("session_info.txt")
        print("Could not find a running session, starting another one.")
        os.execl(sys.executable, 'python3', __file__, *sys.argv[1:])
        exit(1)

# Chrome session is running

# Disable CSS Animations
driver.execute_script("const styleElement = document.createElement('style');\
    styleElement.setAttribute('id','style-tag');\
    const styleTagCSSes = document.createTextNode('*,:after,:before{-webkit-t\
    ransition:none!important;-moz-transition:none!important;-ms-transition:no\
    ne!important;-o-transition:none!important;transition:none!important;-webk\
    t-transform:none!important;-moz-transform:none!important;-ms-transform:no\
    ne!important;-o-transform:none!important;transform:none!important}');\
    styleElement.appendChild(styleTagCSSes);document.head.appendChild\
    (styleElement);")

# Tracking runtime
start_time = datetime.now()
timeout = 3600

# Setting up locators for selenium
check_code_button = driver.find_elements_by_xpath("//button[contains(text(),\
                                                  'Check your code')]")
task_popup = driver.find_elements_by_class_name("task_correction_modal")
task_box = driver.find_elements_by_class_name("task-card")
start_test_button = driver.find_elements_by_xpath("//button[contains(text(),\
                                                  'Start a new test')]")
wait = WebDriverWait(driver, timeout)
before_tests_time = datetime.now()
login_time = before_tests_time - start_time
clicked_check_code_button = 0
check_every_task = False

# Check if all tasks can check code, start test, and close the task.
if len(check_code_button) == len(task_popup) == len(start_test_button) and len(check_code_button) > 0:
    for count in range(0, len(start_test_button)):
        button_list = task_box[count].find_elements_by_tag_name("button")
        if "Done" in button_list[0].text and "yes" in button_list[0].get_attribute("class") and check_every_task is False:
            continue
        check_code_button[count].click()
        clicked_check_code_button += 1
        wait.until(EC.visibility_of(start_test_button[count]))
        start_test_button[count].click()
        close_button = task_popup[count].find_element_by_class_name('close')
        close_button.click()
        wait.until(EC.invisibility_of_element(close_button))
        b = "Starting tests [" + "." * count + " " * (len(task_popup) - count - 1) + "]"
        print(b, end="\r")
    print("\nClicked {:s} buttons".format(str(clicked_check_code_button)))

    # Setting up important variables
    task_type = "mandatory"
    man_total = 0
    man_earned = 0
    adv_total = 0
    adv_earned = 0
    commit_id = 0
    col, row = os.get_terminal_size()
    max_width = col
    count = 0
    show_score = True
    avg_task_time = []
    print()
    # Click every task and check results
    for task_count in range(0, len(task_box)):
        new_line_count = 0
        output_length = 0
        results_loaded = True
        task_name = task_box[task_count].find_element_by_class_name("panel-title").text
        task_type = task_box[task_count].find_element_by_class_name("label").text
        start_task_time = datetime.now()

        # Print the Task Name
        print("-" * max_width)
        if "advanced" in task_type:
            print("| " + task_name + (" " * (max_width-len(task_name) -
                  len(task_type) - 4)) + "\033[5;30;45m" + task_type.upper() +
                  "\033[0m |")
        else:
            print("| " + task_name + (" " * (max_width - len(task_name) -
                  len(task_type) - 4)) + task_type.upper() + " |")
        print("-" * max_width)

        # Checks if task box has a check code button
        button_list = task_box[task_count].find_elements_by_tag_name("button")
        has_check_code_button = False
        task_completed = False
        for item in button_list:
            if "Check your code" in item.text:
                has_check_code_button = True
            if "Done" in button_list[0].text and "yes" in button_list[0].get_attribute("class") and check_every_task is False:
                task_completed = True
        if has_check_code_button is False:
            sys.stdout.write("\033[F" * (new_line_count + 3))
            print("-" * max_width)
            notice = "   \033[5;30;43mMANUAL QA REVIEW\033[0m"
            if "advanced" in task_type:
                print("| " + task_name + notice + (" " * (max_width -
                      len(task_name) - len(task_type) - len(notice) + 14 - 4
                      )) + "\033[5;30;45m" + task_type.upper() + "\033[0m |")
            else:
                print("| " + task_name + notice + (" " * (max_width -
                      len(task_name) - len(task_type) - len(notice) + 14 - 4
                      )) + task_type.upper() + " |")
            print("-" * max_width)
            continue
        if task_completed is True:
            sys.stdout.write("\033[F" * (new_line_count + 3))
            print("-" * max_width)
            if "advanced" in task_type:
                print("| \033[5;30;42m" + task_name + "\033[0m" + (" " *
                      (max_width - len(task_name) - len(task_type) - 4)) +
                      "\033[5;30;45m" + task_type.upper() + "\033[0m |")
            else:
                print("| \033[5;30;42m" + task_name + "\033[0m" + (" " *
                      (max_width - len(task_name) - len(task_type) - 4)) +
                      task_type.upper() + " |")
            print("-" * max_width)
            commit_id += 1
            continue
        check_code_button[task_count].click()

        # wait for the results to load
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
            while counter < timeout and results_loaded is False:
                try:
                    wait.until(EC.visibility_of(start_test_button[task_count]))
                    results_loaded = True
                except KeyboardInterrupt:
                    sys.exit(1)
                except:
                    for a in range(0, len(ascii_animation)):
                        print("Waiting for checker {}".
                              format(ascii_animation[a]), end="\r")
                        time.sleep(0.3/len(ascii_animation))
                counter += 1
            if results_loaded is False:
                start_test_button[task_count].click()
        except:
            results_loaded = False

        # Setting up for popup box
        wait = WebDriverWait(driver, timeout)
        result_box = task_popup[task_count].find_element_by_class_name("result")
        req_box = result_box.find_elements_by_class_name("requirement")
        check_box = result_box.find_elements_by_class_name("code")

        # Get the first valid commit id
        if task_count == commit_id:
            try:
                commit_id = result_box.find_elements_by_tag_name("code")[0].text
            except:
                commit_id += 1
                pass
        output_length = 0
        total_temp = 0
        earned_temp = 0
        code_check_mark = "\033[5;30;42m"+"[+]"+"\033[0m"
        code_x_mark = "\033[5;30;41m"+"[-]"+"\033[0m"
        req_check_mark = "\033[5;32;40m"+"[+]"+"\033[0m"
        req_x_mark = "\033[5;31;40m"+"[-]"+"\033[0m"

        # Going throught each check in the task

        # Requirement Checks
        for num in range(0, len(req_box)):
            total_temp += 1
            class_names = req_box[num].get_attribute("class")
            if "success" in class_names:
                earned_temp += 1
                output_text = "{}:{} ".format(req_box[num].text,
                                              req_check_mark)
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
        # Print new line if there are any req checks
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
                output_text = "{}:{} ".format(check_box[num].text,
                                              code_check_mark)
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

        # Print new line if there are any code checks
        if total_temp > 0:
            print()
            new_line_count += 1

        # Close the task
        close_button = task_popup[task_count].find_element_by_class_name('close')
        wait.until(EC.visibility_of(close_button))
        close_button.click()
        end_task_time = datetime.now()
        avg_task_time.append(end_task_time - start_task_time)
        task_timer = str((end_task_time - start_task_time).
                         total_seconds())[:-4]
        task_timer = "waited "+task_timer+" seconds"

        # Keeps count of total checks in project
        if "mandatory" in task_type:
            man_total += total_temp
            man_earned += earned_temp
        else:
            adv_total += total_temp
            adv_earned += earned_temp
        if earned_temp != total_temp:
            if "advanced" in task_type:
                sys.stdout.write("\033[F" * (new_line_count + 2))
                print("| " + task_name + (" " * (max_width - len(task_name) -
                      len(task_type) - len(task_timer) - 6)) + task_timer +
                      "  \033[5;30;45m" + task_type.upper() + "\033[0m |")
            else:
                sys.stdout.write("\033[F" * (new_line_count + 2))
                print("| " + task_name + (" " * (max_width - len(task_name) -
                      len(task_type) - len(task_timer) - 6)) + task_timer +
                      "  " +
                      task_type.upper() + " |")
            sys.stdout.write("\033[E" * (new_line_count + 2))
            print("**Missing {:d}**".format(total_temp - earned_temp))

        # If results did not load
        elif results_loaded is False:
            sys.stdout.write("\033[F" * (new_line_count + 3))
            print("-" * max_width)
            notice = "    \033[5;30;44mCHECKER TOOK TOO LONG\033[0m"
            if "advanced" in task_type:
                print("| " + task_name + notice + (" " * (max_width -
                      len(task_name) - len(task_type) - len(notice) +
                      14 - 4)) + "\033[5;30;45m" + task_type.upper() +
                      "\033[0m |")
            else:
                print("| " + task_name + notice + (" " * (max_width -
                      len(task_name) - len(task_type) - len(notice) +
                      14 - 4)) + task_type.upper() + " |")
            print("-" * max_width)
            show_score = False
        # Assume every check is correct
        else:
            sys.stdout.write("\033[F" * (new_line_count + 3))
            print("-" * max_width)
            if "advanced" in task_type:
                print("| \033[5;30;42m" + task_name + "\033[0m" +
                      (" " * (max_width - len(task_name) - len(task_type) -
                       4)) + "\033[5;30;45m" + task_type.upper() + "\033[0m |")
            else:
                print("| \033[5;30;42m" + task_name + "\033[0m" +
                      (" " * (max_width - len(task_name) - len(task_type) -
                       4)) + task_type.upper() + " |")
            print("-" * max_width)

        # Wait until task has closed
        wait.until(EC.invisibility_of_element(close_button))
        count += 1

    # Checked every task at this point

    # Print out results
    if str(commit_id).isdigit():
        commit_id = "Not Found"
    print('\n\n')
    if show_score is False:
        print("\033[5;30;44mSCORES ARE NOT COMPLETE, CHECK ONLINE FOR\
              COMPLETE SCORE\033[0m")
    print("Mandatory: {}/{}".format(man_earned, man_total))
    print("Advanced: {}/{}".format(adv_earned, adv_total))
    print("Total: {:d}/{:d}".format(man_earned + adv_earned,
                                    man_total + adv_total))
    print("Used commit id: " + commit_id)
# There are no check_code_buttons
elif len(check_code_button) == 0:
    print("=============================")
    print("Checker is not out yet silly.")
    print("=============================")
else:
    print("This script is unable to run this project.")
end_time = datetime.now()
check_tests_time = end_time - before_tests_time
runtime = end_time - start_time


print("This script ran in {} seconds. Took {}s to login, {}s to check the re"
      "sults".format(str(runtime.total_seconds())[:-4],
                     str(login_time.total_seconds())[:-4],
                     str(check_tests_time.total_seconds())[:-4]
                     ))
print()
