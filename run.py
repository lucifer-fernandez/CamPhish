import os, subprocess, time

PORT = 8080
print(f"[+] Starting PHP server on port {PORT}...")
php_proc = subprocess.Popen(['php','-S',f'0.0.0.0:{PORT}','-t','.'])
time.sleep(2)
print("[+] Starting ngrok tunnel...")
ngrok_proc = subprocess.Popen(['./ngrok','http',str(PORT)])
time.sleep(5)
print("[+] Server and ngrok running.")
print("[*] Press CTRL+C to stop.")

try:
    php_proc.wait()
except KeyboardInterrupt:
    print("[*] Stopping server...")
    php_proc.terminate()
    ngrok_proc.terminate()
