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
            Node(
                package="camera_ros",
                namespace="cameras",
                executable="camera_node",
                name="cam0",
                parameters=[
                    {
                        "camera": 0,
                        "role": "viewfinder",
                        "format": "XBGR8888",
                        "width": 640,
                        "height": 480,
                        "jpeg_quality": 50,
                        "sensor_mode": "mode_2x2binned_720p_regs",
                        "frame_id": "cam0",
                        "FrameDurationLimits": [33333, 33333],
                    }
                ],
            ),
            Node(
                package="camera_ros",
                namespace="cameras",
                executable="camera_node",
                name="cam1",
                parameters=[
                    {
                        "camera": 1,
                        "role": "viewfinder",
                        "format": "XBGR8888",
                        "width": 640,
                        "height": 480,
                        "jpeg_quality": 50,
                        "sensor_mode": "mode_2x2binned_720p_regs",
                        "frame_id": "cam1",
                        "FrameDurationLimits": [33333, 33333],
                    }
                ],
            ),
            Node(
                package="web_video_server",
                namespace="video_server",
                executable="web_video_server",
                name="video_server",
                parameters=[{"port": 8081, "address": "0.0.0.0"}],
            ),
            # ComposableNodeContainer(
            #     name="camera_container",
            #     namespace="",
            #     package="rclcpp_components",
            #     executable="component_container",
            #     composable_node_descriptions=[
            #         ComposableNode(
            #             package="camera_ros",
            #             plugin="camera::CameraNode",
            #             name="cam0",
            #             parameters=[
            #                 {
            #                     "camera": 0,
            #                     "frame_id": "cam0",
            #                     "width": 640,
            #                     "height": 480,
            #                     "format": "XBGR8888",
            #                 }
            #             ],
            #             extra_arguments=[{"use_intra_process_comms": True}],
            #         ),
            #         ComposableNode(
            #             package="camera_ros",
            #             plugin="camera::CameraNode",
            #             name="cam1",
            #             parameters=[
            #                 {
            #                     "camera": 1,
            #                     "frame_id": "cam1",
            #                     "width": 640,
            #                     "height": 480,
            #                     "format": "XBGR8888",
            #                 }
            #             ],
            #             extra_arguments=[{"use_intra_process_comms": True}],
            #         ),
            #     ],
            #     output="screen",
            # ),
        ]
    )
