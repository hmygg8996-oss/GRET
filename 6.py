import winreg
import uuid
import ctypes
import sys

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

def get_current_hwid():
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography", 0, winreg.KEY_READ)
        val, _ = winreg.QueryValueEx(key, "MachineGuid")
        winreg.CloseKey(key)
        return val
    except Exception as e:
        return f"Error: {e}"

def set_machine_guid(new_guid):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"SOFTWARE\Microsoft\Cryptography", 0,
            winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY)
        winreg.SetValueEx(key, "MachineGuid", 0, winreg.REG_SZ, new_guid)
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"{BEFORE} {red}Error: {e}{reset}")
        return False

def set_hw_profile_guid(new_guid):
    try:
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE,
            r"SYSTEM\CurrentControlSet\Control\IDConfigDB\Hardware Profiles\0001",
            0, winreg.KEY_WRITE)
        winreg.SetValueEx(key, "HwProfileGuid", 0, winreg.REG_SZ, f"{{{new_guid}}}")
        winreg.CloseKey(key)
        return True
    except Exception as e:
        print(f"{BEFORE} {red}HwProfileGuid Error: {e}{reset}")
        return False

if not is_admin():
    print(f"{BEFORE} {red}Run as Administrator!{reset}")
    input("Press Enter to exit...")
    sys.exit(1)

print(f"\n{BEFORE_GREEN} {green}HWID Changer{reset}\n")

current = get_current_hwid()
print(f"{BEFORE} {yellow}Current HWID: {white}{current}{reset}\n")

print(f"{BEFORE} {yellow}Mode:{reset}")
print(f"  {white}(1) Random new HWID{reset}")
print(f"  {white}(2) Custom HWID{reset}")
mode = input(f"{BEFORE} {INPUT} Choose (1/2) -> {reset}").strip()

if mode == "1":
    new_guid = str(uuid.uuid4())
elif mode == "2":
    new_guid = input(f"{BEFORE} {INPUT} Enter HWID (xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx) -> {reset}").strip()
    try:
        uuid.UUID(new_guid)
    except ValueError:
        print(f"{BEFORE} {red}Invalid GUID format{reset}")
        input("Press Enter to exit...")
        sys.exit(1)
else:
    print(f"{BEFORE} {red}Invalid choice{reset}")
    input("Press Enter to exit...")
    sys.exit(1)

print(f"\n{BEFORE} {yellow}New HWID: {white}{new_guid}{reset}")
confirm = input(f"{BEFORE} {INPUT} Confirm? (y/n) -> {reset}").strip().lower()

if confirm not in ["y", "yes"]:
    print(f"{BEFORE} {yellow}Cancelled{reset}")
    input("Press Enter to exit...")
    sys.exit(0)

ok1 = set_machine_guid(new_guid)
ok2 = set_hw_profile_guid(new_guid)

if ok1:
    print(f"{BEFORE_GREEN} {green}MachineGuid changed successfully!{reset}")
if ok2:
    print(f"{BEFORE_GREEN} {green}HwProfileGuid changed successfully!{reset}")

print(f"\n{BEFORE_GREEN} {green}Done! Restart your PC to apply changes.{reset}\n")
input("Press Enter to exit...")
