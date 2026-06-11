import paramiko

# Spaces removed
host = "13.233.225.252"

username = "ubuntu"

# Changed to match the GitHub Actions pipeline output
key = "sanu.pem"

ssh = paramiko.SSHClient()

ssh.set_missing_host_key_policy(
    paramiko.AutoAddPolicy()
)

ssh.connect(
    host,
    username=username,
    key_filename=key
)

# Remember: If your code isn't on the server yet, 
# you'll need to add a git pull command here eventually!
stdin, stdout, stderr = ssh.exec_command(
    "python3 app.py"
)

print(stdout.read().decode())
if stderr:
    print("ERRORS:", stderr.read().decode())

ssh.close()
