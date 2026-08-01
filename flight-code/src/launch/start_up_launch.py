from launch import LaunchDescription
from launch_ros.actions import Node, ComposableNodeContainer
from launch_ros.descriptions import ComposableNode


def generate_launch_description() -> LaunchDescription:

    return LaunchDescription(
        [
            Node(
                package="comms_init",
                namespace="comms",
                executable="web_client_init",
                name="web_client",
                arguments=["--log-level", "info"],
            ),
            Node(
                package="comms_init",
                namespace="comms",
                executable="serial_bridge_init",
                name="serial_bridge",
                ros_arguments=["--log-level", "info"],
            ),
            ComposableNodeContainer(
                name="camera_container",
                namespace="",
                package="rclcpp_components",
                executable="component_container",
                composable_node_descriptions=[
                    ComposableNode(
                        package="camera_ros",
                        plugin="camera::CameraNode",
                        parameters=[
                            {
                                "camera": 0,
                                "frame_id": "cam0",
                                "width": 640,
                                "height": 480,
                                "format": "auto",
                            }
                        ],
                        extra_arguments=[{"use_intra_process_comms": True}],
                    ),
                    ComposableNode(
                        package="camera_ros",
                        plugin="camera::CameraNode",
                        parameters=[
                            {
                                "camera": 1,
                                "frame_id": "cam1",
                                "width": 640,
                                "height": 480,
                                "format": "auto",
                            }
                        ],
                        extra_arguments=[{"use_intra_process_comms": True}],
                    ),
                ],
                output="screen",
            ),
        ]
    )