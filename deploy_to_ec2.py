import paramiko
import sys
import os
import base64

host = "13.233.225.252"
username = "ubuntu"

# 1. Grab the Base64 key straight from GitHub's memory
b64_key = os.environ.get("B64_KEY")

if not b64_key:
    print("CRITICAL ERROR: The GitHub Secret 'EC2_SSH_KEY' is empty!")
    sys.exit(1)

print("Reconstructing key file via Python...")
try:
    # Python acts like a vacuum, sucking out any accidental spaces or newlines
    b64_key = b64_key.replace(" ", "").replace("\n", "").replace("\r", "")
    
    # Decode it flawlessly into proper Linux format
    decoded_key = base64.b64decode(b64_key).decode('utf-8')
    
    # Python safely writes the perfect file
    with open("sanu.pem", "w") as f:
        f.write(decoded_key)
        
    print("Key successfully reconstructed!")
except Exception as e:
    print(f"Failed to decode key: {e}")
    sys.exit(1)

# 2. Execute SSH Connection
print("Connecting to EC2...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(
        host,
        username=username,
        key_filename="sanu.pem"
    )
    print("Connected successfully! Running app.py...")
    
    # Execute your AWS command
    stdin, stdout, stderr = ssh.exec_command("python3 app.py")
    
    print(stdout.read().decode())
    if stderr:
        print("ERRORS:", stderr.read().decode())
        
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    ssh.close()
