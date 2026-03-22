import platform
import subprocess
import re
import datetime
import os
import sys

"""
PingLat by @CloudBildr

Loop through a list of IPs/hostnames and record ping results. Supports
loading hosts from a file or entering them interactively. Results can be
saved to a CSV or displayed on screen.

File format (one per line):
    LABEL,ip_or_hostname
    ip_or_hostname          (label defaults to the host value)
"""

current_os = platform.system().lower()


def ping_host(ip):
    if current_os == "windows":
        response = subprocess.getoutput(f'ping -n 1 {ip}')
        match = re.search(r'(.*?Reply.*?)\n', response)
        return match.group(1) if match else "No reply"
    else:
        response = subprocess.getoutput(f'ping -c 1 {ip} | grep ttl')
        return response if response else "No reply"


def load_hosts_from_file(path):
    path = path.strip()
    if not os.path.isfile(path):
        print(f"  Error: file not found: {path}")
        return None
    hosts, ips = [], []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            parts = line.split(",", 1)
            if len(parts) == 2:
                hosts.append(parts[0].strip())
                ips.append(parts[1].strip())
            else:
                hosts.append(parts[0].strip())
                ips.append(parts[0].strip())
    return hosts, ips


def get_hosts():
    print("\nHow would you like to provide hosts?")
    print("  1. Path to a text file")
    print("  2. Enter hosts/IPs manually (comma-separated)")
    choice = input("\nChoice [1/2]: ").strip()

    if choice == "1":
        path = input("File path: ").strip()
        result = load_hosts_from_file(path)
        if result is None:
            sys.exit(1)
        return result
    elif choice == "2":
        raw = input("Enter hosts/IPs (comma-separated, e.g. google.com, 8.8.8.8): ")
        entries = [e.strip() for e in raw.split(",") if e.strip()]
        if not entries:
            print("  No hosts entered.")
            sys.exit(1)
        return entries, entries
    else:
        print("  Invalid choice.")
        sys.exit(1)


def get_output_mode():
    print("\nWhat would you like to do with the results?")
    print("  1. Display on screen")
    print("  2. Save to pinglatstore.csv")
    print("  3. Both")
    choice = input("\nChoice [1/2/3]: ").strip()
    return choice


def display_results(results):
    col_label = max(len(r["host"]) for r in results)
    col_response = max(len(r["response"]) for r in results)

    header = f"{'HOST':<{col_label}}  {'RESULT':<{col_response}}  TIMESTAMP"
    print()
    print(header)
    print("-" * len(header))
    for r in results:
        print(f"{r['host']:<{col_label}}  {r['response']:<{col_response}}  {r['time']}")
    print()


def save_results(results):
    with open("pinglatstore.csv", "a") as f:
        for r in results:
            f.write(f"{r['host']},{r['response']},{r['time']}\n")
    print(f"  Results appended to pinglatstore.csv")


def main():
    hosts, ips = get_hosts()
    output_mode = get_output_mode()

    print("\nPinging...")
    results = []
    for host, ip in zip(hosts, ips):
        response = ping_host(ip)
        results.append({"host": host, "response": response, "time": datetime.datetime.now()})

    if output_mode in ("1", "3"):
        display_results(results)

    if output_mode in ("2", "3"):
        save_results(results)


if __name__ == "__main__":
    main()
