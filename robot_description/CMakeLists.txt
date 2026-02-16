cmake_minimum_required(VERSION 3.20)
project(robot_description)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY urdf meshes config
  DESTINATION share/${PROJECT_NAME}
  PATTERN "*:Zone.Identifier*" EXCLUDE
)

ament_package()
