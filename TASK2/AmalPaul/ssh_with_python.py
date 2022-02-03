import openpyxl
import subprocess

credential_path = "./credentials.xlsx"
key_path = "./Christ_SRE_Token.pem"
folder_name = "amalPaul"
hosts = []

# 1) Read the credentials spreadsheet
credentials_workbook = openpyxl.load_workbook(credential_path)
credentials_sheet = credentials_workbook.active

# 2) Parse the credentials
for row in credentials_sheet.iter_rows(min_row=2, max_col=3):
    if row[0].value:     
        hosts.append({"username":row[0].value, "host":row[1].value, "port":str(int(row[2].value))})
    else:
        break

# 3) Connect to the server using ssh (Read how to create SSH connection via Python)
subprocess.run(["chmod", "400", key_path])
# 4) Create a folder with your name in Camel Case
for host in hosts:
    subprocess.run(["ssh", "-p", host["port"], '-i', key_path,f'{host["username"]}@{host["host"]}', "mkdir", folder_name])
    print("SSH Done and created folder on " + host["host"])
# 5) Copy over this python program that is running from your machine and store it in the your folder on the remote machine
for host in hosts:
    subprocess.run(["scp", "-r", "-P", host["port"], "-i", key_path, "ssh_with_python.py", f'{host["username"]}@{host["host"]}:{folder_name}'])
    print(f"Successfully copied the program to { host['host'] }")

