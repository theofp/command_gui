import rclpy
import tkinter as tk
from rclpy.node import Node
from UI.MainMenu import MainMenu
from motion_msgs.msg import Command
from UI.UI_tools.CommandEnums import *


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
        self.window.geometry("800x700")

        self.window.grid_columnconfigure(0, minsize=300, weight=0)
        self.window.grid_columnconfigure(1, minsize=500, weight=0)

        self.window.grid_rowconfigure(0, minsize=500, weight=0)
        self.window.grid_rowconfigure(1, minsize=100, weight=0)
        self.window.grid_rowconfigure(2, minsize=100, weight=0)

        self.menu = MainMenu(self.window)
        self.is_alive = True

        self.command_publisher = self.create_publisher(
            Command,
            "GUI_command",
            10)

        self.emergency_command_publisher = self.create_publisher(
            Command,
            "GUI_emergency_command",
            10)

        self.timer = self.create_timer(
            0.1,
            self.timer_callback
        )

    def timer_callback(self): # hijacked the update loop!

        self.window.update()
        self.menu.update_menu()
        self.checkPublishStatus()

        # This does not work when the window is closed but ironically that makes it throw an error that leads to killing the process
        if not self.window.winfo_exists(): 
            self.is_alive = False

    def checkPublishStatus(self):

        if self.menu.is_command_available:

            is_emergency = False
            cmd = self.menu.cmd

            if cmd.type == CommandType.Misc.value:
                if (cmd.misc.type == MiscType.Stop.value or
                    cmd.misc.type == MiscType.Start.value or
                    cmd.misc.type == MiscType.Resume.value):

                    is_emergency = True
                
            if is_emergency:
                self.emergency_command_publisher.publish(cmd)
            else:
                self.command_publisher.publish(cmd)

            self.menu.is_command_available = False

        pass

def main(*args, **kwargs):

    rclpy.init()

    node = CommandNode()

    while node.is_alive:
        rclpy.spin_once(node)

    node.destroy_node()
    rclpy.shutdown()

        