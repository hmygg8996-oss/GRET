# Copyright (c) RedTiger 
# See the file 'LICENSE' for copying permission
# ----------------------------------------------------------------------------------------------------------------------------------------------------------|
# EN: 
#     - Do not touch or modify the code below. If there is an error, please contact the owner, but under no circumstances should you touch the code.
#     - Do not resell this tool, do not credit it to yours.
# FR: 
#     - Ne pas toucher ni modifier le code ci-dessous. En cas d'erreur, veuillez contacter le propriétaire, mais en aucun cas vous ne devez toucher au code.
#     - Ne revendez pas ce tool, ne le créditez pas au vôtre.

import requests
import json
import random
import concurrent.futures
import subprocess
import sys
import os
from datetime import datetime

# Colors
red = '\033[91m'
green = '\033[92m'
white = '\033[97m'
reset = '\033[0m'

# Webhook settings
username_webhook = "IP Generator"
avatar_webhook = "https://i.imgur.com/4M34hi2.png"
color_webhook = 0xFF0000


BEFORE = f"{red}[{reset}"
AFTER = f"{red}]{reset}"
BEFORE_GREEN = f"{green}[{reset}"
AFTER_GREEN = f"{green}]{reset}"
INPUT = f"{red}>{reset}"
GEN_VALID = f"{green}+{reset}"
GEN_INVALID = f"{red}-{reset}"

def Title(title):
    if sys.platform.startswith("win"):
        os.system(f"title {title}")
    else:
        print(f"\033]0;{title}\007", end='')

Title("Ip Generator")

try:
    mode = input(f"\n{BEFORE} {INPUT} Mode: (1) Random IP / (2) Specific IP -> {reset}")
    
    if mode not in ["1", "2"]:
        print(f"{BEFORE} {red}Error: Please choose 1 or 2{reset}")
        sys.exit(1)
    
    if mode == "2":
        specific_ip = input(f"{BEFORE} {INPUT} Enter IP address -> {reset}")
        # Validate IP format
        parts = specific_ip.split(".")
        if len(parts) != 4 or not all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
            print(f"{BEFORE} {red}Error: Invalid IP format{reset}")
            sys.exit(1)
    
    webhook = input(f"{BEFORE} {INPUT} Webhook ? (y/n) -> {reset}")
    if webhook.lower() in ['y', 'yes']:
        webhook_url = input(f"{BEFORE} {INPUT} Webhook URL -> {reset}")
        try:
            messages_per_ip = int(input(f"{BEFORE} {INPUT} How many messages per valid IP? -> {reset}"))
            if messages_per_ip < 1:
                messages_per_ip = 1
        except ValueError:
            print(f"{BEFORE} {red}Error: Invalid number, using 1{reset}")
            messages_per_ip = 1
    else:
        webhook_url = None
        messages_per_ip = 1

    try:
        threads_number = int(input(f"{BEFORE} {INPUT} Threads Number -> {reset}"))
    except ValueError:
        print(f"{BEFORE} {red}Error: Invalid number{reset}")
        sys.exit(1)

    if mode == "1":
        try:
            total_checks = int(input(f"{BEFORE} {INPUT} How many IPs to check? (0 for unlimited) -> {reset}"))
        except ValueError:
            print(f"{BEFORE} {red}Error: Invalid number{reset}")
            sys.exit(1)
    else:
        total_checks = 1

    def SendWebhook(embed_content):
        if webhook_url:
            payload = {
                'embeds': [embed_content],
                'username': username_webhook,
                'avatar_url': avatar_webhook
            }
            headers = {'Content-Type': 'application/json'}
            try:
                requests.post(webhook_url, data=json.dumps(payload), headers=headers)
            except requests.RequestException as e:
                print(f"{BEFORE} Error sending webhook: {e}{reset}")

    number_valid = 0
    number_invalid = 0
    checks_done = 0

    def IpCheck():
        global number_valid, number_invalid, checks_done

        if mode == "2":
            ip = specific_ip
        else:
            ip = ".".join(str(random.randint(1, 255)) for _ in range(4))

        try:
            if sys.platform.startswith("win"):
                result = subprocess.run(['ping', '-n', '1', ip], capture_output=True, text=True, timeout=2)
            elif sys.platform.startswith("linux"):
                result = subprocess.run(['ping', '-c', '1', '-W', '1', ip], capture_output=True, text=True, timeout=2)
            else:
                print(f"{BEFORE} {red}Error: Unsupported platform{reset}")
                sys.exit(1)

            checks_done += 1

            if result.returncode == 0:
                number_valid += 1
                if webhook_url:
                    embed_content = {
                        'title': 'Ip Valid !',
                        'description': f"**Ip:**\n```{ip}```",
                        'color': color_webhook,
                        'footer': {"text": username_webhook, "icon_url": avatar_webhook}
                    }
                    for _ in range(messages_per_ip):
                        SendWebhook(embed_content)
                print(f"{BEFORE_GREEN} {GEN_VALID} Logs: {white}{number_invalid} invalid - {number_valid} valid{green} Status:  {white}Valid{green}  Ip: {white}{ip}{green}")
            else:
                number_invalid += 1
                print(f"{BEFORE} {GEN_INVALID} Logs: {white}{number_invalid} invalid - {number_valid} valid{red} Status: {white}Invalid{red} Ip: {white}{ip}{red}")
        except Exception:
            number_invalid += 1
            checks_done += 1
            print(f"{BEFORE} {GEN_INVALID} Logs: {white}{number_invalid} invalid - {number_valid} valid{red} Status: {white}Invalid{red} Ip: {white}{ip}{red}")
        Title(f"Ip Generator - Invalid: {number_invalid} - Valid: {number_valid} - Checked: {checks_done}")

    def Request():
        if mode == "2":
            IpCheck()
        else:
            with concurrent.futures.ThreadPoolExecutor(max_workers=threads_number) as executor:
                executor.map(lambda _: IpCheck(), range(threads_number))

    if mode == "2":
        Request()
    else:
        if total_checks == 0:
            while True:
                Request()
        else:
            while checks_done < total_checks:
                remaining = total_checks - checks_done
                batch_size = min(threads_number, remaining)
                with concurrent.futures.ThreadPoolExecutor(max_workers=batch_size) as executor:
                    executor.map(lambda _: IpCheck(), range(batch_size))

            print(f"\n{BEFORE} {green}Finished! Total checked: {checks_done} - Valid: {number_valid} - Invalid: {number_invalid}{reset}")

except KeyboardInterrupt:
    print(f"\n{BEFORE} {red}Stopped by user{reset}")
    sys.exit(0)
except Exception as e:
    print(f"{BEFORE} {red}Error: {e}{reset}")
    sys.exit(1)

