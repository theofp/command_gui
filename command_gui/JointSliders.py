import rclpy
from rclpy.node import Node
from UI.JointSliderUI import JointSliderUI

class JointSliderNode(Node):

    def __init__(self, name : str = 'JointSlider'):
        super.__init__(name)



def main(*args, **kwargs):

    rclpy.init(args,kwargs)

    node = JointSliderNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()



if __name__ == "__main__":
    main()