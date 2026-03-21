import subprocess
import winreg
import os
import sys
import ctypes

red = '\033[91m'
green = '\033[92m'
yellow = '\033[93m'
white = '\033[97m'
reset = '\033[0m'

BEFORE = f"{red}[{reset}"
BEFORE_GREEN = f"{green}[{reset}"

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def log_ok(msg): print(f"{BEFORE_GREEN} {green}{msg}{reset}")
def log_err(msg): print(f"{BEFORE} {red}{msg}{reset}")
def log_info(msg): print(f"{BEFORE} {yellow}{msg}{reset}")

def disable_system_proxy():
    try:
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Internet Settings",
            0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "ProxyEnable", 0, winreg.REG_DWORD, 0)
        winreg.SetValueEx(key, "ProxyServer", 0, winreg.REG_SZ, "")
        winreg.SetValueEx(key, "ProxyOverride", 0, winreg.REG_SZ, "")
        winreg.CloseKey(key)
        log_ok("System proxy disabled")
    except Exception as e:
        log_err(f"Proxy registry error: {e}")

def disable_ie_proxy():
    try:
        subprocess.run(["netsh", "winhttp", "reset", "proxy"], capture_output=True)
        log_ok("WinHTTP proxy reset")
    except Exception as e:
        log_err(f"WinHTTP error: {e}")

def kill_vpn_processes():
    vpn_procs = [
        "openvpn.exe", "nordvpn.exe", "expressvpn.exe", "protonvpn.exe",
        "windscribe.exe", "mullvad.exe", "surfshark.exe", "cyberghost.exe",
        "privatevpn.exe", "ipvanish.exe", "hidemyass.exe", "tunnelbear.exe",
        "tor.exe", "torrc.exe", "privoxy.exe", "psiphon.exe", "lantern.exe",
        "hotspotshield.exe", "purevpn.exe", "vyprvpn.exe"
    ]
    killed = 0
    for proc in vpn_procs:
        result = subprocess.run(["taskkill", "/F", "/IM", proc], capture_output=True)
        if result.returncode == 0:
            log_ok(f"Killed: {proc}")
            killed += 1
    if killed == 0:
        log_info("No VPN/proxy processes found running")
    else:
        log_ok(f"Killed {killed} process(es)")

def remove_vpn_adapters():
    try:
        result = subprocess.run(["netsh", "interface", "show", "interface"],
            capture_output=True, text=True)
        vpn_keywords = ["vpn", "tap", "tun", "nordlynx", "proton", "express",
                        "windscribe", "mullvad", "wireguard", "openvpn"]
        for line in result.stdout.splitlines():
            for kw in vpn_keywords:
                if kw.lower() in line.lower():
                    parts = line.split()
                    if len(parts) >= 4:
                        iface = " ".join(parts[3:])
                        # Disable
                        subprocess.run(["netsh", "interface", "set", "interface",
                            iface, "admin=disabled"], capture_output=True)
                        # Uninstall via pnputil
                        subprocess.run(["pnputil", "/remove-device", iface],
                            capture_output=True)
                        log_ok(f"Removed adapter: {iface}")
    except Exception as e:
        log_err(f"Adapter error: {e}")

def reset_dns():
    try:
        # Reset DNS to automatic (DHCP)
        result = subprocess.run(["netsh", "interface", "show", "interface"],
            capture_output=True, text=True)
        for line in result.stdout.splitlines():
            if "Connected" in line or "connected" in line:
                parts = line.split()
                if len(parts) >= 4:
                    iface = " ".join(parts[3:])
                    subprocess.run(["netsh", "interface", "ip", "set", "dns",
                        iface, "dhcp"], capture_output=True)
        log_ok("DNS reset to automatic (DHCP)")
    except Exception as e:
        log_err(f"DNS reset error: {e}")

def clean_hosts_file():
    try:
        hosts = r"C:\Windows\System32\drivers\etc\hosts"
        with open(hosts, "r") as f:
            lines = f.readlines()
        clean = [l for l in lines if not any(kw in l.lower() for kw in
            ["vpn", "proxy", "tor", "nordvpn", "expressvpn", "protonvpn"])]
        with open(hosts, "w") as f:
            f.writelines(clean)
        log_ok("Hosts file cleaned")
    except Exception as e:
        log_err(f"Hosts file error: {e}")

def flush_dns():
    subprocess.run(["ipconfig", "/flushdns"], capture_output=True)
    log_ok("DNS cache flushed")

def reset_winsock():
    subprocess.run(["netsh", "winsock", "reset"], capture_output=True)
    log_ok("Winsock reset")

def reset_tcp():
    subprocess.run(["netsh", "int", "ip", "reset"], capture_output=True)
    log_ok("TCP/IP stack reset")

def delete_tor_folder():
    tor_path = r"C:\Tor"
    if os.path.exists(tor_path):
        subprocess.run(["rmdir", "/s", "/q", tor_path], shell=True, capture_output=True)
        log_ok("Tor folder deleted")
    else:
        log_info("Tor folder not found")

print(f"\n{BEFORE_GREEN} {green}VPN / Proxy Cleaner{reset}\n")

if not is_admin():
    log_err("Run as Administrator for full cleanup!")
    print()

log_info("Starting cleanup...")
print()

log_info("Killing VPN/proxy processes...")
kill_vpn_processes()
print()

log_info("Disabling system proxy...")
disable_system_proxy()
disable_ie_proxy()
print()

log_info("Removing VPN adapters...")
remove_vpn_adapters()
print()

log_info("Resetting DNS to automatic...")
reset_dns()
print()

log_info("Cleaning hosts file...")
clean_hosts_file()
print()

log_info("Flushing DNS...")
flush_dns()
print()

log_info("Resetting Winsock...")
reset_winsock()
print()

log_info("Resetting TCP/IP...")
reset_tcp()
print()

log_info("Deleting Tor folder...")
delete_tor_folder()
print()

log_ok("Cleanup complete! Restart your PC to apply all changes.")
input("\nPress Enter to exit...")
