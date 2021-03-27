import time, os, sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys

from contants import *

LOG_PATH = LOG_PATH +"/"+ sys.argv[1]
USERNAME = sys.argv[2]
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

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
opt.add_experimental_option('prefs', {'download.default_directory' : LOG_PATH}) # set path save log


driver = webdriver.Chrome(
    options = opt,
    executable_path = DRIVER_PATH
)
driver.set_window_size(1280, 1024)


class Lauch:
    def __init__(self, ):
        print("start")
        print("open chrome")
        

    def join_jitsi_room(self, ):
        # Optional argument, if not specified will search path.
        driver.get(ROOM_URL)
        time.sleep(5) # Let the user actually see something!
        search_box = driver.find_element_by_class_name('field')
        search_box.send_keys(USERNAME)
        time.sleep(5)
        search_box.send_keys(Keys.ENTER)
        time.sleep(30)
        print("join room")

    def save_log(self,):
        # driver.send_keys(Keys.CONTROL + 't')
        driver.execute_script("window.open('https://www.google.com');")

        time.sleep(25)
        driver.switch_to.window(driver.window_handles[-1])
        driver.get("chrome://webrtc-internals/")
        time.sleep(15)
        driver.find_elements_by_tag_name('summary')[0].click()
        time.sleep(5)
        driver.find_elements_by_tag_name('button')[0].click()
        print("save log")

    def __del__(self,):
        print("complete")
        driver.quit()


# class TCNetem:
#     def __init__(self,bw):
#         os.system('echo \"1\" | sudo -S pkill java')
#         os.system('echo \"1\" | sudo pkill chromium')
#         os.system('echo \"1\" | sudo pkill chromedriver')
#         self.set_bandwidth_limit(bandwidth=bw)
    
#     def set_bandwidth_limit(self,):
#         pass

#     def reset(self,):
#         os.system('sudo tc qdisc del dev eth0 root')
lauch = Lauch()
lauch.join_jitsi_room()
#set limit
# netem = TCNetem(bw)

time.sleep(20)

lauch.save_log()
time.sleep(50)
driver.quit()
# netem.reset()