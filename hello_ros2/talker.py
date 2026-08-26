# talker.py
#
# This is the "hello world" of ROS: a node that repeatedly PUBLISHES a text
# message onto a "topic" — a named channel that any other node can listen to.
# Publishers don't know or care who (if anyone) is listening; that's the whole
# point of ROS's design, it decouples nodes from each other.

import rclpy                      # the core ROS 2 Python client library
from rclpy.node import Node       # base class every ROS 2 node inherits from
from std_msgs.msg import String   # a built-in message type: just wraps one string


class HelloTalker(Node):
    def __init__(self):
        # Every node needs a unique name — ROS uses it to identify the node
        # on the network (e.g. in `ros2 node list`).
        super().__init__('hello_talker')

        # create_publisher(message_type, topic_name, queue_size).
        # queue_size=10 means: if messages pile up faster than they can be
        # sent, buffer up to 10 before dropping the oldest ones.
        self.publisher_ = self.create_publisher(String, 'hello_topic', 10)

        # A "timer" calls a function on a fixed schedule. Here, ROS will call
        # self.publish_hello every 1.0 second, forever, until we stop the node.
        self.timer = self.create_timer(1.0, self.publish_hello)

        # Just a counter so we can visibly see the messages changing over time.
        self.count = 0

    def publish_hello(self):
        msg = String()                                       # empty message
        msg.data = f'Hello, ROS! (message #{self.count})'     # fill in its one field
        self.publisher_.publish(msg)                          # send it on 'hello_topic'

        # ROS's built-in logger, rather than print(), tags output with the
        # node name + timestamp, which becomes very useful once you have many
        # nodes running at once and need to tell their output apart.
        self.get_logger().info(f'Publishing: "{msg.data}"')

        self.count += 1


def main():
    rclpy.init()              # start up the ROS 2 client library — do this first
    node = HelloTalker()      # construct our node
    rclpy.spin(node)          # hand control to ROS: blocks here, repeatedly
                               # triggering the timer callback, until Ctrl+C
    node.destroy_node()       # clean shutdown
    rclpy.shutdown()


if __name__ == '__main__':
    main()
