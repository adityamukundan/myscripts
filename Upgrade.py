import paramiko
import paramiko_expect
from paramiko_expect import SSHClientInteraction
import codecs
import sys
import time
import re
import subprocess
import socket
import errno
import FTP_Name

def connection_ssh():
    SSH_ADDRESS = "10.76.7.18"
    SSH_USERNAME = "admin"
    SSH_PASSWORD = "admin"
    ## CODE BELOW ##
    ssh = paramiko.SSHClient()
    ssh.load_system_host_keys()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD, look_for_keys=False)
    interact = SSHClientInteraction(ssh, display=True)
    a = interact.expect(['.*seeing.*', '.*#.*'])
    if a == 0:
        interact.send('y')
        interact.expect('.*#.*')
    else:
        interact.send('\n')
        interact.expect('.*#.*')
    return interact


try:
    link = FTP_Name.ftp_link_name()
    vx_slot = input('Please enter the VX slot number(1-4):')
    vadc    = input('Please enter vADC slot number(1-10):')
    interact = connection_ssh()
    interact.send('\n')
    interact.expect('.*#.*')
    time.sleep(3)
    interact.send("\n")
    interact.expect('.*#.*')
    interact.send('/i/sys/mgmt')
    interact.expect('.*System#.*')
    interact.send('/boot/gtimg -m')
    interact.expect('.*Enter.*')
    interact.send('all')
    interact.expect('.*Enter.*')
    # VX Slot
    interact.send(vx_slot)
    interact.expect('.*Enter.*')
    # Vadc Slot
    interact.send(vadc)
    interact.expect('.*Enter.*')
    # FTP server IP
    interact.send('10.229.10.10')
    interact.expect('.*Enter.*')
    # FTP download link
    interact.send(link)
    time.sleep(5)
    interact.expect('.*Enter.*')
    # FTP username
    interact.send('reluser')
    interact.expect('.*Enter.*')
    # FTP password
    interact.send('qwerty1!')
    interact.expect('.*Enter.*')
    interact.send('\n')
    interact.expect('.*download.*')
    interact.send('y')
    time.sleep(20)
    interact.expect('.*')
    j = 2
    while j > 1:
        time.sleep(20)
        z=interact.expect(['>>.*','.*Enter.*','.+'],timeout=9000)
        v = interact.current_output_clean
        if z == 0:
            interact.send('\n')
            interact.expect('.*Boot.*')
            break
        if z == 1:
            time.sleep(10)
            v1 = re.search(r'\((\d+)',v)
            mac_address = re.findall(r'\w+:\w+:\w+:\w+:\w+:\w+:*', v)
            mac_address = str(mac_address[0])
            size_actual = v1.group(1)
            empty_space = '  '
            location_gen = t = "D:\Random Files\pw2.exea"
            total = location_gen + empty_space + mac_address + empty_space + size_actual
            version_password = subprocess.Popen(total, stdout=subprocess.PIPE).communicate()
            actual_password = str(version_password[0])
            find_password = re.findall(r'\w{8}',actual_password)
            interact.send(find_password[3])
            time.sleep(10)
            continue
    interact.send('\n')
    interact.expect('.*Options.*')
    interact.send('/boot/image')
    interact.expect('.*type.*')
    interact.send('adc')
    time.sleep(3)
    interact.expect('.*vADC.*')
    # Vadc  for image upgrade
    interact.send('3')
    interact.expect('.*Enter.*')
    # Image to which device should be upgraded
    interact.send(vadc)
    interact.expect('.*wish.*')
    interact.send('\n')
    time.sleep(3)
    interact.expect('.*Options.*')
    interact.send('/boot/image')
    interact.expect('.*type.*')
    interact.send('vx')
    time.sleep(4)
    interact.expect('.*Enter.*')
    # vx image . This image must be of same/lesser version than that of vadc.
    interact.send(vx_slot)
    time.sleep(5)
    interact.expect('.*function.*')
    interact.send('y')
    time.sleep(3)
    question = interact.expect(['.*analysis.*','.*restart.*'])
    if question == 0:
        interact.send('\n')
        time.sleep(2)
        interact.expect('.*restart.*')
        interact.send('y')
    else:
        interact.send('y')
        time.sleep(2)
    time.sleep(3)
    reboot_device = interact.expect(['.*Operation.*','.*reset.*'])
    if reboot_device == 0:
        interact.send('y')
        time.sleep(2)
        interact.expect('.*reset.*')
        interact.send('y')
    else:
        interact.send('y')
    time.sleep(25)
    interact.send('\n')
except socket.error as error_msg:
    print('device is rebooting please wait while the device comes up ')
    wait = 2
    while wait > 1:
        try:
            interact = connection_ssh()
            interact.send('/boot/cur')
            interact.expect('.*Options.*')
            print('\n upgrade process is complete')
            break
        except:
            continue
print('thanks for running the script')