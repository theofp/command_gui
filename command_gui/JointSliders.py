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
        super().__init__(name)
        self.window = tk.Tk()
        self.window.title("Barebones UI")
        self.window.geometry("300x500")
        self.UI = JointSliderUI(self.window)

        self.publisher = self.create_publisher(Float32MultiArray, "testUIOut", 10)

        self.timer = self.create_timer(
            0.05,
            self.timer_callback
        )

    def timer_callback(self):
        self.window.update()
        out = self.UI.get_slider_values()
        pub = Float32MultiArray()
        for i in range(len(out)):
            pub.data.append(out[i])
        self.publisher.publish(pub)


def main(*args, **kwargs):

    rclpy.init()

    node = JointSliderNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()



if __name__ == "__main__":
    main()