from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from pynput.keyboard import Controller, Key
import time
import numpy as np
import sys

#Choose whether the play wants to play online or on practice
online_or_practice = sys.argv[1]
# username = sys.argv[2]
# password = sys.argv[3]

driver = webdriver.Firefox()
link = 'https://play.typeracer.com/'
driver.get(link)

keyboard = Controller()

#Wait until practice mode or online mode is available
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'gwt-Anchor')))

#Entering practice mode
keyboard.press(Key.ctrl_l)
keyboard.press(Key.alt)
if online_or_practice == 'practice':
    keyboard.press('o')
else:
    keyboard.press('l')
keyboard.release(Key.ctrl_l)
keyboard.release(Key.alt)
if online_or_practice == 'practice':
    keyboard.release('o')
else:
    keyboard.release('l')

#Making sure online players have been found
if online_or_practice == 'online':
    #A sign up page might pop up when trying to access online, Choose a guest nickname is chosen
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'popupContent')))
    if (driver.find_element_by_class_name('popupContent').is_displayed()):
        popup = driver.find_element_by_class_name('popupContent')
        guest_nickname_choose = driver.find_elements_by_css_selector('.gwt-DisclosurePanel.gwt-DisclosurePanel-closed')[2].click()
        guest_nickname = driver.find_elements_by_class_name('gwt-TextBox')[2]
        guest_nickname.send_keys('Tedibaba')
        test = driver.find_elements_by_css_selector('.gwt-Button')[2].click()
        
    ''' 
    This is supposed to work but i guess typeracer has a bug
    keyboard.press(Key.ctrl_l)
    keyboard.press(Key.alt)
    keyboard.press('i')
    keyboard.release(Key.ctrl_l)
    keyboard.release(Key.alt)
    keyboard.release('i')
    '''
    driver.find_elements_by_css_selector('.gwt-Anchor')[3].click()

    #Watching the count down
    time.sleep(3)
    online_mode_page_source = driver.page_source
    starting = False
    while not starting:
        online_soup = BeautifulSoup(online_mode_page_source, features='html5lib')
        ready_message = online_soup.find('div', attrs={'class', 'lightLabel'}).get_text()
        if ready_message == 'Go!' or "It's the final countdown!":
            starting = True
    
    seconds = np.Infinity
    while seconds != 0:
        page = BeautifulSoup(driver.page_source, features='html5lib')
        timer = page.findAll('span', attrs={'class': 'time'})[1].get_text().split(':')[1]
        seconds = int(timer)
        print(timer)
    

#finding input box and making sure text has been loaded
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, 'txtInput')))
input_box = driver.find_element_by_class_name('txtInput')

#Finding text
page_source = driver.page_source
soup = BeautifulSoup(page_source, features='html5lib')
textbox = soup.find('table', attrs={'class': 'inputPanel'})
text = textbox.find('div').get_text()
print(text)

#Coverting the text into single letters and spaces so the computer can type them
letters = list(text)
time.sleep(1)
for char in letters:
    input_box.send_keys(char)
    time.sleep(0.005)

#If a authentication comes up
challenge_input = input('Enter the challenge text: ')
time.sleep(5)
challenge_textbox = driver.find_element_by_class_name('challengeTextArea')
challenge_textbox.send_keys(challenge_input)
