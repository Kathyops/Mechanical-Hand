import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    # 1. 获取包路径
    pkg_el_hand = get_package_share_directory('el_hand')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')

    # 2. 自动找到您左侧树里的 urdf 文件 (以 mechanical_hand.urdf 为例)
    urdf_file_path = os.path.join(pkg_el_hand, 'urdf', 'mechanical_hand.urdf')

    # 3. 读取 URDF 内容
    if not os.path.exists(urdf_file_path):
        print(f"⚠️ 注意：找不到 URDF 文件，请确认路径: {urdf_file_path}")
        return LaunchDescription()

    with open(urdf_file_path, 'r') as infp:
        robot_description = infp.read()

    # 4. 启动 Gazebo 服务和客户端
    gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')
        )
    )
    gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')
        )
    )

    # 5. 启动 robot_state_publisher (把您的 URDF 传给系统)
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description}],
    )

        # 6. 将机器人生成到 Gazebo 世界 (使用 spawn_entity 替换 spawn_entity.py)
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity',
        arguments=['-entity', 'mechanical_hand', '-file', urdf_file_path],
        output='screen'
    )

    return LaunchDescription([
        gazebo_server,
        gazebo_client,
        robot_state_publisher_node,
        spawn_entity
    ])