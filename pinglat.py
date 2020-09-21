import platform
import subprocess
"""
PingLat by @ThumbSec
Loop through a list of IPs and labels then record the actual ping results to a CSV.
Parse the data file to get whatever statistics you need.
Example usage: Ping key LAN devices like Wireless Access Points and then out to the world to help pinpoint latency issues. 
Set up cron on Scheduled Task to run it as frequently as you like.
"""

current_os = platform.system().lower() # Get current OS from platform

# Host and IP arrays. Replace with external file input or edit as needed.
hosts = ("WAP", "gateway", "google")
ips = ("172.27.x.x", "172.27.x.y", "8.8.8.8")
##############################################

data_file = open("pinglatstore.csv", "a") # Open and prepare data file for append write.

for host, ip in zip(hosts, ips): # Combine arrays using Python zip and loop through each. Then check current_os to determine which ping command to use.
    if current_os == "windows":
        param = "-n"
        response = subprocess.getoutput(f'ping {param} 1 {ip}') # .getoutput actually returns the output of the command instead of a boolean.
    else:
        param = "-c"
        response = subprocess.getoutput('ping {} 1 {} | grep ttl'.format(param, ip))

    data_file.write('\n{},{}'.format(host,response)) # write ping output for each IP labeled with your "hostname" to CSV. 

data_file.close()
