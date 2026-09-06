import tkinter as tk
from UI.UI_blocks.dynamic_entries import DynamicNumberEntry
from UI.UI_tools.field_validators import *
from Configuration.Distribution import ParamDistributor
import rclpy

class ConfigUI(tk.Frame):

    root : tk.Tk = None

    # label text

    link_labels_txt = [
        "Link 1 (Back Arm)",
        "Link 2 (Forearm)",
        "Link 3 (Hand)" ]

    joint_labels_txt = [
        "Joint 1 (Shoulder)",
        "Joint 2 (Shoulder)",
        "Joint 3 (Elbow)",
        "Joint 4 (Wrist)",
        "Joint 5 (Wrist)" ]

    linear_ik_labels_txt = [
        "P",
        "I",
        "D" ]

    Home_labels_txt = [
        "j1",
        "j2",
        "j3",
        "j4",
        "j5" ]

    # labels

    link_labels  : list[tk.Label] = []
    joint_labels : list[tk.Label] = []
    home_labels  : list[tk.Label] = []
    linear_ik_labels : list[tk.Label] = []

    column_labels : list[tk.Label] = []

    # Components

    link_entries : list[DynamicNumberEntry] = []
    joint_entries : list[DynamicNumberEntry] = []
    home_entries : list[DynamicNumberEntry] = []
    linear_ik_entries : list[DynamicNumberEntry] = []

    # Buttons

    UpdateButton : tk.Button = None
    WriteButton : tk.Button = None

    # ressource 

    Distributor : ParamDistributor = None

    # For pure structure

    is_command_available : bool = False

    def __init__(self, root : tk.Tk):

        self.root = root
        self.Distributor = ParamDistributor()
        super().__init__()

        self.grid_propagate(False)

        # Link

        self.column_labels.append(tk.Label(
            self,
            text="Links"
        ))

        self.column_labels[0].grid(row = 0, column = 0, columnspan = 2, padx = 5, pady = 5)

        for i in range(3):

            l = tk.Label(
                self,
                text=self.link_labels_txt[i]
                )
            l.id = i
            l.parent = self
            self.link_labels.append(l)

            e = DynamicNumberEntry(root = self)
            e.id = i
            e.config(width=10)
            var = self.Distributor.config["links"][f"l{i+1}"]
            e.delete(0, tk.END)
            e.insert(0, str(var))
            e.field_value = var
            self.link_entries.append(e)

            l.grid(row = i+1, column = 0, padx = 5, pady = 5)
            e.grid(row = i+1, column = 1, padx = 5, pady = 5)

        # Joint

        self.column_labels.append(tk.Label(
            self,
            text="[min]    Joints    [max]"
        ))

        self.column_labels[1].grid(row = 0, column = 3, columnspan = 2, padx = 5, pady = 5)

        for i in range(5):

            l = tk.Label(
                self,
                text=self.joint_labels_txt[i]
                )
            l.id = i
            l.parent = self
            self.joint_labels.append(l)

            e = DynamicNumberEntry(root = self)
            e.id = i
            e.config(width=10)
            var = self.Distributor.config["joint_limits"][f"j{i+1}"]["min"]
            e.delete(0, tk.END)
            e.insert(0, str(var))
            e.field_value = var
            self.joint_entries.append(e)

            l.grid(row = i+1, column = 2, padx = 5, pady = 5)
            e.grid(row = i+1, column = 3, padx = 5, pady = 5)

            e = DynamicNumberEntry(root = self)
            e.id = i
            e.config(width=10)
            var = self.Distributor.config["joint_limits"][f"j{i+1}"]["max"]
            e.delete(0, tk.END)
            e.insert(0, str(var))
            e.field_value = var
            self.joint_entries.append(e)

            e.grid(row = i+1, column = 4, padx = 5, pady = 5)

        # Home

        self.column_labels.append(tk.Label(
            self,
            text="Home Position"
        ))

        self.column_labels[2].grid(row = 0, column = 5, columnspan = 2, padx = 5, pady = 5)
        
        for i in range(5):

            l = tk.Label(
                self,
                text=self.Home_labels_txt[i]
                )
            l.id = i
            l.parent = self
            self.home_labels.append(l)

            e = DynamicNumberEntry(root = self)
            e.id = i
            e.config(width=10)

            var = self.Distributor.config["home_position"][f"j{i+1}"]
            e.delete(0, tk.END)
            e.insert(0, str(var))
            e.field_value = var

            self.home_entries.append(e)

            l.grid(row = i+1, column = 5, padx = 5, pady = 5)
            e.grid(row = i+1, column = 6, padx = 5, pady = 5)

        # Linear IK 

        self.column_labels.append(tk.Label(
            self,
            text="Linear IK"
        ))

        self.column_labels[3].grid(row = 0, column = 7, columnspan = 2, padx = 5, pady = 5)

        for i in range(3):

            l = tk.Label(
                self,
                text=self.linear_ik_labels_txt[i]
                )
            l.id = i
            l.parent = self
            self.linear_ik_labels.append(l)

            e = DynamicNumberEntry(root = self)
            e.id = i
            e.config(width=10)

            var = self.Distributor.config["linear_IK_params"][f"{self.linear_ik_labels_txt[i]}"]
            e.delete(0, tk.END)
            e.insert(0, str(var))
            e.field_value = var

            self.linear_ik_entries.append(e)

            l.grid(row = i+1, column = 7, padx = 5, pady = 5)
            e.grid(row = i+1, column = 8, padx = 5, pady = 5)

        # Buttons 

        UpdateButton = tk.Button(
            self,
            text="Update",
            command=self.update_config
        )

        UpdateButton.grid(row = 7, column = 0, columnspan = 2, padx = 5, pady = 5)

        WriteButton = tk.Button(
            self,
            text="Write",
            command=self.write_config
        )

        WriteButton.grid(row = 7, column = 2, columnspan = 2, padx = 5, pady = 5)


    def update_config(self, do_publish = True):
        # Update the configuration from the entries
        for i in range(3):
            self.Distributor.set_link_config(
                l1=float(self.link_entries[0].get()),
                l2=float(self.link_entries[1].get()),
                l3=float(self.link_entries[2].get())
            )

        for i in range(5):
            self.Distributor.set_joint_config(
                joint_id=i+1,
                min=float(self.joint_entries[i*2].get()),
                max=float(self.joint_entries[i*2 + 1].get())
            )

        self.Distributor.set_linear_config(
            p=float(self.linear_ik_entries[0].get()),
            i=float(self.linear_ik_entries[1].get()),
            d=float(self.linear_ik_entries[2].get())
        )

        for i in range(5):
            self.Distributor.config["home_position"][f"j{i+1}"] = float(self.home_entries[i].get())     

        if do_publish:
            self.Distributor.publish_config()

    def write_config(self):
        # Write the configuration to the file
        self.update_config(do_publish = False)  
        self.Distributor.write_config()