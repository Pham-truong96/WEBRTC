import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


opt = Options()
opt.add_argument("--disable-infobars")
opt.add_argument("start-maximized")
opt.add_argument("--disable-extensions")
# Pass the argument 1 to allow and 2 to block
opt.add_experimental_option("prefs", { \
    "profile.default_content_setting_values.media_stream_mic": 1, 
    "profile.default_content_setting_values.media_stream_camera": 1,
    "profile.default_content_setting_values.geolocation": 1, 
    "profile.default_content_setting_values.notifications": 1 
  })


driver = webdriver.Chrome(chrome_options=opt,  executable_path='C:\\Users\\kienbay\\Desktop\\webrtc_lauch\\chromedriver.exe')  # Optional argument, if not specified will search path.
driver.get('https://meet.jit.si/ArtificialMatchesStretchToo')
time.sleep(5) # Let the user actually see something!
search_box = driver.find_element_by_class_name('field')
search_box.send_keys('234')
# time.sleep(5)
# search_box.submit()
time.sleep(5)
elem = driver.find_element_by_xpath(
    '//div[@id="react"]' + 
    '//div[@id="videoconference_page"]' + 
    '//div[@id="lobby-screen"]' + 
    '//div[@class="content"]' + 
    '//div[@class="prejoin-input-area-container"]' +
    '//div[@class="prejoin-input-area"]' + 
    '//div[@class="prejoin-preview-dropdown-container"]'
    '//div[@class="action-btn  primary "]'
).click()
print("----------------------------")
print(elem)
print("----------------------------")
elem.click()
time.sleep(5) # Let the user actually see something!
driver.quit()