from launch import LaunchDescription
from launch.actions import TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['2', '0.5', '0', '0', '0', '0', 'map', 'odom'],
            output='screen'
        ),
        
        TimerAction(
            period=5.0,  
            actions=[
                Node(
                    package='my_turtlebot3_navigation',
                    executable='my_turtlebot3_navigation',
                    output='screen',
                )
            ]
        )
    ])
