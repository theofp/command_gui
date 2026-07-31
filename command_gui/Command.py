import tkinter as tk
from rclpy import Node

class CommandNode(Node):

    window : tk.Tk = None
    UI = None

    def __init__(self, *args, **kwargs):
        super().__init__("CommandGUI")
        self.window = tk.Tk()
        self.window.title("Barebones UI")
        self.window.geometry("300x500")
        # self.UI = JointSliderUI(self.window)

        self.timer = self.create_timer(
            0.05,
            self.timer_callback()
        )

    def timer_callback():
        pass
        