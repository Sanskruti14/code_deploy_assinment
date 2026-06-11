import paramiko
import sys
import os
import base64

host = "13.233.225.252"
username = "ubuntu"

# 1. Grab the Base64 key straight from GitHub's memory
b64_key = os.environ.get("B64_KEY")

if not b64_key:
    print("CRITICAL ERROR: The GitHub Secret 'SSH_PRIVATE_KEY' is empty!")
    sys.exit(1)

try:
    b64_key = b64_key.replace(" ", "").replace("\n", "").replace("\r", "")
    decoded_key = base64.b64decode(b64_key).decode('utf-8')
    with open("sanu.pem", "w") as f:
        f.write(decoded_key)
except Exception as e:
    print(f"Failed to decode key: {e}")
    sys.exit(1)

# 2. Execute SSH Connection AND Deploy Code
print("Connecting to EC2...")
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    ssh.connect(
        host,
        username=username,
        key_filename="sanu.pem"
    )
    print("Connected successfully! Pulling the latest files from GitHub to EC2...")
    
    # --- THIS IS THE NEW MAGIC COMMAND ---
    # It clones your repo if it is missing, pulls the latest code, 
    # lists the files so you can see them, and runs your program!
    deploy_command = """
    if [ ! -d "code_deploy_assinment" ]; then
        git clone https://github.com/Sanskruti14/code_deploy_assinment.git
    fi
    cd code_deploy_assinment
    git pull origin main
    
    echo "--- Files successfully copied to EC2: ---"
    ls -la
    
    echo "--- Running Program ---"
    python3 main.py 
    """
    # Note: If your math program is named app.py instead of main.py, 
    # change the last line above!

    stdin, stdout, stderr = ssh.exec_command(deploy_command)
    
    # Print the output straight from the EC2 server
    print(stdout.read().decode())
    
    err = stderr.read().decode()
    if err:
        print("ERRORS/WARNINGS:", err)
        
except Exception as e:
    print(f"Connection failed: {e}")
finally:
    ssh.close()
