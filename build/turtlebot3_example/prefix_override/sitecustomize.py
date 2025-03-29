import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/netweaver/Projects/GSOC/JdeRobot/ros2_challenge_ws/install/turtlebot3_example'
