import os

from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, TimerAction
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import xacro


def generate_launch_description():

    pkg_el_hand = get_package_share_directory('el_hand')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')


    urdf_file_path = os.path.join(
        pkg_el_hand,
        'urdf',
        'mechanical_hand.urdf'
    )


    robot_description = xacro.process_file(urdf_file_path).toxml()


    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_gazebo_ros,
                'launch',
                'gzserver.launch.py'
            )
        )
    )


    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                pkg_gazebo_ros,
                'launch',
                'gzclient.launch.py'
            )
        )
    )


    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[
            {
                'robot_description': robot_description
            }
        ],
        output='screen'
    )


    spawn_entity = TimerAction(
    period=3.0,
    actions=[
        Node(
            package='gazebo_ros',
            executable='spawn_entity.py',
            arguments=[
                '-entity',
                'mechanical_hand',
                '-topic',
                'robot_description',
                '-x',
                '0',
                '-y',
                '0',
                '-z',
                '0.0'
            ],
            output='screen'
        )
    ]
)

    
    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "joint_state_broadcaster",
            "-c",
            "/controller_manager"
     ],
)

    
    hand_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=[
            "hand_controller",
            "-c",
            "/controller_manager"
        ],

 )

    return LaunchDescription([
        gazebo_server,
        gazebo_client,
        robot_state_publisher,
        spawn_entity,
        joint_state_broadcaster_spawner,
        hand_controller_spawner
    ])
