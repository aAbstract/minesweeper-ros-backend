import rospy
import std_msgs.msg as ros_std_msgs
import sys
import cv2
import pickle
import base64

import lib.ros as ros_man
import lib.settings as set_man


# module config
_NODE_NAME = 'camera_adapter_node'

# module state
_camera_adapter = cv2.VideoCapture(0)
_cam_feed_pub: rospy.Publisher = None
_settings_obj: dict = None


def ros_node_setup():
    global _cam_feed_pub
    global _settings_obj

    is_init = ros_man.init_node(_NODE_NAME)

    if not is_init:
        sys.exit()

    _settings_obj = set_man.get_settings()

    topic_id = ros_man.create_topic_id('camera_feed')
    q_size: int = _settings_obj['ros']['msg_queue_size']

    _cam_feed_pub = rospy.Publisher(
        topic_id, ros_std_msgs.String, queue_size=q_size)


def ros_node_loop():
    # read frame
    cap_success, frame = _camera_adapter.read()
    if not cap_success:
        return
    frame = cv2.resize(frame, (400, 400))

    # compress frame
    _, compressed_frame = cv2.imencode(
        '.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])

    # convert frame to binary data
    bin_frame = pickle.dumps(compressed_frame, pickle.HIGHEST_PROTOCOL)

    # base64 encode frame
    encoded_bin_frame = base64.b64encode(bin_frame).decode()

    # publish frame in ROS
    _cam_feed_pub.publish(encoded_bin_frame)
