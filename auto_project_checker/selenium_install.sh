echo "-------------------"
echo "Installing Selenium"
echo "-------------------"
sudo apt-get update
sudo apt-get -y install python3-pip
sudo pip3 install selenium

echo "------------------------------"
echo "Installing Java, Chrome-stable"
echo "------------------------------"
wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
sudo apt-get update 
sudo apt-get install google-chrome-stable
sudo apt-get -y install openjdk-7-jre google-chrome-stable xvfb unzip firefox
echo "-------------------"
echo "Installing Selenium"
echo "-------------------"
SELENIUM_VERSION=$(curl "https://selenium-release.storage.googleapis.com/" | perl -n -e'/.*<Key>([^>]+selenium-server-standalone[^<]+)/ && print $1')
wget "https://selenium-release.storage.googleapis.com/${SELENIUM_VERSION}" -O selenium-server-standalone.jar
chown vagrant:vagrant selenium-server-standalone.jar
sudo mv selenium-server-standalone.jar /usr/local/bin
echo "------------------------"
echo "Installing Chrome Driver"
echo "------------------------"
CHROMEDRIVER_VERSION=$(curl "http://chromedriver.storage.googleapis.com/LATEST_RELEASE")
wget "http://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
sudo rm chromedriver_linux64.zip
chown vagrant:vagrant chromedriver
sudo mv chromedriver /usr/local/bin
export DISPLAY=:10

sudo pip3 install --upgrade --ignore-installed urllib3
