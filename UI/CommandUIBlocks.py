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

        self.grid_propagate(False)

        self.solver_type = ttk.Combobox(
            self,
            values=[x.name for x in SolverType],
            state="readonly"
        )

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
                text=self.entry_labels[i],
                width=3
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

  