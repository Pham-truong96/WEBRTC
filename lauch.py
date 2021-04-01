import time, os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from contants import *
from internet_mock import *

class ChromeSetUp:
    def __init__(self, bandwidth, client):
        self.LOG_PATH = LOG_PATH +"/"+ bandwidth
        self.USERNAME = client
        if not os.path.exists(self.LOG_PATH):
            os.makedirs(self.LOG_PATH)

        opt = Options()
        opt.add_argument("--disable-infobars")
        opt.add_argument("start-maximized")
        opt.add_argument("--disable-extensions")
        opt.add_argument('--headless')
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
        

    def join_jitsi_room(self, username):
        # Optional argument, if not specified will search path.
        self.driver.get(ROOM_URL)
        time.sleep(5) # Let the user actually see something!
        search_box = self.driver.find_element_by_class_name('field')
        search_box.send_keys(username)
        time.sleep(5)
        search_box.send_keys(Keys.ENTER)
        time.sleep(15)
        print("join room")

    def save_log(self,):
        # driver.send_keys(Keys.CONTROL + 't')
        self.driver.execute_script("window.open('https://www.google.com');")

        time.sleep(5)
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.driver.get("chrome://webrtc-internals/")
        time.sleep(5)
        self.driver.find_elements_by_tag_name('summary')[0].click()
        time.sleep(2*60)
        self.driver.find_elements_by_tag_name('button')[0].click()
        print("save log")

    def __del__(self,):
        print("complete")
        
def main():
    net_moc = TCNetem()
    for bandwidth in bandwidths:
        net_moc.set_bandwidth_limit(bandwidth)
        chrome = ChromeSetUp(bandwidth, "client1").get_browser()
        lauch = Lauch(chrome)
        lauch.join_jitsi_room(username="client1")
        time.sleep(30)
        lauch.save_log()
        time.sleep(5)
        chrome.quit()
        time.sleep(5)
        net_moc.reset()
if __name__  == "__main__":
    main()
