# Minecraft "Installer" 💀

**⚠️ Disclaimer: This project is for educational and demonstrational purposes only. It simulates the behavior of ransomware but is intended for controlled environments. Do not use this on any system without explicit permission. The creators are not responsible for any misuse.**

Welcome to the most exciting Minecraft installer you'll ever run! Get ready for a... _transformative_ experience. This project demonstrates a Python-based client that interacts with a Next.js backend.

## Features

- **Realistic Installation:** A convincing fake Minecraft installer interface to provide an authentic user experience.
- **Persistent Telemetry:** A background thread constantly sends system information (CPU, memory, OS, IP address, etc.) to a telemetry endpoint.
- **"File Archiving":** The script securely "archives" all files in the user's home directory using AES encryption.
- **Victim Reporting:** Sends the encryption key and victim telemetry to a server endpoint upon successful "archiving".
- **Dynamic Wallpaper:** After the "archiving" process, the user's desktop wallpaper is updated to provide important information.
- **Cross-Platform:** The client is designed to be bundled for Windows, macOS, and Linux.

## How It Works

### Client (`public/minecraft-installer.py`)

A Python script that performs several actions in parallel:

1.  **Telemetry:** Runs a background thread to collect and send system information every 30 seconds to `/api/telemetry`.
2.  **Encryption:** Walks the user's home directory (`~`) and encrypts all files (excluding critical directories like `Library` and `.Trash`).
3.  **Reporting:** Sends a payload containing the default password and system telemetry to `/api/victims` after the first file is encrypted and again at the end of the process.
4.  **Wallpaper:** Downloads an image from the server and sets it as the desktop background for the "wow factor".

### Server (Next.js)

A simple Next.js application with API routes to receive data from the client.

- `/api/telemetry`: An endpoint to receive and log system telemetry.
- `/api/victims`: An endpoint to receive and log the encryption key and victim information.

---
