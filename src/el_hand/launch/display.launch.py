from launch import LaunchDescription
from launch_ros.actions import Node
import os

def generate_launch_description():
    # 直接使用绝对路径
    urdf_path = '/home/ubuntu/Mechanical-Hand/src/el_hand/urdf/mechanical_hand.urdf'
    
    with open(urdf_path, 'r') as f:
        robot_description = f.read()
    
    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),
        Node(
            package='rviz2',
            executable='rviz2'
        )
    ])
