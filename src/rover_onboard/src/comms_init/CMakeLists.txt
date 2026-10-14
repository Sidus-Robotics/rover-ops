# colcon build --packages-select comms_init
# source install/setup.bash
# ros2 run comms_init web_client_init

cmake_minimum_required(VERSION 3.8)
project(comms_init)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(ixwebsocket REQUIRED)
find_package(rover_interfaces REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(CppLinuxSerial REQUIRED)
find_package(Threads REQUIRED)

# set(SRC_FILES main.cpp serialib.cpp)
# add_executable(your_project_name ${SRC_FILES})

add_executable(web_client_init src/web_client_init.cpp)
add_executable(serial_bridge_init src/serial_bridge_init.cpp)

target_include_directories(web_client_init PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
  "$<INSTALL_INTERFACE:include>"
)

# Dependencies within /opt/ros/jazzy/include
ament_target_dependencies(web_client_init
  rclcpp
  sensor_msgs
  rover_interfaces
  std_msgs
)

target_include_directories(serial_bridge_init PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
  "$<INSTALL_INTERFACE:include>"
)

# Dependencies within /opt/ros/jazzy/include
ament_target_dependencies(serial_bridge_init
  rclcpp
  sensor_msgs
  rover_interfaces
  Threads
  CppLinuxSerial
)

# Other libraries, within /usr/local/include
# Note, it is the second way of linking libraries shown here:
# https://docs.ros.org/en/jazzy/How-To-Guides/Ament-CMake-Documentation.html
# It was the only way it would link through the way I installed it ( in ~/.)
target_link_libraries(web_client_init
  ixwebsocket::ixwebsocket
)

target_link_libraries(serial_bridge_init
  Threads::Threads
  CppLinuxSerial
)

install(
  TARGETS web_client_init
  DESTINATION lib/${PROJECT_NAME}
)

install(
  TARGETS serial_bridge_init
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
