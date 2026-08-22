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


class CommandUITargetXYZ(tk.Frame):

    root : tk.Tk = None

    is_command_available : bool = False

    pi = 3.1415
    pi2 = pi/2

    u_bound = [ pi/3,  pi/3]
    l_bound = [-pi/3, -pi/3]

    entry_labels = [
        "X",
        "Y",
        "Z"
    ]

    def __init__(self, root : tk.Tk):

        super().__init__()
        self.root = root

        self.entries = [] # UI.DynamicEntry objects
        self.labels = []  # Tk.Label objects

        self.solver_type = ttk.Combobox(
            self,
            values=[x.name for x in SolverType],
            state="readonly"
        )

        self.param_entry_1 = DynamicNumberEntry(root=self)

        def validator_(value, lower=self.l_bound[0], upper=self.u_bound[0]):
            try:
                x = float(value)
            except ValueError:
                return False
            queerie = (lower <= x <= upper)
            return queerie

        self.param_entry_1.set_validator(validator = validator_)

        self.param_entry_1.delete(0, tk.END)
        self.param_entry_1.insert(0, "0.0")

        self.param_entry_2 = DynamicNumberEntry(root=self)

        def validator_(value, lower=self.l_bound[1], upper=self.u_bound[1]):
            try:
                x = float(value)
            except ValueError:
                return False
            queerie = (lower <= x <= upper)
            return queerie

        self.param_entry_2.set_validator(validator = validator_)

        self.param_entry_2.delete(0, tk.END)
        self.param_entry_2.insert(0, "0.0")
        
        for i in range(3):

            l = tk.Label(
                master = self,
                text=self.entry_labels[i]
                )
            
            l.id = i
            l.parent = self

            e = DynamicNumberEntry(root=self)
            e.id = i
            e.config(width=10)

            def validator_(value, id = i):
                try:
                    x = float(value)
                    return True
                except ValueError:
                    return False

            e.set_validator(validator = validator_)

            e.grid(row = i, column = 1, sticky="ew", padx = 10)
            l.grid(row = i, column = 0, sticky="ew", padx = 10)

            self.entries.append(e)
            self.labels.append(l)

        self.solver_type.grid(row = 0, column = 2, columnspan=1, sticky="ew", padx=10, pady=10)
        self.solver_type.set("FourDSmart")
        self.param_entry_1.grid(row = 1, column = 2, columnspan=1, sticky="ew", padx=10, pady=10)
        self.param_entry_2.grid(row = 2, column = 2, columnspan=1, sticky="ew", padx=10, pady=10)

class CommandUITarget(tk.Frame):

    root : tk.Tk = None

    pi = 3.1415
    pi2 = pi/2

    u_bound = [ pi2,  pi2,  pi2,  pi2,  pi2]
    l_bound = [-pi2, -pi2, -pi2, -pi2, -pi2]

    entry_labels = [
        "theta 1",
        "theta 2",
        "theta 3",
        "theta 4",
        "theta 5"
    ]

    is_command_available : bool = False

    def __init__(self, root : tk.Tk):
        super().__init__()
        self.root = root

        self.entries = [] # UI.DynamicEntry objects
        self.labels = []  # Tk.Label objects

        for i in range(5):

            l = tk.Label(
                master = self,
                text=self.entry_labels[i]
                )
            l.id = i
            l.parent = self

            e = DynamicNumberEntry(root=self)
            e.id = i
            e.config(width=10)

            def validator_(value, lower=self.l_bound[i], upper=self.u_bound[i], id = i):
                try:
                    x = float(value)
                except ValueError:
                    return False
                queerie = (lower <= x <= upper)

                return queerie

            e.set_validator(validator = validator_)

            e.grid(row = i, column = 1, sticky="ew", padx = 10)
            l.grid(row = i, column = 0, sticky="ew", padx = 10)

            self.entries.append(e)
            self.labels.append(l)

class MiscCommandUI(tk.Frame):
    # i don't yet know all the commands this should encompass

    is_command_available : bool = False

    misc_type : ttk.Combobox = None
    misc_type_label : tk.Label = None
    misc_param_entry : DynamicNumberEntry = None

    root : tk.Tk = None

    def __init__(self, root):
        super().__init__()

        self.root = root
        self.is_command_available = False

        self.misc_type = ttk.Combobox(
            self,
            values=[x.name for x in MiscType],
            state="readonly"
        )

        self.misc_type.bind(
            "<<ComboboxSelected>>",
            self.misc_type_selected
        )

        self.misc_type_label = tk.Label(
            self,
            text="Undefined"
        )

        self.misc_param_entry = DynamicNumberEntry(root=self)

        def validator_(value):
            try:
                x = float(value)
            except ValueError:
                return False
            return float(value) >= 0.0

        self.misc_param_entry.set_validator(validator = validator_)

        self.misc_type.grid(row = 0, column = 0, sticky="ew", padx=10, pady=10)
        self.misc_type.set("Wait")
        self.misc_type_label.grid(row = 0, column = 1, sticky="ew", padx=10, pady=10)
        self.misc_param_entry.grid(row = 1, column = 1, sticky="ew", padx=10, pady=10)


    def misc_type_selected(self, event):

        cmd_type = self.misc_type.get()

        if (cmd_type == "Wait" or cmd_type == "WaitAndResume"):

            self.misc_type_label.config(text="Time (seconds) \n  Must be positive")
            self.misc_param_entry.config(state="normal")

        else:
            self.misc_type_label.config(text="Inactive Entry")
            self.misc_param_entry.config(state="disabled")
    # Wait commands et cetera 

