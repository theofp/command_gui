import tkinter as tk
from tkinter import ttk
from UI.UI_blocks.dynamic_entries import DynamicNumberEntry
from UI.UI_tools.field_validators import *
from UI.JointSliderUI import JointSliderUI
from motion_msgs.msg import Command
from motion_msgs.msg import Movement
from motion_msgs.msg import Misc
from motion_msgs.msg import Trajectory
from UI.UI_tools.CommandEnums import *
from UI.CommandUIBlocks import *
from UI.CLIUI import CLIUI
import os

class MainMenu():

    # Buttons

    TargetXYZButton : tk.Button = None
    TargetButton : tk.Button = None
    MiscButton : tk.Button = None
    JointSliderButton : tk.Button = None
    MainMenuButton : tk.Button = None

    # Permanent Menu (this is a frame to yes)

    PermanentMenu : tk.Frame = None
    
    # Frames

    TargetXYZUI : CommandUITargetXYZ = None
    TargetUI : CommandUITarget = None
    MiscUI : MiscCommandUI = None
    JointSliderUI_ : JointSliderUI= None

    CLIUI_ : CLIUI = None

    is_command_available : bool = False
    path : str = os.getcwd()
    image_path : str = os.path.join(path,"src","command_gui","UI", "Images")
    menu_img_path : str = os.path.join(image_path, "Robot1.png")

    type_dict : dict 

    # Misc
    root : tk.Tk = None
    cmd : Command = Command()

    def __init__(self, root):

        self.root = root

        self.TargetXYZUI = CommandUITargetXYZ(self.root)
        self.TargetUI = CommandUITarget(self.root)
        self.MiscUI = MiscCommandUI(self.root)
        self.JointSliderUI_ = JointSliderUI(self.root)
        self.CLIUI_ = CLIUI(self.root)

        self.MenuGUI = tk.Frame(self.root)
        self.setupMenuGUI()

        self.is_menu_active = True
        self.is_target_xyz_ui_active = False
        self.is_target_ui_active = False
        self.is_misc_ui_active = False
        self.is_joint_slider_ui_active = False
        self.is_cli_ui_active = False

        self.active_frame = self.MenuGUI

        self.MainMenuButton = tk.Button(
            master = self.root,
            text="Main Menu",
            font=("Arial", 12),
            command=self.show_menu_gui
        )

        self.PublishButton = tk.Button(
            master = self.root,
            text="Publish Command",
            font=("Arial", 12),
            command=self.publish_pipeline_start
        )

        self.PermanentMenu = PermanentUI(self.root)

        self.build()

    # UI preparation method

    def setupMenuGUI(self):

        self.TargetXYZButton = tk.Button(
            master = self.MenuGUI,
            text="Target XYZ",
            font=("Arial", 12),
            command=self.show_target_xyz_ui
        )

        self.TargetButton = tk.Button(
            master = self.MenuGUI,
            text="Target",
            font=("Arial", 12),
            command=self.show_target_ui
        )

        self.MiscButton = tk.Button(
            master = self.MenuGUI,
            text="Misc",
            font=("Arial", 12),
            command=self.show_misc_ui
        )

        self.JointSliderButton = tk.Button(
            master = self.MenuGUI,
            text="Joint Sliders",
            font=("Arial", 12),
            command=self.show_joint_slider_ui
        )

        self.CLIUIButton = tk.Button(
            master = self.MenuGUI,
            text="Command Line Interface",
            font=("Arial", 12),
            command=self.show_cli_ui
        )

        self.TargetXYZButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.TargetButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.MiscButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.JointSliderButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.CLIUIButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.MenuGUI.is_command_available = False

    def build(self):

        if self.is_menu_active:
            self.show_menu_gui()
            return
        
        if self.is_target_xyz_ui_active:
            self.show_target_xyz_ui()
            return
        
        if self.is_target_ui_active:
            self.show_target_ui()
            return
        
        if self.is_misc_ui_active:
            self.show_misc_ui()
            return
        
        if self.is_joint_slider_ui_active:
            self.show_joint_slider_ui()

        if self.is_cli_ui_active:
            self.show_cli_ui()
            return

        else:
            print("No UI is active, nothing to build")
            return      

    # UI Update methods

    def show_menu_gui(self):

        self.forget_all_frames()
        self.is_menu_active = True
        self.MenuGUI.grid(row = 0, column = 0, rowspan = 3 , sticky="nsew", padx=10, pady=10)
        self.PermanentMenu.grid(row = 0, column = 1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.PermanentMenu.set_label_text("Main Menu")
        self.active_frame = self.MenuGUI    

    def show_target_xyz_ui(self):

        self.forget_all_frames()
        self.is_target_xyz_ui_active = True
        self.TargetXYZUI.grid(row = 0, column = 0, sticky="nsew", padx=10, pady=10)
        self.MainMenuButton.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)
        self.PublishButton.grid(row = 2, column = 0, sticky="ew", padx=10, pady=10)
        self.PermanentMenu.grid(row = 0, column = 1, rowspan = 3, sticky="nsew", padx=10, pady=10)
        self.PermanentMenu.set_label_text("Cartesian Target")
        self.active_frame = self.TargetXYZUI

    def show_target_ui(self):

        self.forget_all_frames()
        self.is_target_ui_active = True
        self.TargetUI.grid(row = 0, column = 0, sticky="nsw", padx=10, pady=10)
        self.MainMenuButton.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)
        self.PublishButton.grid(row = 2, column = 0, sticky="ew", padx=10, pady=10)
        self.PermanentMenu.grid(row = 0, column = 1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.PermanentMenu.set_label_text("Joint Target")
        self.active_frame = self.TargetUI

    def show_misc_ui(self):

        self.forget_all_frames()
        self.is_misc_ui_active = True
        self.MiscUI.grid(row = 0, column = 0, sticky="nsew", padx=10, pady=10)
        self.MainMenuButton.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)
        self.PublishButton.grid(row = 2, column = 0, sticky="ew", padx=10, pady=10)
        self.PermanentMenu.grid(row = 0, column = 1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.PermanentMenu.set_label_text("Miscellaneous Commands")
        self.active_frame = self.MiscUI

    def show_joint_slider_ui(self):

        self.forget_all_frames()
        self.is_joint_slider_ui_active = True
        self.JointSliderUI_.grid(row = 0, column = 0, sticky="nsew", padx=10, pady=10)
        self.MainMenuButton.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)
        self.PublishButton.grid(row = 2, column = 0, sticky="ew", padx=10, pady=10)
        self.PermanentMenu.grid(row = 0, column = 1, rowspan=3, sticky="nsew", padx=10, pady=10)
        self.PermanentMenu.set_label_text("Joint Slider")
        self.active_frame = self.JointSliderUI_

    def show_cli_ui(self):
        self.forget_all_frames()
        self.is_cli_ui_active = True
        self.CLIUI_.grid(row = 0, column = 0, columnspan = 4, sticky="nsew", padx=10, pady=10)
        self.MainMenuButton.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)
        self.PermanentMenu.disable_image()
        self.PermanentMenu.grid(row = 1, column = 1, columnspan = 3, sticky="nsew", padx=10, pady=10)
        self.active_frame = self.CLIUI_

    def forget_all_frames(self):
        if self.active_frame is self.CLIUI_:
            self.PermanentMenu.enable_image()

        self.is_menu_active = False
        self.is_target_xyz_ui_active = False
        self.is_target_ui_active = False
        self.is_misc_ui_active = False
        self.is_joint_slider_ui_active = False
        self.is_cli_ui_active = False

        self.MainMenuButton.grid_forget()
        self.MenuGUI.grid_forget()
        self.TargetXYZUI.grid_forget()
        self.TargetUI.grid_forget()
        self.MiscUI.grid_forget()
        self.JointSliderUI_.grid_forget()
        self.PublishButton.grid_forget()
        self.PermanentMenu.grid_forget()
        self.CLIUI_.grid_forget()

    # Command Builders

    def build_command_TargetXYZ(self):

        self.preset_command()
        self.cmd.type = CommandType.Movement.value
        self.cmd.motion = Movement()

        self.cmd.motion.target_xyz.x = float(self.TargetXYZUI.entries[0].field_value)
        self.cmd.motion.target_xyz.y = float(self.TargetXYZUI.entries[1].field_value)
        self.cmd.motion.target_xyz.z = float(self.TargetXYZUI.entries[2].field_value)
        
        self.cmd.motion.solver_type = SolverType[self.TargetXYZUI.solver_type.get()].value
        self.cmd.motion.type = MotionTypeXYZ[self.TargetXYZUI.motion_type.get()].value

        self.TargetXYZUI.is_command_available = False

    def build_command_Target(self):

        self.preset_command()
        self.cmd.type = CommandType.Movement.value
        self.cmd.motion = Movement()
        
        self.cmd.motion.target.t1 = float(self.TargetUI.entries[0].field_value)
        self.cmd.motion.target.t2 = float(self.TargetUI.entries[1].field_value)
        self.cmd.motion.target.t3 = float(self.TargetUI.entries[2].field_value)
        self.cmd.motion.target.t4 = float(self.TargetUI.entries[3].field_value)
        self.cmd.motion.target.t5 = float(self.TargetUI.entries[4].field_value)

        self.cmd.motion.type = MotionType[self.TargetUI.motion_type.get()].value

        self.TargetUI.is_command_available = False

    def build_command_Misc(self):

        self.preset_command()
        self.cmd.type = CommandType.Misc.value
        self.cmd.misc.type = MiscType[self.MiscUI.misc_type.get()].value

        parameter = self.MiscUI.misc_param_entry.get()

        if parameter == "":
            self.cmd.misc.misc_parameter = 0.0
        else:
            self.cmd.misc.misc_parameter = float(parameter)

        
        self.MiscUI.is_command_available = False

    def build_command_JointSlider(self):

        self.preset_command()
        self.cmd.type = CommandType.Movement.value
        self.cmd.motion = Movement()
        self.cmd.motion.type = MovementType.GoTo.value

        self.cmd.motion.target = self.JointSliderUI_.get_slider_values()

        self.JointSliderUI_.is_command_available = False

    def build_command_permanent_menu_command(self):

        self.preset_command()
        self.cmd.type = CommandType.Misc.value
        self.cmd.misc.type = self.PermanentMenu.command_type.value

        self.cmd.misc.misc_parameter = 0.0

        self.PermanentMenu.is_command_available = False

    def preset_command(self):

        self.cmd.type = CommandType.Undefined.value
        self.cmd.motion = Movement()
        self.cmd.misc = Misc()
        self.trajectory = Trajectory()

        return self.cmd

    # MAINLOOP METHODS

    def update_menu(self): ### Could be made more beautiful with a dictionary of methods

        if not self.active_frame.is_command_available:

            if self.PermanentMenu.is_command_available:

                self.is_command_available = True
                self.build_command_permanent_menu_command()
                return 

            if self.active_frame == self.CLIUI_:
            
                if (len(self.CLIUI_.command_queue) > 0 and not self.is_command_available):
                    self.is_command_available = True
                    self.cmd = self.CLIUI_.command_queue.pop(0)
                    return

            self.is_command_available = False
            return

        if self.active_frame == self.TargetXYZUI:
            
            self.is_command_available = True
            self.build_command_TargetXYZ()
            return

        if self.active_frame == self.TargetUI:

            self.is_command_available = True
            self.build_command_Target()
            return

        if self.active_frame == self.MiscUI:

            self.is_command_available = True
            self.build_command_Misc()
            return

        if self.active_frame == self.JointSliderUI_:

            self.is_command_available = True
            self.build_command_JointSlider()
            return  



    def publish_pipeline_start(self): # this allows the publication of garbage (maybe not with the internal validators)
        if self.active_frame == self.MenuGUI:
            print("No command to publish, please select a command type")
            return
        else:
            self.active_frame.is_command_available = True
        

    
      