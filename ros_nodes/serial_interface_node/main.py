import rospy
import sys
import std_msgs.msg as ros_std_msgs
import lib.serial_driver as serial_driver
import json

import lib.ros as ros_man
import lib.settings as set_man


# module config
_NODE_NAME = 'serial_interface_node'

# module state
_sensors_pub: rospy.Publisher = None
_cmd_sub: rospy.Subscriber = None
_settings_obj: dict = None


def _joystick_cmd_read_handler(msg: ros_std_msgs.String):
    # out_serial_packet = f"0000,0000,0000,0000,{msg.data}"
    serial_driver.write_raw(msg.data)


def ros_node_setup():
    global _sensors_pub
    global _settings_obj
    global _cmd_sub

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _cmd_sub = rospy.Subscriber(
        '/joystick_node/cmd', ros_std_msgs.String, _joystick_cmd_read_handler)

    serial_driver.init_driver()
    _settings_obj = set_man.get_settings()

    topic_id = ros_man.create_topic_id('sensors')
    q_size: int = _settings_obj['ros']['msg_queue_size']

    _sensors_pub = rospy.Publisher(
        topic_id, ros_std_msgs.String, queue_size=q_size)


# def ros_node_loop():
#     # read data from serial port
#     serial_input = serial_driver.read_raw()

#     if serial_input != '':
#         # ACCX:ACCY:ACCZ:COIL
#         # 0000,0000,0000,0---
#         packet_parts = serial_input.split(',')
#         if len(packet_parts) != 4:
#             return

#         acc_x = int(packet_parts[0])
#         acc_y = int(packet_parts[1])
#         acc_z = int(packet_parts[2])
#         coil = int(packet_parts[3])

#         # publish serial data in ROS
#         _sensors_pub.publish(json.dumps({
#             'acc_x': acc_x,
#             'acc_y': acc_y,
#             'acc_z': acc_z,
#             'coil': coil,
#         }))


def ros_node_loop():
    serial_input = serial_driver.read_raw()

    if serial_input != '':
        acc_x = 0
        acc_y = 0
        acc_z = 0
        coil = int(serial_input)

        # publish serial data in ROS
        _sensors_pub.publish(json.dumps({
            'acc_x': acc_x,
            'acc_y': acc_y,
            'acc_z': acc_z,
            'coil': coil,
        }))
