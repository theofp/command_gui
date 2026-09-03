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
import os


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

        self.grid_propagate(False)
        self.config(width=75, height=50)

        self.solver_type = ttk.Combobox(
            self,
            values=[x.name for x in SolverType],
            state="readonly"
        )
        self.solver_type.config(width=10)

        self.motion_type = ttk.Combobox(
            self,
            values=[x.name for x in [MotionTypeXYZ.Linear, MotionTypeXYZ.Joint]],
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
        self.param_entry_1.config(width=10)

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
        self.param_entry_2.config(width=10)
        
        for i in range(3):

            l = tk.Label(
                master = self,
                text=self.entry_labels[i],
                width=3
                )
            
            l.id = i
            l.parent = self

            e = DynamicNumberEntry(root=self)
            e.id = i
            e.config(width=10)
            e.delete(0, tk.END)
            e.insert(0, "0.0")

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
        self.param_entry_1.grid(row = 1, column = 2, columnspan=1, sticky="ew", padx=10, pady=10)
        self.param_entry_2.grid(row = 2, column = 2, columnspan=1, sticky="ew", padx=10, pady=10)
        self.motion_type.grid(row = 3, column = 0, columnspan=3, sticky="ew", padx=10, pady=10)

        self.solver_type.set("FourDSmart")
        self.motion_type.set("Joint")

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

        self.motion_type = ttk.Combobox(
            self,
            values=[x.name for x in [MotionType.Linear, MotionType.Joint]],
            state="readonly"
        )

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
            e.delete(0, tk.END)
            e.insert(0, "0.0")

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

        self.motion_type.grid(row = 5, column = 0, columnspan=2, sticky="ew", padx=10, pady=10)
        self.motion_type.set("Joint")

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
        self.grid_propagate(False)
        self.config(width=300, height=50)
        self.columnconfigure(0, weight=1)

        self.misc_type = ttk.Combobox(
            self,
            values=[x.name for x in MiscType],
            state="readonly"
        )

        self.misc_type.config(width=20)

        self.misc_type.bind(
            "<<ComboboxSelected>>",
            self.misc_type_selected
        )

        self.misc_type_label = tk.Label(
            self,
            text="Undefined"
        )

        self.misc_type_label.config(width=20)

        self.misc_param_entry = DynamicNumberEntry(root=self)
        self.misc_param_entry.config(width=20)
        self.misc_param_entry.delete(0, tk.END)
        self.misc_param_entry.insert(0, "0.0")

        def validator_(value):
            try:
                x = float(value)
            except ValueError:
                return False
            return float(value) >= 0.0

        self.misc_param_entry.set_validator(validator = validator_)

        self.misc_type.grid(row = 0, column = 0, sticky="ew", padx=10, pady=10)
        self.misc_type.set("Wait")
        self.misc_type_label.grid(row = 1, column = 0, sticky="ew", padx=10, pady=10)
        self.misc_param_entry.grid(row = 2, column = 0, sticky="ew", padx=10, pady=10)


    def misc_type_selected(self, event):

        cmd_type = self.misc_type.get()

        if (cmd_type == "Wait" or cmd_type == "WaitAndResume"):

            self.misc_type_label.config(text="Time (seconds) \n  Must be positive")
            self.misc_param_entry.config(state="normal")

        else:
            self.misc_type_label.config(text="Inactive Entry")
            self.misc_param_entry.config(state="disabled")
    # Wait commands et cetera 

class PermanentUI(tk.Frame):

    root : tk.Tk = None

    # IMG

    MenuImgLbl : tk.Label = None
    MenuImg : tk.PhotoImage = None

    path : str = os.getcwd()
    image_path : str = os.path.join(path,"src","command_gui","UI", "Images")
    menu_img_path : str = os.path.join(image_path, "Robot1.png")

    # Buttons

    HomeButton : tk.Button = None
    StopAndCancelButton : tk.Button = None
    StartAndResumeButton : tk.Button = None

    # Misc

    is_command_available : bool = False
    is_stopped : bool = False
    is_image_disabled : bool = False

    command_type = MiscType.Undefined

    def __init__(self, root : tk):
        super().__init__()
        self.root = root

        self.grid_propagate(False)
        self.config(width=500, height=700)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

        self.rowconfigure(0, weight=4)
        self.rowconfigure(1, weight=1)

        self.MenuImg = tk.PhotoImage(file=self.menu_img_path)
        self.MenuImgLbl = tk.Label(
            master = self,
            image=self.MenuImg,
            text = "Main Menu",
            font=("Arial", 20),
            compound="bottom",
            borderwidth=3,
            highlightbackground="blue",
            highlightcolor="blue",
            highlightthickness=4
        )

        self.MenuImgLbl.config(width=400, height=400)

        self.HomeButton = tk.Button(
            master = self,
            text = "Home",
            command = self.go_home,
            width=10
        )
        self.StopAndCancelButton = tk.Button(
            master = self,
            text = "Stop and Cancel",
            command = self.stop_and_cancel,
            width=10
        )
        self.StartAndResumeButton = tk.Button(
            master = self,
            text = "Start and Resume",
            command = self.start_and_resume,
            width=10
        )

        self.update_text()

        self.MenuImgLbl.grid(row = 0, column = 0, columnspan=3, sticky="nsew", padx=25, pady=10)

        self.HomeButton.grid(row = 1, column = 0, sticky="nsew", padx=25, pady=10)
        self.StopAndCancelButton.grid(row = 1, column = 1, sticky="nsew", padx=25, pady=10)
        self.StartAndResumeButton.grid(row = 1, column = 2, sticky="nsew", padx=25, pady=10)

    def go_home(self):
        if not self.is_stopped:
            print("Home command issued")
            self.is_command_available = True
            self.command_type = MiscType.Home

    def stop_and_cancel(self):
        if self.is_stopped:
            self.Cancel()
        else:
            self.Stop()

        self.update_text()

    def start_and_resume(self):
        if self.is_stopped:
            self.Resume()
        else:
            self.Start()

        self.update_text()

    def Stop(self):
        print("Stop command issued")
        self.is_stopped = True
        self.is_command_available = True
        self.command_type = MiscType.Stop

    def Resume(self):
        print("Resume command issued")
        self.is_stopped = False
        self.is_command_available = True
        self.command_type = MiscType.Resume

    def Start(self):
        print("Start command issued")
        self.is_stopped = False
        self.is_command_available = True
        self.command_type = MiscType.Start

    def Cancel(self):
        print("Cancel command issued")
        self.is_stopped = False
        self.is_command_available = True
        self.command_type = MiscType.CancelMotion

    def update_text(self):

        if self.is_stopped:
            self.StopAndCancelButton.config(text="Cancel")
            self.StartAndResumeButton.config(text="Resume")
        else:
            self.StopAndCancelButton.config(text="Stop")
            self.StartAndResumeButton.config(text="Start")

    def set_label_text(self, text : str):
        self.MenuImgLbl.config(text=text)

    def forget_all(self):
        self.MenuImgLbl.grid_forget()
        self.HomeButton.grid_forget()
        self.StopAndCancelButton.grid_forget()
        self.StartAndResumeButton.grid_forget()

    def disable_image(self):
        self.is_image_disabled = True
        self.forget_all()
        self.build()

    def enable_image(self):
        self.is_image_disabled = False
        self.forget_all()
        self.build()

    def build(self):
        i = 0
        if not self.is_image_disabled:
            self.MenuImgLbl.grid(row = 0, column = 0, columnspan=3, sticky="nsew", padx=25, pady=10)
            i = 1

        self.HomeButton.grid(row = i, column = 0, sticky="nsew", padx=25, pady=10)
        self.StopAndCancelButton.grid(row = i, column = 1, sticky="nsew", padx=25, pady=10)
        self.StartAndResumeButton.grid(row = i, column = 2, sticky="nsew", padx=25, pady=10)
