cmake_minimum_required(VERSION 3.8)
project(commission)

if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_compile_options(-Wall -Wextra -Wpedantic)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(picam_client_init src/picam_client_init)

target_include_directories(picam_client_init PUBLIC
  "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
  "$<INSTALL_INTERFACE:include/${PROJECT_NAME}>"
)

ament_target_dependencies(picam_client_init
  rclcpp
  std_msgs
)

install(
  TARGETS picam_client_init
  DESTINATION lib/${PROJECT_NAME}
)

ament_package()
