# autopep8: off
import time
import rospy
import sys
import os

sys.path.append(os.getcwd())

# change this
import ros_nodes.example_camera_adapter_node.main as example_camera_adapter_node
# autopep8: on


# change this
_NODE_DELAY = 0.01  # 10ms delay / operation frequency 100Hz


if __name__ == '__main__':
    # change this
    example_camera_adapter_node.ros_node_setup()

    while True:
        if rospy.is_shutdown():
            break

        try:
            # change this
            example_camera_adapter_node.ros_node_loop()

        except rospy.ROSInterruptException:
            break

        time.sleep(_NODE_DELAY)
