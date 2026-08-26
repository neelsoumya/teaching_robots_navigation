# doubler.py
#
# THE NEW IDEA IN THIS PRACTICAL: a node that is BOTH a subscriber and a
# publisher at the same time. It listens on one topic, transforms whatever
# it hears, and republishes the result on a *different* topic.
#
# This "listen, transform, republish" pattern is extremely common in real
# ROS systems - e.g. a node that takes raw camera data in and publishes a
# processed/filtered version out, without the rest of the system needing to
# know or care how the transformation happened.

import rclpy
from rclpy.node import Node
from std_msgs.msg import Int64


class Doubler(Node):
    def __init__(self):
        super().__init__('doubler')

        # Set up the OUTPUT side first: a publisher for the transformed
        # value. We create this before the subscription so the publisher
        # already exists by the time the first incoming message needs
        # republishing.
        self.publisher_ = self.create_publisher(Int64, 'doubled_numbers', 10)

        # Set up the INPUT side: subscribe to the raw numbers topic, and
        # call on_number every time a new one arrives.
        self.subscription = self.create_subscription(
            Int64,
            'numbers',
            self.on_number,
            10
        )

    def on_number(self, msg):
        doubled = msg.data * 2                 # the actual "work" this node does

        out_msg = Int64()
        out_msg.data = doubled
        self.publisher_.publish(out_msg)       # republish the transformed value

        # Log both sides of the transformation so we can watch it happen
        self.get_logger().info(f'Received {msg.data}, publishing {doubled}')


def main():
    rclpy.init()
    node = Doubler()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
