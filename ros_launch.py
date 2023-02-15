import os
import sys
import subprocess
import time
import re

import lib.log as log_man
import lib.settings as set_man


MODULE_ID = 'ros_launch'

settings_obj = set_man.get_settings()

# validate network configs
network_config: dict[str, str] = settings_obj['networking']

log_man.print_log(MODULE_ID, 'INFO', 'checking network configs')

for machine_name, machine_ip in network_config.items():
    if machine_ip in ['', '127.0.0.1']:
        continue

    log_man.print_log(MODULE_ID, 'DEBUG',
                       f"checking host {machine_name} with IP {machine_ip}")

    proc_exit_code = os.system(f"ping -4 -c 1 {machine_ip}")

    if proc_exit_code != 0:
        log_man.print_log(
            MODULE_ID, 'ERROR', f"host {machine_name} with IP {machine_ip} is offline")
        sys.exit()

log_man.print_log(MODULE_ID, 'INFO',
                   'finished scanning machines, all machines are online')

# start ros master node
log_man.print_log(MODULE_ID, 'INFO', 'starting ROS master node')
os.system('docker compose up -d')
# wait until ros master boots up
time.sleep(2)
log_man.print_log(MODULE_ID, 'INFO', 'finished starting ROS master node')

# start slave ros nodes
log_man.print_log(MODULE_ID, 'INFO', 'starting slave ROS nodes')

ros_nodes_map: dict = settings_obj['ros']['nodes']
nodes_to_check: list[str] = ['/rosout']

for machine_name in ros_nodes_map.keys():
    # skip manual machines
    if machine_name in settings_obj['ros']['ignore_machines']:
        continue

    machine_ip = settings_obj['networking'][machine_name]
    machine_ssh_username = settings_obj['security'][machine_name]['username']
    machine_ssh_password = settings_obj['security'][machine_name]['password']

    for node_name in ros_nodes_map[machine_name]:
        # skip ignored nodes
        if node_name in settings_obj['ros']['ignore_nodes']:
            continue

        log_man.print_log(
            MODULE_ID, 'INFO', f"starting nodes: ({machine_name}|{machine_ip}).{node_name}")

        nodes_to_check.append(f"/{node_name}")

        launch_cmd = f'sshpass -p "{machine_ssh_password}" ssh -f {machine_ssh_username}@{machine_ip} "cd ~/z_ros_aquila/ros && (python3 ./ros_nodes/{node_name}/bootstrap.py > /dev/null 2>&1 &) && exit"'
        os.system(launch_cmd)
        time.sleep(1)

log_man.print_log(MODULE_ID, 'INFO', 'done starting slave ROS nodes')

# ros launch validation
log_man.print_log(MODULE_ID, 'INFO', 'starting ROS validation routine')

main_cu_ip = settings_obj['networking']['main_cu']
main_cu_ssh_username = settings_obj['security']['main_cu']['username']
main_cu_ssh_pass = settings_obj['security']['main_cu']['password']
validation_cmd = f'sshpass -p "{main_cu_ssh_pass}" ssh {main_cu_ssh_username}@{main_cu_ip} "docker exec z_ros_aquila-ros-1 /bin/bash -c \\"source /ros_entrypoint.sh && rosnode list\\""'

sub_process = subprocess.Popen(
    validation_cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
stdout, _ = sub_process.communicate()
output = stdout.decode()
active_nodes_list = output.split()

# format active nodes
try:
    for i in range(len(active_nodes_list)):
        if active_nodes_list[i] == '/rosout':
            continue

        active_nodes_list[i] = re.findall(
            '\/[a-z_]+', active_nodes_list[i])[0][:-1]

except:
    log_man.print_log(MODULE_ID, 'ERROR',
                       f"error reading active ROS nodes: {output}")

if set(nodes_to_check) == set(active_nodes_list):
    log_man.print_log(MODULE_ID, 'INFO', 'ROS validation routine succeed')

else:
    log_man.print_log(MODULE_ID, 'ERROR', 'ROS validation routine faild')
    print('nodes_to_check:')
    print(nodes_to_check)
    print('active_nodes')
    print(active_nodes_list)
