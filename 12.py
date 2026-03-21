import subprocess
import socket
import sys
import ctypes

red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
white = '\033[97m'
reset = '\033[0m'

BEFORE = f"{red}[{reset}"
BEFORE_GREEN = f"{green}[{reset}"
INPUT = f"{yellow}>{reset}"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def get_interfaces():
    result = subprocess.run(["netsh", "interface", "ip", "show", "config"],
        capture_output=True, text=True)
    interfaces = []
    current = None
    for line in result.stdout.splitlines():
        if "Configuration for interface" in line:
            current = line.split('"')[1] if '"' in line else None
        if current and "IP Address" in line and ":" in line:
            ip = line.split(":")[-1].strip()
            if ip and not ip.startswith("0."):
                interfaces.append((current, ip))
    return interfaces

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "Unknown"

def set_static_ip(iface, ip, mask, gateway):
    subprocess.run(["netsh", "interface", "ip", "set", "address",
        iface, "static", ip, mask, gateway], capture_output=True)

def set_dhcp(iface):
    subprocess.run(["netsh", "interface", "ip", "set", "address",
        iface, "dhcp"], capture_output=True)
    subprocess.run(["netsh", "interface", "ip", "set", "dns",
        iface, "dhcp"], capture_output=True)

print(f"\n{BEFORE_GREEN} {green}Local IP Changer{reset}\n")

if not is_admin():
    print(f"{BEFORE} {red}Run as Administrator!{reset}\n")

print(f"{BEFORE} {yellow}Current local IP: {white}{get_local_ip()}{reset}\n")

# Show interfaces
interfaces = get_interfaces()
if not interfaces:
    # fallback
    result = subprocess.run(["ipconfig"], capture_output=True, text=True)
    print(result.stdout)
else:
    print(f"{BEFORE} {yellow}Available interfaces:{reset}")
    for i, (name, ip) in enumerate(interfaces):
        print(f"  {white}[{i+1}] {name} - {ip}{reset}")

print()
iface_name = input(f"{BEFORE} {INPUT} Interface name (e.g. Wi-Fi or Ethernet) -> {reset}").strip()

print(f"\n{BEFORE} {yellow}Mode:{reset}")
print(f"  {white}(1) Set custom IP{reset}")
print(f"  {white}(2) Reset to DHCP (automatic){reset}")
mode = input(f"{BEFORE} {INPUT} Choose (1/2) -> {reset}").strip()

if mode == "1":
    new_ip = input(f"{BEFORE} {INPUT} New IP (e.g. 192.168.1.100) -> {reset}").strip()
    mask = input(f"{BEFORE} {INPUT} Subnet mask (default 255.255.255.0) -> {reset}").strip() or "255.255.255.0"
    gateway = input(f"{BEFORE} {INPUT} Gateway (e.g. 192.168.1.1) -> {reset}").strip()

    print(f"\n{BEFORE} {yellow}Setting IP to {new_ip}...{reset}")
    set_static_ip(iface_name, new_ip, mask, gateway)
    print(f"{BEFORE_GREEN} {green}Done! New local IP: {white}{get_local_ip()}{reset}")

elif mode == "2":
    print(f"\n{BEFORE} {yellow}Resetting to DHCP...{reset}")
    set_dhcp(iface_name)
    import time; time.sleep(3)
    print(f"{BEFORE_GREEN} {green}Done! New local IP: {white}{get_local_ip()}{reset}")

else:
    print(f"{BEFORE} {red}Invalid choice{reset}")

input("\nPress Enter to exit...")