class MainMenu():

    # Buttons

    TargetXYZButton : tk.Button = None
    TargetButton : tk.Button = None
    MiscButton : tk.Button = None
    JointSliderButton : tk.Button = None
    MainMenuButton : tk.Button = None
    
    # Frames

    TargetXYZUI : CommandUITargetXYZ = None
    TargetUI : CommandUITarget = None
    MiscUI : MiscCommandUI = None
    JointSliderUI_ : JointSliderUI= None

    is_command_available : bool = False

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

        self.MenuGUI = tk.Frame(self.root)
        self.setupMenuGUI()

        self.is_menu_active = True
        self.is_target_xyz_ui_active = False
        self.is_target_ui_active = False
        self.is_misc_ui_active = False
        self.is_joint_slider_ui_active = False

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

        self.TargetXYZButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.TargetButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.MiscButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.JointSliderButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

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

        else:
            print("No UI is active, nothing to build")
            return      

    # UI Update methods

    def show_menu_gui(self):

        self.forget_all_frames()
        self.is_menu_active = True
        self.MenuGUI.pack(fill=tk.BOTH, expand=True)
        self.active_frame = self.MenuGUI

    def show_target_xyz_ui(self):

        self.forget_all_frames()
        self.is_target_xyz_ui_active = True
        self.TargetXYZUI.pack(fill=tk.BOTH, expand=True)
        self.MainMenuButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.PublishButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.active_frame = self.TargetXYZUI

    def show_target_ui(self):

        self.forget_all_frames()
        self.is_target_ui_active = True
        self.TargetUI.pack(fill=tk.BOTH, expand=True)
        self.MainMenuButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.PublishButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.active_frame = self.TargetUI

    def show_misc_ui(self):

        self.forget_all_frames()
        self.is_misc_ui_active = True
        self.MiscUI.pack(fill=tk.BOTH, expand=True)
        self.MainMenuButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.PublishButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.active_frame = self.MiscUI

    def show_joint_slider_ui(self):

        self.forget_all_frames()
        self.is_joint_slider_ui_active = True
        self.JointSliderUI_.pack(fill=tk.BOTH, expand=True)
        self.MainMenuButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.PublishButton.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.active_frame = self.JointSliderUI_

    def forget_all_frames(self):

        self.is_menu_active = False
        self.is_target_xyz_ui_active = False
        self.is_target_ui_active = False
        self.is_misc_ui_active = False
        self.is_joint_slider_ui_active = False


        self.MainMenuButton.pack_forget()
        self.MenuGUI.pack_forget()
        self.TargetXYZUI.pack_forget()
        self.TargetUI.pack_forget()
        self.MiscUI.pack_forget()
        self.JointSliderUI_.pack_forget()
        self.PublishButton.pack_forget()

    # Command Builders

    def build_command_TargetXYZ(self):

        self.preset_command()
        self.cmd.type = CommandType.Movement.value
        self.cmd.motion.type = MovementType.GoToXYZ.value
        self.cmd.motion = Movement()

        self.cmd.motion.target_xyz.x = float(self.TargetXYZUI.entries[0].field_value)
        self.cmd.motion.target_xyz.y = float(self.TargetXYZUI.entries[1].field_value)
        self.cmd.motion.target_xyz.z = float(self.TargetXYZUI.entries[2].field_value)
        
        self.cmd.motion.solver_type = SolverType[self.TargetXYZUI.solver_type.get()].value

        self.TargetXYZUI.is_command_available = False

    def build_command_Target(self):

        self.preset_command()
        self.cmd.type = CommandType.Movement.value
        self.cmd.motion = Movement()
        self.cmd.motion.type = MovementType.GoTo.value # to be fixed
        
        self.cmd.motion.target.t1 = float(self.TargetUI.entries[0].field_value)
        self.cmd.motion.target.t2 = float(self.TargetUI.entries[1].field_value)
        self.cmd.motion.target.t3 = float(self.TargetUI.entries[2].field_value)
        self.cmd.motion.target.t4 = float(self.TargetUI.entries[3].field_value)
        self.cmd.motion.target.t5 = float(self.TargetUI.entries[4].field_value)

        self.TargetUI.is_command_available = False

    def build_command_Misc(self):
        # I have yet to make the UI for this
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

    def preset_command(self):

        self.cmd.type = CommandType.Undefined
        self.cmd.motion = Movement()
        self.cmd.misc = Misc()
        self.trajectory = Trajectory()

        return self.cmd

    # MAINLOOP METHODS

    def update_menu(self): ### Could be made more beautiful with a dictionary of methods

        if not self.active_frame.is_command_available:

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
        

    
        







