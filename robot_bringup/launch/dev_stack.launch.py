from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description() -> LaunchDescription:
    model = DeclareLaunchArgument(
        'model',
        default_value=PathJoinSubstitution(
            [FindPackageShare('robot_description'), 'urdf', 'manipulator_robot.urdf']
        ),
        description='Absolute path to URDF file',
    )

    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': ParameterValue(
                    Command(['xacro ', LaunchConfiguration('model')]),
                    value_type=str,
                )
            }
        ],
        output='screen',
    )

    jsp_gui = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        output='screen',
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        output='screen',
    )

    return LaunchDescription([model, rsp, jsp_gui, rviz])
