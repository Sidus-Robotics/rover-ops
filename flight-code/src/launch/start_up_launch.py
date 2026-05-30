from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='PLACE_HOLDER',
            namespace='PLACE_HOLDER',
            executable='PLACE_HOLDER',
            name='sim',
            arguments=['--ros-args', '--log-level', 'info']
        ),
        Node(
            package='PLACE_HOLDER',
            namespace='PLACE_HOLDER',
            executable='PLACE_HOLDER',
            name='sim',
            ros_arguments=['--log-level', 'warn']
        ),
        Node(
            package='PLACE_HOLDER',
            executable='PLACE_HOLDER',
            name='PLACE_HOLDER',
            remappings=[
                ('/PLACE_HOLDER/PLACE_HOLDER', '/PLACE_HOLDER/PLACE_HOLDER/PLACE_HOLDER'),
                ('/PLACE_HOLDER/PLACE_HOLDER', '/PLACE_HOLDER/PLACE_HOLDER/cmPLACE_HOLDERd_vel'),
            ]
        )
    ])