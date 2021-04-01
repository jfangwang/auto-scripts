sudo apt-get update

if ! command -v pip &> /dev/null
then
    echo "==============="
    echo "Installing pip3"
    echo "==============="
    sudo apt-get -y install python3-pip
fi

if ! command -v google-chrome-stable &> /dev/null
then
    echo "=============================="
    echo "Installing Java, Chrome-stable"
    echo "=============================="
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
    sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
    sudo apt-get install google-chrome-stable
    sudo apt-get -y install openjdk-7-jre google-chrome-stable xvfb unzip firefox
fi

if ! command -v selenium &> /dev/null
then
    echo "==================="
    echo "Installing Selenium"
    echo "==================="
    sudo pip3 install selenium
    SELENIUM_VERSION=$(curl "https://selenium-release.storage.googleapis.com/" | perl -n -e'/.*<Key>([^>]+selenium-server-standalone[^<]+)/ && print $1')
    wget "https://selenium-release.storage.googleapis.com/${SELENIUM_VERSION}" -O selenium-server-standalone.jar
    chown vagrant:vagrant selenium-server-standalone.jar
    sudo mv selenium-server-standalone.jar /usr/local/bin
fi
echo "------------------------"
echo "Installing Chrome Driver"
echo "------------------------"
rm chromedriver
CHROMEDRIVER_VERSION=$(curl "http://chromedriver.storage.googleapis.com/LATEST_RELEASE")
wget "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo rm chromedriver_linux64.zip
chown vagrant:vagrant chromedriver
sudo cp chromedriver /usr/local/bin

export DISPLAY=:10
sudo pip3 install --upgrade --ignore-installed urllib3
echo "============================================="
echo "You're good to go. Just run the main.py file."
echo "============================================="
