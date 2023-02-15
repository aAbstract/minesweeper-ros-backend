# autopep8: off
import time
import rospy
import sys
import os

sys.path.append(os.getcwd())

# change this
import ros_nodes.camera_adapter_node.main as camera_adapter_node
# autopep8: on


# change this
_NODE_DELAY = 0.05  # 50ms delay / operation frequency 20Hz


if __name__ == '__main__':
    # change this
    camera_adapter_node.ros_node_setup()

    while True:
        if rospy.is_shutdown():
            break

        try:
            # change this
            camera_adapter_node.ros_node_loop()

        except rospy.ROSInterruptException:
            break

        time.sleep(_NODE_DELAY)
