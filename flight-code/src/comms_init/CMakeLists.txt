cmake_minimum_required(VERSION 3.8)
project(comms_init)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(ixwebsocket REQUIRED)

add_executable(web_server_init src/web_server_init.cpp)

target_include_directories(web_server_init PUBLIC
  $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
  $<INSTALL_INTERFACE:include>
)

# Dependencies within /opt/ros/jazzy/include
ament_target_dependencies(web_server_init
  rclcpp
  std_msgs
)

# Other libraries, within /usr/local/include 
target_link_libraries(web_server_init
  ixwebsocket::ixwebsocket
)

install(TARGETS web_server_init
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
