![Image of auto proj](https://i.imgur.com/WZNODKC.png)
# Welcome to Auto Project Checker
## What is this?
This is a python selenium script to check the results of the checker. Instead of hitting the 'check code' button for every task, you just run this script once and that's it. This project was initially built for vagrant running on ```ubuntu 16.04 LTS distro``` but also works on PC.
## Set up
Everything is bundled in ```selenium_install.sh``` to keep things simple. For installation, run the file by entering in ```./selenium_install.sh``` into terminal. Enter 'y' when prompted and will take a couple minutes.

## Usage
### First run:
After installation, run ```./main.py```. You will be prompted to enter in your username and password which will be saved to ```holberton_login.txt```. From here you can just run ```./main.py``` without re-entering your credentials or project number/URL.

![Image of prompt](https://i.imgur.com/CK9VBQQ.png)
### Switching Project number or URL
```./main.py [PROJECT]``` where ```[PROJECT]``` represents a url or project number.
Example: ```./main.py 212``` or ```./main.py https://intranet.hbtn.io/projects/212```

## Contributing
Feel free to make a pull request or raise any git issues and will be updated accordingly.

## Files

| File          | Description   |
| ------------- |:-------------:|
| checker.py    | Checks the checker with selenium     |
| chromedriver      | chromedriver for linux     |
| chromedriver.exe      | chromedriver for windows     |
| main.py     | checks holberton_login.txt for login    |
| selenium_install.sh      | Installs all required packages for this project   |

## Author
Jonny Wang
