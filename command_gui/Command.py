import rclpy
import tkinter as tk
from rclpy.node import Node
from UI.CommandUIBlocks import MainMenu
from motion_msgs.msg import Command


class CommandNode(Node):

    # ROS tings
    command_publisher = None
    timer = None

    # Tkinter tings
    window : tk.Tk = None
    menu : MainMenu = None
    UI = None

    #cmd tuple

    def __init__(self, *args, **kwargs):

        super().__init__("CommandGUI")
        self.window = tk.Tk()
        self.window.title("Barebones UI")
        self.window.geometry("900x600")

        self.menu = MainMenu(self.window)

        self.command_publisher = self.create_publisher(
            Command,
            "temp_topic",
            10)

        self.timer = self.create_timer(
            0.1,
            self.timer_callback
        )

    def timer_callback(self): # hijacked the update loop!
        self.window.update()
        self.menu.update_menu()
        self.checkPublishStatus()

    def checkPublishStatus(self):
        if self.menu.is_command_available:
            cmd = self.menu.cmd
            self.command_publisher.publish(cmd)
            self.menu.is_command_available = False
        pass

def main(*args, **kwargs):

    rclpy.init()

    node = CommandNode()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()

        