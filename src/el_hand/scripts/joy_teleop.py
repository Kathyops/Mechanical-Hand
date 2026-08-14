
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Joy
from std_msgs.msg import Float64MultiArray

class JoyTeleopNode(Node):
    def __init__(self):
        super().__init__('joy_teleop_node')
        
        self.sub = self.create_subscription(Joy, '/joy', self.joy_callback, 10)
        # 修改：适配 hand_controller
        self.pub = self.create_publisher(Float64MultiArray, '/hand_controller/commands', 10)
        
        self.joint_names = ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'joint8', 'joint9', 'joint10', 'joint11', 'joint12', 'joint13', 'joint14', 'joint15', 'joint16', 'joint17', 'joint18', 'joint19', 'joint20']
        self.positions = [0.0] * 20
        
        self.step = 0.05
        self.current_joint = 0
        self.deadzone = 0.15
        
        self.BTN_PREV = 4
        self.BTN_NEXT = 5
        self.BTN_SEND = 0
        self.BTN_RESET = 1
        self.BTN_ZERO = 2
        self.AXIS_CONTROL = 1
        self.AXIS_DIRECTION = 1
        
        self.get_logger().info('🎮 手柄遥操作已启动！')
        self.get_logger().info(f'📍 当前关节: {self.joint_names[self.current_joint]}')

    def joy_callback(self, msg):
        moved = False
        
        if msg.buttons[self.BTN_PREV] == 1:
            self.current_joint = (self.current_joint - 1) % len(self.joint_names)
            self.get_logger().info(f'📍 当前关节: {self.joint_names[self.current_joint]}')
        if msg.buttons[self.BTN_NEXT] == 1:
            self.current_joint = (self.current_joint + 1) % len(self.joint_names)
            self.get_logger().info(f'📍 当前关节: {self.joint_names[self.current_joint]}')
        
        if abs(msg.axes[self.AXIS_CONTROL]) > self.deadzone:
            delta = msg.axes[self.AXIS_CONTROL] * self.step * self.AXIS_DIRECTION
            self.positions[self.current_joint] += delta
            self.positions[self.current_joint] = max(-3.14, min(3.14, self.positions[self.current_joint]))
            moved = True
            self.get_logger().info(f'  {self.joint_names[self.current_joint]} = {self.positions[self.current_joint]:.3f}')
        
        if msg.buttons[self.BTN_SEND] == 1:
            self.send_command()
        if msg.buttons[self.BTN_RESET] == 1:
            self.positions = [0.0] * len(self.joint_names)
            self.send_command()
            self.get_logger().info('🔄 所有关节已重置到 0')
        if msg.buttons[self.BTN_ZERO] == 1:
            self.positions[self.current_joint] = 0.0
            self.send_command()
            self.get_logger().info(f'🔄 {self.joint_names[self.current_joint]} 已归零')
        
        

    def send_command(self):
        # 发送 Float64MultiArray 给 hand_controller
        msg = Float64MultiArray()
        msg.data = self.positions
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = JoyTeleopNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
