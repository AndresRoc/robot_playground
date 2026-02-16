# robot_bringup

Development launch package.

Current launch target:
- `dev_stack.launch.py`: starts `robot_state_publisher`, `joint_state_publisher_gui`, and `rviz2`.

Next step:
- replace with xacro-based and package-share-based model loading,
- add launch profiles per robot (`manipulator`, `scara`, `mobile`).
