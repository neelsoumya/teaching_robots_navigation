# number_publisher.py
#
# Same shape as talker.py, but publishes a number that increases every tick
# instead of a fixed string. This gives the next node (doubler.py) something
# worth transforming.

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64   # built-in message type wrapping one 64-bit integer


class NumberPublisher(Node):
    def __init__(self):
        super().__init__('number_publisher')

        self.publisher_ = self.create_publisher(Int64, 'numbers', 10)
        self.timer = self.create_timer(1.0, self.publish_number)
        self.current_number = 0   # the value we'll publish next

    def publish_number(self):
        msg = Int64()
        msg.data = self.current_number
        self.publisher_.publish(msg)
        self.get_logger().info(f'Publishing: {msg.data}')
        self.current_number += 1


def main():
    rclpy.init()
    node = NumberPublisher()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
