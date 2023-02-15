# autopep8: off
import os
import sys

sys.path.append(os.getcwd())

import lib.log as log_man
import lib.settings as set_man
# autopep8: on


MODULE_ID = 'upload_main_cu_code'

settings_obj = set_man.get_settings()
main_cu_ip = settings_obj['networking']['main_cu']


# check if raspi is online
log_man.print_log(MODULE_ID, 'DEBUG',
                   f"checking control unit machine with ip: {main_cu_ip}")
proc_exit_code = os.system(f"ping -4 -c 1 {main_cu_ip}")

if proc_exit_code != 0:
    log_man.print_log(MODULE_ID, 'ERROR', f"main_cu / ip:{main_cu_ip} is offline")
    sys.exit()

log_man.print_log(MODULE_ID, 'DEBUG', f"main_cu / ip:{main_cu_ip} is online")

# upload ros codebase
log_man.print_log(MODULE_ID, 'DEBUG', "uploading ROS codebase")

main_cu_ssh_username = settings_obj['security']['main_cu']['username']
main_cu_ssh_pass = settings_obj['security']['main_cu']['password']

os.system(
    f'sshpass -p "{main_cu_ssh_pass}" ssh {main_cu_ssh_username}@{main_cu_ip} "rm -r ~/z_ros_aquila/ros"')
os.system(
    f'sshpass -p "{main_cu_ssh_pass}" rsync -a --progress ../ros {main_cu_ssh_username}@{main_cu_ip}:~/z_ros_aquila/')

log_man.print_log(MODULE_ID, 'DEBUG', "done uploading ROS codebase")
