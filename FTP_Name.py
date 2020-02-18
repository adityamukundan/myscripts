import paramiko
from paramiko_expect import SSHClientInteraction
import re
import string
import warnings
import cryptography
from cryptography import utils

def ftp_link_name():
    try:
        version =  input('Please input the version number:')
        time = 2
        while time > 1:
            imagetype = input(" 1.HW_CH_ODS \n 2.HW_CH_ODS-DPDK \n 3.HW_CH_ODS-FIPS \n 4.HW_CH_ODS-QAT \n Please Enter the type of image :\n")
            if imagetype == '1':
                type = 'HW_CH_ODS'
                break
            elif imagetype == '2':
                type = 'HW_CH_ODS-DPDK'
                break
            elif imagetype == '3':
                type = 'HW_CH_ODS-FIPS'
                break
            elif imagetype == '4':
                type = 'HW_CH_ODS-QAT'
                break
            else:
                print("please input a valid choice")
                continue
        build_number = input('Please enter the build number or press 1 for last successful build \n')
        if build_number == '1':
            build_rls = 'lastSuccessfulBuild'
        else:
            build_rls = build_number
        SSH_ADDRESS = "10.229.10.10"
        SSH_USERNAME = "reluser"
        SSH_PASSWORD = "qwerty1!"
        ## CODE BELOW ##
        warnings.simplefilter("ignore", cryptography.utils.DeprecatedIn23)
        ssh = paramiko.SSHClient()
        ssh.load_system_host_keys()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(SSH_ADDRESS, username=SSH_USERNAME, password=SSH_PASSWORD, look_for_keys=False)
        stdin, stdout, stderr = ssh.exec_command("cd alteonGIT \n cd cheetah \n cd " + version + " \n cd "+build_rls+" \n cd " +type+ " \n cd NDEBUG \n ls")
        build = stdout.readlines()
        actual_build = build[2]
        actual_path = "alteonGIT/cheetah/" + version + "/"+build_rls+"/" +type+ "/NDEBUG/"+actual_build
        actual_path = actual_path.strip()
        print(actual_path)
        return actual_path
    except paramiko.ssh_exception.AuthenticationException as msg:
        print('please enter valid user name ')
    except paramiko.ssh_exception.NoValidConnectionsError as msg:
        print('no connections')