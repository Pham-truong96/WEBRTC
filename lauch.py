import time, os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

from contants import *
from internet_mock import *

class ChromeSetUp:
    def __init__(self, bandwidth, client):
        self.LOG_PATH = "/home/webrtc/apprtc-logs/"
        self.USERNAME = client
        if not os.path.exists(self.LOG_PATH):
            os.makedirs(self.LOG_PATH)

        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--headless') # not open windows
        opt.add_argument('--disable-gpu')
        opt.add_argument("--allow-file-access-from-files") #allows getUserMedia() to be called from file:// URLs.
        opt.add_argument("disable-translate") #disables Translate into .. Popup
        opt.add_argument("use-fake-ui-for-media-stream") #avoids the need to grant camera/microphone permissions
        opt.add_argument("use-fake-device-for-media-stream") #feeds a test pattern to getUserMedia() instead of live camera input.
        opt.add_argument("use-file-for-fake-video-capture="+FAKE_FILE) #feeds a Y4M test file to getUserMedia() instead of live camera input
        opt.add_argument("enable-logging --v=1 --vmodule=*source*/talk/*=3") #some logging parameters
        opt.add_argument("mute-audio") #disables sound
        opt.add_argument("--no-sandbox") #
        opt.add_argument("--disable-dev-shm-usage") #
        opt.add_experimental_option('prefs', {'download.default_directory' : self.LOG_PATH}) # set path save log


        self.driver = webdriver.Chrome(
            options = opt,
            executable_path = DRIVER_PATH
        )
        self.driver.set_window_size(1280, 1024)

    def get_browser(self,):
        return self.driver

    def __del__(self,):
        # self.driver.quit()
        print("quit chrome")


class Lauch:
    def __init__(self, driver):
        self.driver = driver
        print("start")
        print("open chrome")

    def dumps_log(self,):
        self.driver.get("chrome://webrtc-internals/")
        self.driver.find_elements_by_tag_name('summary')[0].click()
        time.sleep(2)
        select = Select(self.driver.find_element_by_id('statsSelectElement'))
        select.select_by_value('Legacy Non-Standard (callback-based) getStats() API')


    def join_jitsi_room(self, username):
        # Optional argument, if not specified will search path.
        body = self.driver.find_element_by_tag_name("body")
        time.sleep(1)
        # body.send_keys(Keys.CONTROL + 't')
        self.driver.execute_script("window.open('');")
        time.sleep(1)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get(ROOM_URL)
        time.sleep(5) # Let the user actually see something!
        search_box = self.driver.find_element_by_class_name('field')
        search_box.send_keys(username)
        time.sleep(5)
        search_box.send_keys(Keys.ENTER)
        time.sleep(15)
        print("join room")
    
    def save_log(self,):
        # body = self.driver.find_element_by_tag_name("body")
        # body.send_keys(Keys.CONTROL + '\t')
        self.driver.switch_to.window(self.driver.window_handles[0])
        
        time.sleep(90)
        self.driver.find_elements_by_tag_name('button')[0].click()
        time.sleep(10)
        print("save log")

    def __del__(self,):
        print("complete")
        
def main():
    net_moc = TCNetem()
    chrome = ChromeSetUp("eooe", "client1").get_browser()
    lauch = Lauch(chrome)
    lauch.dumps_log()
    time.sleep(1)
    lauch.join_jitsi_room(username="client1")
    time.sleep(90)
    lauch.save_log()
    chrome.quit()
    net_moc.reset()
if __name__  == "__main__":
    print("start")
    main()
