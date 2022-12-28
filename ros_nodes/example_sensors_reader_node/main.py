import rospy
import std_msgs.msg as ros_std_msgs
import sys

import lib.ros as ros_util


# module config
_NODE_NAME = 'example_sensors_reader_node'


# ros msgs handlers
def _example_ros_msg_handler(msg: ros_std_msgs.String):
    print(f"example_sensors_topic: {msg.data}")


def ros_node_setup():
    is_init = ros_util.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    topic_id = ros_util.compute_topic_id(
        'example_sensors_node', 'example_sensors_topic')

    rospy.Subscriber(topic_id, ros_std_msgs.String, _example_ros_msg_handler)


def ros_node_loop():
    pass
