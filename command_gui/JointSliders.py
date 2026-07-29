import rclpy
from rclpy.node import Node
from UI.JointSliderUI import JointSliderUI
import tkinter as tk
from rclpy.clock import Time
from std_msgs.msg import Float32MultiArray

class JointSliderNode(Node):

    UI : JointSliderUI = None
    window : tk.Tk = None 

    def __init__(self, name : str = 'JointSlider'):
        super.__init__(name)
        self.window = tk.Tk()
        self.window.title("Barebones UI")
        self.window.size("900x300")
        self.UI = JointSliderUI(self.window)

        self.publisher = self.create_publisher(Float32MultiArray, "testUIOut")

        self.timer = self.create_timer(
            0.05,
            self.timer_callback()
        )

    def timer_callback(self):
        out = self.UI.get_slider_values()
        pub = Float32MultiArray()
        for i in range(len(out)):
            pub[i] = out[i]
        self.publisher.publish(pub)


def main(*args, **kwargs):

    rclpy.init(args,kwargs)

    node = JointSliderNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()



if __name__ == "__main__":
    main()