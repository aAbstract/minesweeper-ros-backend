import rospy
import std_msgs.msg as ros_std_msgs
import sys
import pygame

import lib.ros as ros_man
import lib.settings as set_man


# module config
_NODE_NAME = 'joystick_node'
_BTNS_MAP = {
    # buttons
    0: '1',
    1: '2',
    2: '3',
    3: '4',
    4: 'LT',
    5: 'RT',
    6: 'LB',
    7: 'RB',
    # arrows
    (0, 1): 'W',
    (1, 0): 'D',
    (0, -1): 'S',
    (-1, 0): 'A',
    (0, 0): 'X',
    (1, 1): 'D',
    (1, -1): 'S',
    (-1, -1): 'S',
    (-1, 1): 'A',
}

# module state
_settings_obj: dict = None
_joystick_handler: pygame.joystick.Joystick = None
_la_pub: rospy.Publisher = None
_ra_pub: rospy.Publisher = None
_cmd_pub: rospy.Publisher = None


def ros_node_setup():
    global _settings_obj
    global _joystick_handler
    global _la_pub
    global _ra_pub
    global _cmd_pub

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = set_man.get_settings()
    q_size: int = _settings_obj['ros']['msg_queue_size']

    la_topic_id = ros_man.create_topic_id('left_analog')
    ra_topic_id = ros_man.create_topic_id('right_analog')
    cmd_topic_id = ros_man.create_topic_id('cmd')

    _la_pub = rospy.Publisher(
        la_topic_id, ros_std_msgs.String, queue_size=q_size)
    _ra_pub = rospy.Publisher(
        ra_topic_id, ros_std_msgs.String, queue_size=q_size)
    _cmd_pub = rospy.Publisher(
        cmd_topic_id, ros_std_msgs.String, queue_size=q_size)

    pygame.init()
    pygame.joystick.init()
    _joystick_handler = pygame.joystick.Joystick(0)


def ros_node_loop():
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            _cmd_pub.publish(_BTNS_MAP[event.button])

        elif event.type == pygame.JOYHATMOTION:
            _cmd_pub.publish(_BTNS_MAP[event.value])

        elif event.type == pygame.JOYAXISMOTION:
            lax = 0
            lay = 0
            rax = 0
            ray = 0

            if event.axis == 0:
                lax = event.value

            elif event.axis == 1:
                lay = -event.value

            elif event.axis == 2:
                ray = -event.value

            elif event.axis == 3:
                rax = event.value

            _la_pub.publish(f"{lax},{lay}")
            _ra_pub.publish(f"{rax},{ray}")
