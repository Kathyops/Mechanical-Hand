import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Joy
from std_msgs.msg import Float64MultiArray


class JoyToHand(Node):

    def __init__(self):
        super().__init__('joy_to_hand')

        self.publisher = self.create_publisher(
            Float64MultiArray,
            '/hand_controller/commands',
            10
        )

        self.subscription = self.create_subscription(
            Joy,
            '/joy',
            self.joy_callback,
            10
        )


    def joy_callback(self, msg):

        # 左摇杆左右
        value = msg.axes[0]

        # 映射到关节角度
        angle = value * 3.14

        command = Float64MultiArray()
        command.data = [angle]

        self.publisher.publish(command)


def main():

    rclpy.init()

    node = JoyToHand()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()
