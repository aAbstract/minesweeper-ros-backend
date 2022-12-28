import rospy
import std_msgs.msg as ros_std_msgs
import sys
import cv2
import base64
import pickle

import lib.ros as ros_util


# module config
_NODE_NAME = 'example_camera_reader_node'


# ros msgs handlers
def _example_ros_frame_reader(msg: ros_std_msgs.String):
    input_bin_stream = msg.data.encode()

    # base64 decode
    decoded_bin_frame = base64.b64decode(input_bin_stream)

    # recover frame from binary stream
    frame = pickle.loads(decoded_bin_frame)

    # decode JPEG frame
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cv2.imshow('CAM_1', frame)
    cv2.waitKey(1)


def ros_node_setup():
    is_init = ros_util.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    topic_id = ros_util.compute_topic_id(
        'example_camera_adapter_node', 'camera_feed')

    rospy.Subscriber(topic_id, ros_std_msgs.String, _example_ros_frame_reader)


def ros_node_loop():
    pass
