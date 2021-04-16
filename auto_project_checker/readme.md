![Image of auto proj](https://i.imgur.com/WZNODKC.png)
# Welcome to Auto Project Checker
## What is this?
This is a python selenium script to check the results of the checker. Instead of hitting the 'check code' button for every task, you just run this script once and that's it. This project was primarily built for vagrant running on ```ubuntu 16.04 LTS distro``` but could also run on PC with VSCode after installing everything manually.
## Setup
This project is in a directory ```auto_project_checker``` which is part of the repo ```auto-scripts```.
### Setup for Vagrant running Ubuntu

1. Clone the repo: ```git clone https://github.com/jfangwang/auto-scripts.git```
2. cd into auto-scripts repo: ```cd auto-scripts/auto_project_checker```
3. Everything is bundled in ```selenium_install.sh``` to keep things simple. For installation, run the file by entering in ```./selenium_install.sh``` into terminal. Enter 'y' when prompted and will take a couple minutes.

## Usage
### First run
After installation, run ```./main.py```. You will be prompted to enter in your username and password which will be saved to ```holberton_login.txt```. From here you can just run ```./main.py``` without re-entering your credentials or project number/URL.

![Image of prompt](https://i.imgur.com/CK9VBQQ.png)

### How do I run it?
Just run ```./main.py``` to run it normally. It will skip tasks that have been marked as done by the checker to reduce time.
### How do I switch projects?
```./main.py [PROJECT]``` where ```[PROJECT]``` represents a url or project number.
Example: ```./main.py 212``` or ```./main.py https://intranet.hbtn.io/projects/212```
The script will save the new project url and will not need the extra argument again.
### Want to check every task just in case
Run ```./main.py -e``` to make sure you got every task right. ```-e``` is a flag notifying the script to check the results of every task in the project. 

### Common Commands

* ```./main.py -e 212``` or ```./main.py 212 -e``` : Check every task in the 0x00. C - Hello, World project.
* ```./main.py``` : Check the results of whatever project url is saved in holberton_login.txt. If no project url exists, it will prompt you to enter one in.
* ```./main.py https://intranet.hbtn.io/projects/209``` or ```./main.py 209``` : Check the results of the project "0x03. Shell, init files, variables and expansions"
## Contributing
Feel free to make a pull request, raise any git issues and will be updated accordingly.

## Files

| File          | Description   |
| ------------- |:-------------:|
| checker.py    | Checks the checker with selenium     |
| chromedriver      | chromedriver for linux     |
| chromedriver.exe      | chromedriver for windows     |
| holberton_login.txt      | A newly created file after running ```./main.py``` storing credentials and project URL|
| main.py     | checks holberton_login.txt for login    |
| selenium_install.sh      | Installs all required packages for this project   |

## Author
Jonny Wang from Cohort 13
