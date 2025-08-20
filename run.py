import subprocess
import requests
import time
import shutil
import os

PORT = 8080

print("[+] Starting PHP server on port", PORT, "...")

# kill old php processes (if any)
subprocess.Popen(["pkill", "-f", "php"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

# start php server
php_proc = subprocess.Popen(["php", "-S", f"0.0.0.0:{PORT}"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

time.sleep(2)

print("[+] Starting ngrok tunnel...")

# check if ./ngrok exists, otherwise use system ngrok
ngrok_path = "./ngrok" if os.path.isfile("./ngrok") else "ngrok"

try:
    ngrok_proc = subprocess.Popen([ngrok_path, "http", str(PORT)], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    time.sleep(5)

    # get public url
    try:
        tunnel_url = requests.get("http://127.0.0.1:4040/api/tunnels").json()['tunnels'][0]['public_url']
        print("[+] Public URL:", tunnel_url)
    except Exception as e:
        print("[-] Could not fetch public URL, check ngrok installation.", e)

    print("[*] Press CTRL+C to stop servers.")

    # keep running
    php_proc.wait()
    ngrok_proc.wait()

except FileNotFoundError:
    print("[-] ngrok not found! Please install ngrok and put it in this folder or install globally.")
