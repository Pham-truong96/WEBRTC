import os, time, paramiko, shutil

# Path to your ssh id
HOME_DIR = "/home/control"

# Client IPs
ips = [
    #"YOUR_IP_HERE"
    "10.128.0.2",
    "10.128.0.3",
    "10.128.0.4"
]

# Measurement bandwidths
bandwidths = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 1, 2, 3, 4, 5, 15, 30, 50]
# bandwidths = [0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 1]

# Iterations
iterations = 10

# Duration is the actual measurement time. The actual measurement takes around 25 seconds longer (setup + waiting time)
duration = 100

# 
switchBw = False
setBwTime = 0


for bw in bandwidths:
    if not os.path.exists("{0}/webrtc-logs/{1}".format(HOME_DIR, bw)):
        os.makedirs("{0}/webrtc-logs/{1}".format(HOME_DIR, bw))

        if not os.path.exists("{0}/webrtc-logs/bw_{1}".format(HOME_DIR, bw)):
            os.makedirs("{0}/webrtc-logs/bw_{1}".format(HOME_DIR, bw))

        for ip in ips:
            if not os.path.exists("{0}/webrtc-logs/{1}/{2}".format(HOME_DIR, bw, ip)):
                os.makedirs("{0}/webrtc-logs/{1}/{2}".format(HOME_DIR, bw, ip))

            os.system("sshpass -p 1 scp -r -o StrictHostKeyChecking=no client@{0}:/home/webrtc/apprtc-logs/* {1}/webrtc-logs/{2}/{0}/".format(ip, HOME_DIR, bw))

            # os.system("sshpass -p 1 ssh -o StrictHostKeyChecking=no client@{0} 'rm -r /home/webrtc/apprtc-logs/*'".format(ip))

            for folder in os.listdir("{0}/webrtc-logs/{1}/{2}".format(HOME_DIR, bw, ip)):
                if not os.path.isdir("{0}/webrtc-logs/{1}/{2}/{3}".format(HOME_DIR, bw, ip, folder)):
                    continue
                for file in os.listdir("{0}/webrtc-logs/{1}/{2}/{3}".format(HOME_DIR, bw, ip, folder)):
                    l_ip = ""
                    if file.startswith("10."):
                        l_ip = file

                    if os.path.exists("{0}/webrtc-logs/{1}/{2}/{3}/webrtc_internals_dump.txt".format(HOME_Dir, bw, ip, folder)) and l_ip != "":
                        if not os.path.exists("{0}/webrtc-logs/bw_{1}/{2}".format(HOME_DIR, bw, folder)):
                            os.makedirs("{0}/webrtc-logs/bw_{1}/{2}".format(HOME_DIR, bw, folder))
                        
                        # Rename downloaded dump file to webrtclog_ip.log
                        for sttime in [1,2,3,4,5,6,7,8,9,10]:
                            os.rename(
                                "{0}/webrtc-logs/{1}/{2}/{3}/{4}/webrtc_internals_dump.txt".format(HOME_DIR, bw, ip, folder, sttime),
                                "{0}/webrtc-logs/bw_{1}/{2}/webrtclog_{4}_{3}.log".format(HOME_DIR, bw, folder, l_ip, sttime))
                        

        shutil.rmtree("{0}/webrtc-logs/{1}".format(HOME_DIR, bw))