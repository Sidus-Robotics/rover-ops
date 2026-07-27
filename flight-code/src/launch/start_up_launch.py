from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='comms_init',
            namespace='comms',
            executable='web_client_init',
            name='web_client',
            arguments=['--log-level', 'info']
        ),
        Node(
            package='comms_init',
            namespace='comms',
            executable='serial_bridge_init',
            name='serial_bridge',
            ros_arguments=['--log-level', 'info']
        ),
        # Node(
        #     package='PLACE_HOLDER',
        #     executable='PLACE_HOLDER',
        #     name='PLACE_HOLDER',
        #     remappings=[
        #         ('/PLACE_HOLDER/PLACE_HOLDER', '/PLACE_HOLDER/PLACE_HOLDER/PLACE_HOLDER'),
        #         ('/PLACE_HOLDER/PLACE_HOLDER', '/PLACE_HOLDER/PLACE_HOLDER/PLACE_HOLDER'),
        #     ]
        # )
    ])