# listener.py
#
# The counterpart to talker.py. This node SUBSCRIBES to 'hello_topic' and
# reacts every time a new message arrives — it doesn't run on a timer, ROS
# calls our function automatically whenever data shows up.

import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class HelloListener(Node):
    def __init__(self):
        super().__init__('hello_listener')

        # create_subscription(message_type, topic_name, callback, queue_size).
        # `on_message` is a callback: we hand ROS the function, and ROS calls
        # it for us — we never call on_message() ourselves anywhere.
        self.subscription = self.create_subscription(
            String,
            'hello_topic',
            self.on_message,
            10
        )

    def on_message(self, msg):
        # `msg` here is a String message object; msg.data is the text inside.
        self.get_logger().info(f'Heard: "{msg.data}"')


def main():
    rclpy.init()
    node = HelloListener()
    rclpy.spin(node)     # blocks, waiting for messages, calling on_message()
                          # each time one arrives, until Ctrl+C
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
