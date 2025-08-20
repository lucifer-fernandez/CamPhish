import subprocess
import requests
import time
import os
import signal
import sys

PORT = 8080

print("[+] Cleaning old processes...")
subprocess.Popen(["pkill", "-f", "php"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
subprocess.Popen(["pkill", "-f", "ngrok"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
time.sleep(1)

print("[+] Starting PHP server on port", PORT, "...")

# start php server (show error if fails)
try:
    php_proc = subprocess.Popen(
        ["php", "-S", f"0.0.0.0:{PORT}"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
except FileNotFoundError:
    print("[-] PHP is not installed! Install with: pkg install php -y")
    sys.exit(1)

time.sleep(2)

# check if PHP really started
try:
    r = requests.get(f"http://127.0.0.1:{PORT}", timeout=3)
    print("[+] PHP server running OK!")
except Exception as e:
    print("[-] PHP server failed to start! Is PHP installed?")
    php_proc.terminate()
    sys.exit(1)

print("[+] Starting ngrok tunnel...")

# check if ./ngrok exists, otherwise use system ngrok
ngrok_path = "./ngrok" if os.path.isfile("./ngrok") else "ngrok"

try:
    ngrok_proc = subprocess.Popen(
        [ngrok_path, "http", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.STDOUT
    )
except FileNotFoundError:
    print("[-] Ngrok not installed or not found in PATH!")
    php_proc.terminate()
    sys.exit(1)

time.sleep(5)

# get public url
try:
    tunnel_url = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
    print("[+] Public URL:", tunnel_url)
except Exception as e:
    print("[-] Could not fetch public URL, check ngrok installation.", e)
    php_proc.terminate()
    ngrok_proc.terminate()
    sys.exit(1)

print("[*] Press CTRL+C to stop servers.")

# keep running until CTRL+C
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n[!] Server stopped. Cleaning up...")

    php_proc.terminate()
    ngrok_proc.terminate()

    # make sure they are killed
    try:
        php_proc.wait(timeout=2)
    except:
        php_proc.kill()

    try:
        ngrok_proc.wait(timeout=2)
    except:
        ngrok_proc.kill()

    print("[+] Cleanup complete. Goodbye!")
