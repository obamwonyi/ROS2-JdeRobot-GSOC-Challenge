cmake_minimum_required(VERSION 3.8)
project(introduction_to_ros2)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

# find dependencies
find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)        # Add ROS2 C++ client library
find_package(std_msgs REQUIRED)      # Add standard messages package
find_package(gazebo REQUIRED)
find_package(robot_state_publisher REQUIRED)
find_package(turtlebot3_description REQUIRED)
# Removed the find_package(launch_ros REQUIRED) line

add_executable(introduction_to_ros2 src/introduction_to_ros2.cpp)
target_include_directories(introduction_to_ros2 PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:include/${PROJECT_NAME}>)
target_compile_features(introduction_to_ros2 PUBLIC c_std_99 cxx_std_17)

# Link ROS2 dependencies
ament_target_dependencies(introduction_to_ros2
        rclcpp
        std_msgs
)

install(TARGETS introduction_to_ros2
        DESTINATION lib/${PROJECT_NAME})

# Install launch files
install(DIRECTORY launch
        DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY
        launch
        rviz
        DESTINATION share/${PROJECT_NAME}/
)

## Install RViz configuration files
#install(DIRECTORY rviz
#        DESTINATION share/${PROJECT_NAME}
#)

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  set(ament_cmake_copyright_FOUND TRUE)
  set(ament_cmake_cpplint_FOUND TRUE)
  ament_lint_auto_find_test_dependencies()
endif()

ament_package()