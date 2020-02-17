import paramiko
import paramiko_expect
from paramiko_expect import SSHClientInteraction
import codecs
import sys
import time
import re
import subprocess


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
interact = connection_ssh()
interact.expect('.*#.*')
time.sleep(3)
interact.send("\n")
interact.send('/i/sys/mgmt')
interact.expect('.*System#.*')