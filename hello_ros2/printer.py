# printer.py
#
# The end of the pipeline: subscribes to the final, transformed topic and
# prints what it sees. Deliberately the same shape as listener.py from the
# hello world - once you've learned the subscriber pattern once, you've
# learned it for good.

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class Printer(Node):
    def __init__(self):
        super().__init__('printer')
        self.subscription = self.create_subscription(
            Int64,
            'doubled_numbers',
            self.on_number,
            10
        )

    def on_number(self, msg):
        self.get_logger().info(f'Final result: {msg.data}')


def main():
    rclpy.init()
    node = Printer()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
