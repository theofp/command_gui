import tkinter as tk
from rclpy import Node
from UI.CommandUIBlocks import MainMenu
import motion_msgs.msg.Command as Command


class CommandNode(Node):

    # ROS tings
    command_publisher = None
    timer = None

    # Tkinter tings
    window : tk.Tk = None
    menu : MainMenu = None
    UI = None

    #cmd tuple

    cmd : tuple = None

    def __init__(self, *args, **kwargs):

        super().__init__("CommandGUI")
        self.window = tk.Tk()
        self.window.title("Barebones UI")
        self.window.geometry("300x500")

        self.menu = MainMenu(root = self.window)

        self.command_publisher = self.create_publisher(
            Command,
            "temp_topic",
            10)

        self.timer = self.create_timer(
            0.1,
            self.timer_callback()
        )

    def timer_callback(self): # hijacked the update loop!
        self.window.update()
        self.menu.update_menu()
        self.checkPublishStatus()

    def checkPublishStatus(self):
        if self.menu.is_command_available:
            cmd = self.menu.cmd
            self.command_publisher.publish(cmd)
        pass

    def preset_command(self):

        self.cmd.command_type = "default"
        self.cmd.target_xyz = {0,0,0}
        self.cmd.target = {0,0,0,0,0}
        self.cmd.time = 0.0 # s
        self.cmd.movement_type = "4D"
        self.cmd.is_approach_given = False
        self.cmd.Approach4D = 0.0
        self.cmd.Approach5D = {0,0}
        self.cmd.PathName = "default"

        return



        