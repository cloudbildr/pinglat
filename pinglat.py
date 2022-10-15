import platform
import subprocess
import re
import datetime

"""
PingLat by @CloudBildr

Loop through a list of IPs and labels then record the actual ping results to a CSV. Parse the data file to get whatever
statistics you need. Example usage: Ping key LAN devices like Wireless Access Points and then out to the world to help
narrow focus on latency issues. Set up cron or Scheduled Task to run it as frequently as you like.

Example output to pinglatstore.csv (Linux ping: 

WAP,64 bytes from 172.27.X.X: icmp_seq=1 ttl=64 time=5.68 ms,2020-09-23 21:26:24.372455

"""

current_os = platform.system().lower()  # Get current OS from platform

# Host and IP arrays. Replace with external file input or edit as needed.
hosts = ("WAP", "IOT_DEVICE", "GOOGLE")
ips = ("172.27.x.x", "172.27.x.x", "8.8.8.8")
#####################################################

data_file = open("pinglatstore.csv", "a")

for host, ip in zip(hosts, ips):
    if current_os == "windows":
        param = "-n"
        response = subprocess.getoutput(f'ping {param} 1 {ip}')
        response = re.search(r'(.*?Reply.*?)\n', response)
        response = response.group(1)
    else:
        param = "-c"
        response = subprocess.getoutput('ping {} 1 {} | grep ttl'.format(param, ip))

    time = datetime.datetime.now()
    data_file.write('{},{},{}\n'.format(host, response, time))

data_file.close()
