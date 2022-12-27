# autopep8: off
import os
import sys

sys.path.append(os.getcwd())

import lib.settings as settings_util
# autopep8: on


settings_obj = settings_util.get_settings()
main_cu_ip = settings_obj['networking']['main_cu']
main_cu_ssh_username = settings_obj['security']['main_cu']['username']
main_cu_ssh_pass = settings_obj['security']['main_cu']['password']

cmd = f'sshpass -p "{main_cu_ssh_pass}" ssh -t {main_cu_ssh_username}@{main_cu_ip} "docker exec -it z_ros_aquila-ros-1 /bin/bash"'
os.system(cmd)
