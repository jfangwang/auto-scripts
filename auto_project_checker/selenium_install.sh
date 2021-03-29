echo "-------------------"
echo "Installing Selenium"
echo "-------------------"
sudo pip3 install selenium

# apt-get update
sudo apt-get update
echo "------------------------------"
echo "Installing Java, Chrome-stable"
echo "------------------------------"
sudo apt-get -y install openjdk-7-jre google-chrome-stable xvfb unzip firefox
