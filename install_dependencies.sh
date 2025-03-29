#!/bin/bash

# Update package lists
sudo apt update

# Install TurtleBot4 packages
sudo apt install -y ros-jazzy-turtlebot4-desktop
sudo apt install -y ros-jazzy-turtlebot4-msgs
sudo apt install -y ros-jazzy-turtlebot4-navigation
sudo apt install -y ros-jazzy-turtlebot4-simulator

# Install dependencies for visualization
sudo apt install -y ros-jazzy-rviz2
sudo apt install -y ros-jazzy-nav2-rviz-plugins

echo "TurtleBot4 packages installed successfully!"