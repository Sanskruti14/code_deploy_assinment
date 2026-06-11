import paramiko
import sys

host = "13.233.225.252"
username = "ubuntu"
key = "sanu.pem"

# --- 1. DEBUG CHECK: Verify the file formatting ---
try:
    with open(key, 'r') as f:
        content = f.read()
        lines = content.split('\n')
        print(f"--- KEY FORMAT DEBUG ---")
        print(f"Total lines in key file: {len(lines)}")
        print(f"Starts with: {lines[0]}")
        print(f"------------------------")
        
        if len(lines) < 5:
            print("CRITICAL ERROR: Key file lost its line breaks. It is one giant string.")
            sys.exit(1) # Stop the script before Paramiko crashes
except Exception as e:
    print(f"Could not read key file: {e}")

# --- 2. EXECUTE SSH CONNECTION ---
print("Connecting to EC2...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

ssh.connect(
    host,
    username=username,
    key_filename=key
)

print("Connected successfully! Running app.py...")
stdin, stdout, stderr = ssh.exec_command("python3 app.py")

print(stdout.read().decode())
if stderr:
    print("ERRORS:", stderr.read().decode())

ssh.close()
