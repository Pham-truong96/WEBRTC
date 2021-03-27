

import os, time, paramiko, shutil

HOME_DIR = "/home/controller"
ips = [
    "",
    "",
    ""
]
bandwidths = [0.25, 0.5, 1, 2, 3, 4, 5, 15, 30, 50]


class Cotroller:
    def __init__(self,):
        for ip in ips:
            if not os.path.exists("{0}/webrtc-logs/{1}/".format(HOME_DIR, ip)):
                os.makedirs("{0}/webrtc-logs/{1}/".format(HOME_DIR, ip))
    
    