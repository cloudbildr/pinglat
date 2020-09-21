import platform
import subprocess
import re
"""
PingLat by @ThumbSec
Loop through a list of IPs and labels then record the actual ping results to a CSV.
Parse the data file to get whatever statistics you need.
Example usage: Ping key LAN devices like Wireless Access Points and then out to the world to help 
pinpoint latency issues. 
Set up cron on Scheduled Task to run it as frequently as you like.
"""

current_os = platform.system().lower()  # Get current OS from platform

# Host and IP arrays. Replace with external file input or edit as needed.
hosts = ("WAP", "IOT_DEVICE", "GOOGLE")
ips = ("172.27.X.X", "172.27.X.X", "8.8.8.8")
##############################################

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

    data_file.write(
        '\n{},{}'.format(host, response))

data_file.close()
