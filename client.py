from lauch import *

bandwidth = "start"
chrome = ChromeSetUp(bandwidth, "client2").get_browser()

lauch = Lauch(chrome)
lauch.join_jitsi_room(username="client2")

