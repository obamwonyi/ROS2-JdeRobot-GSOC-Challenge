#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import PoseStamped
from nav2_simple_commander.robot_navigator import BasicNavigator
import time
import math
from tf_transformations import quaternion_from_euler

class WaypointNavigation(Node):
    def __init__(self):
        super().__init__('waypoint_navigation')
        self.navigator = BasicNavigator()
        self.navigator.waitUntilNav2Active()
        self.get_logger().info("Nav2 is active, starting navigation...")

        # Define waypoints as (x, y, yaw_radians)
        self.waypoints = [
            (0.0, 2.0, 0.0),       # First waypoint
            (0.0, 2.0, 1.57),      # Same position, but rotate 90 degrees
            (-2.0, 2.0, 1.57)      # Move to new position
        ]

        goal_poses = []
        for wp in self.waypoints:
            # Create goal pose
            goal = PoseStamped()
            goal.header.frame_id = "map"
            goal.header.stamp = self.navigator.get_clock().now().to_msg()

            # Set position
            goal.pose.position.x = wp[0]
            goal.pose.position.y = wp[1]
            goal.pose.position.z = 0.0

            # Convert yaw to quaternion properly
            q = quaternion_from_euler(0, 0, wp[2])
            goal.pose.orientation.x = q[0]
            goal.pose.orientation.y = q[1]
            goal.pose.orientation.z = q[2]
            goal.pose.orientation.w = q[3]

            goal_poses.append(goal)
            self.get_logger().info(f"Added waypoint: x={wp[0]}, y={wp[1]}, yaw={wp[2]}")

        # Start waypoint navigation
        self.navigator.followWaypoints(goal_poses)
        self.get_logger().info("Waypoint navigation started")

        # Monitor progress
        i = 0
        while not self.navigator.isTaskComplete():
            i += 1
            feedback = self.navigator.getFeedback()
            if feedback and feedback.current_waypoint != -1:
                current = feedback.current_waypoint + 1
                total = len(self.waypoints)
                self.get_logger().info(f"Moving to waypoint {current}/{total}")

            # Only log every 5 seconds to reduce spam
            if i % 5 == 0:
                self.get_logger().info("Navigation in progress...")
            time.sleep(1)

        # Check result
        result = self.navigator.getResult()
        if result == BasicNavigator.TaskResult.SUCCEEDED:
            self.get_logger().info("Navigation completed successfully!")
        else:
            self.get_logger().info(f"Navigation failed with status: {result}")

def main(args=None):
    rclpy.init(args=args)
    node = WaypointNavigation()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()