import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node

import xacro


def generate_launch_description():

    # Check if we're told to use sim time
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_robot_simulation = LaunchConfiguration('robot_simulation')
    # Process the URDF file
    pkg_path = os.path.join(get_package_share_directory('kalBot'))
    xacro_file = os.path.join(pkg_path,'description','robot.urdf.xacro')
    robot_description_config = xacro.process_file(xacro_file)
    
    # Create a robot_state_publisher node
    params = {'robot_description': robot_description_config.toxml(), 'use_sim_time': use_sim_time}
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[params]
    )
    params = {'robot_simulation': use_robot_simulation }
    node_kalBot_controller = Node(
            package='my_controller',
            executable='driver',
            output='screen',
            emulate_tty=True,
            parameters=[params]
        )

    # Launch!
    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Use sim time if true'),
        DeclareLaunchArgument(
            'robot_simulation',
            default_value="True",
            description='Use sim if true'
        ),
        node_robot_state_publisher,
        node_kalBot_controller
    ])
