import requests
import subprocess
import sys
import time

red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
white = '\033[97m'
reset = '\033[0m'

BEFORE = f"{red}[{reset}"
BEFORE_GREEN = f"{green}[{reset}"
INPUT = f"{yellow}>{reset}"

def get_ip():
    try:
        return requests.get("https://api.ipify.org", timeout=5).text.strip()
    except:
        return None

def release_renew_ip():
    try:
        subprocess.run(["ipconfig", "/release"], capture_output=True)
        time.sleep(2)
        subprocess.run(["ipconfig", "/renew"], capture_output=True)
        return True
    except Exception as e:
        print(f"{BEFORE} {red}Error: {e}{reset}")
        return False

def flush_dns():
    subprocess.run(["ipconfig", "/flushdns"], capture_output=True)

print(f"\n{BEFORE_GREEN} {green}IP Changer{reset}\n")

old_ip = get_ip()
print(f"{BEFORE} {yellow}Current IP: {white}{old_ip}{reset}\n")

try:
    count = int(input(f"{BEFORE} {INPUT} How many times to rotate IP? (1-10) -> {reset}").strip())
    if count < 1: count = 1
    if count > 10: count = 10
except:
    count = 1

for i in range(count):
    print(f"\n{BEFORE} {yellow}Attempt {i+1}/{count} - Releasing and renewing IP...{reset}")
    release_renew_ip()
    flush_dns()
    time.sleep(3)
    new_ip = get_ip()
    if new_ip and new_ip != old_ip:
        print(f"{BEFORE_GREEN} {green}IP changed! {white}{old_ip}{green} -> {white}{new_ip}{reset}")
        old_ip = new_ip
        break
    elif new_ip == old_ip:
        print(f"{BEFORE} {yellow}IP same ({new_ip}), trying again...{reset}")
    else:
        print(f"{BEFORE} {yellow}Could not verify IP, trying again...{reset}")

final_ip = get_ip()
if final_ip:
    print(f"\n{BEFORE_GREEN} {green}Final IP: {white}{final_ip}{reset}")
    if final_ip != old_ip:
        print(f"{BEFORE_GREEN} {green}IP successfully changed!{reset}")
    else:
        print(f"{BEFORE} {yellow}IP did not change - your ISP may use static IP.{reset}")
        print(f"{BEFORE} {yellow}Try turning off your router for 5 minutes.{reset}")

input("\nPress Enter to exit...")
