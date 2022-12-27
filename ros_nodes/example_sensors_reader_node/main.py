import rospy
import std_msgs.msg as ros_std_msgs
import sys

import lib.ros as ros_util
import lib.settings as settings_util


# module config
_MODULE_ID = 'ros_nodes.example_sensors_reader_node.main'
_NODE_NAME = 'example_sensors_reader_node'

# module state
_settings_obj: dict = None


# ros msgs handlers
def _example_ros_msg_handler(msg: ros_std_msgs.String):
    print(f"example_sensors_topic: {msg.data}")


def ros_node_setup():
    global _settings_obj

    is_init = ros_util.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = settings_util.get_settings()

    topic_id = ros_util.compute_topic_id(
        'example_sensors_node', 'example_sensors_topic')

    rospy.Subscriber(topic_id, ros_std_msgs.String, _example_ros_msg_handler)


def ros_node_loop():
    pass
