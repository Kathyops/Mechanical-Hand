cmake_minimum_required(VERSION 3.8)
project(el_hand)

find_package(ament_cmake REQUIRED)

# 如果有 C++ 代码，取消注释
# find_package(rclcpp REQUIRED)
# add_executable(my_node src/main.cpp)
# target_link_libraries(my_node rclcpp::rclcpp)
# install(TARGETS my_node DESTINATION lib/${PROJECT_NAME})

# 安装 URDF/meshes/launch 等文件
install(
  DIRECTORY urdf meshes launch config
  DESTINATION share/${PROJECT_NAME}
)

ament_package()


