#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
import sys
import tty
import termios

class TeleopNode(Node):
    def __init__(self):
        super().__init__('teleop_node')
        self.pub = self.create_publisher(JointTrajectory, '/joint_trajectory_controller/joint_trajectory', 10)
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'joint8', 'joint9', 'joint10', 'joint11', 'joint12', 'joint13', 'joint14', 'joint15', 'joint16', 'joint17', 'joint18', 'joint19', 'joint20']
        self.positions = [0.0] * 20
        self.step = 0.1

    def send_command(self):
        msg = JointTrajectory()
        msg.joint_names = self.joint_names
        point = JointTrajectoryPoint()
        point.positions = self.positions
        point.time_from_start.sec = 1
        msg.points = [point]
        self.pub.publish(msg)
        print(f"发送位置: {self.positions[:4]}...")

    def get_key(self):
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            key = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
        return key

def main():
    rclpy.init()
    node = TeleopNode()
    print("控制键: a/d 增加/减少当前关节, w/s 切换关节, 空格发送, q退出")
    joint_idx = 0
    while True:
        key = node.get_key()
        if key == 'q':
            break
        elif key == 'w':
            joint_idx = (joint_idx + 1) % 20
            print(f"当前控制关节: {node.joint_names[joint_idx]}")
        elif key == 's':
            joint_idx = (joint_idx - 1) % 20
            print(f"当前控制关节: {node.joint_names[joint_idx]}")
        elif key == 'a':
            node.positions[joint_idx] -= node.step
            print(f"{node.joint_names[joint_idx]} = {node.positions[joint_idx]:.2f}")
        elif key == 'd':
            node.positions[joint_idx] += node.step
            print(f"{node.joint_names[joint_idx]} = {node.positions[joint_idx]:.2f}")
        elif key == ' ':
            node.send_command()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
