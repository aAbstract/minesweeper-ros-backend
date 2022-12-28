import rospy
import std_msgs.msg as ros_std_msgs
import sys
import cv2
import pickle
import base64

import lib.ros as ros_util
import lib.settings as settings_util


# module config
_NODE_NAME = 'example_camera_adapter_node'

# module state
_camera_adapter = cv2.VideoCapture(0)
_temp_pub: rospy.Publisher = None
_settings_obj: dict = None


def ros_node_setup():
    global _temp_pub
    global _settings_obj

    is_init = ros_util.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = settings_util.get_settings()

    topic_id = ros_util.create_topic_id('camera_feed')
    q_size: int = _settings_obj['ros']['msg_queue_size']

    _temp_pub = rospy.Publisher(
        topic_id, ros_std_msgs.String, queue_size=q_size)


def ros_node_loop():
    # read frame
    _, frame = _camera_adapter.read()
    frame = cv2.resize(frame, (500, 500))

    # compress frame
    _, compressed_frame = cv2.imencode(
        '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # convert frame to binary data
    bin_frame = pickle.dumps(compressed_frame, pickle.HIGHEST_PROTOCOL)

    # base64 encode frame
    encoded_bin_frame = base64.b64encode(bin_frame).decode()

    # publish frame in ROS
    _temp_pub.publish(encoded_bin_frame)
