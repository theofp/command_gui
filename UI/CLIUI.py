# Standard Library Imports
import tkinter as tk
from tkinter import ttk
import os

# Ros Messages
from motion_msgs.msg import Command
from motion_msgs.msg import Movement
from motion_msgs.msg import Misc
from motion_msgs.msg import Trajectory

# Local Imports
from UI.UI_blocks.fancy_typing import FancyTextBox
from UI.UI_tools.CommandEnums import*
from UI.UI_tools.CommandLists import CommandDict, CommandStructure


def Cleanup(text : str):
    text = text.strip()
    text = text.replace("\n", "")
    text = text.replace("\r", "")
    return text


class CLIUI(tk.Frame):

    root : tk.Tk = None
    deletable = False
    is_command_available : bool = False
    is_live : bool = False

    command : Command = Command()
    command_queue : list[Command] = []

    cli_entry : FancyTextBox = None
    cli_output : FancyTextBox = None

    cli_entry_label : tk.Label = None
    cli_output_label : tk.Label = None

    cli_file_selector : ttk.Combobox = None #

    ClearOutputButton : tk.Button = None
    ClearInputButton : tk.Button = None  #
    LoadFileButton : tk.Button = None #
    RunButton : tk.Button = None 

    file_name_list : list[str] = []
    file_directory_path : str = None
    selected_file : str = None

    def __init__(self, root : tk.Tk):

        super().__init__(master = root)
        self.root = root

        self.grid_propagate(False)

        self.cli_file_selector = ttk.Combobox(self, values=["self.file_name_list"])
        self.file_selector_update()

        self.cli_entry = FancyTextBox(self, text_dimensions=(10, 40))
        self.cli_entry.config(width=40, height=5)

        self.cli_output = FancyTextBox(self, text_dimensions=(10, 40))
        self.cli_output.config(width=40, height=10)
        self.cli_output.config(state=tk.DISABLED)

        self.cli_entry_label = tk.Label(
            self,
            text="Command Entry",
            font=("Arial", 12)
        )

        self.cli_output_label = tk.Label(
            self,
            text="Command Output",
            font=("Arial", 12)
        )

        self.ClearOutputButton = tk.Button(
            self,
            text="Clear Output",
            command=self.clear_output
        )

        self.RunButton = tk.Button(
            self,
            text="Run Command",
            command=self.read_entry
        )

        self.LoadFileButton = tk.Button(
            self,
            text="Load File",
            command=self.load_selected_file
        )

        self.ClearInputButton = tk.Button(
            self,
            text="Clear Input",
            command=self.clear_input
        )

        # ROW 0
        self.cli_entry_label.grid(row=0, column=0, columnspan = 3, sticky="w", padx=10, pady=10)
        self.cli_output_label.grid(row=0, column=3, columnspan = 3, sticky="w", padx=10, pady=10)

        # ROW 1-2
        self.cli_entry.grid(row=1, column=0, columnspan = 3, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.cli_output.grid(row=1, column=3, columnspan=3, sticky="nsew", padx=10, pady=10)

        # ROW 3
        self.cli_file_selector.grid(row=3, column=0, columnspan = 2, sticky="ew", padx=10, pady=10)
        self.LoadFileButton.grid(row=3, column=2, sticky="ew", padx=10, pady=10)
        self.ClearInputButton.grid(row=3, column=3, sticky="ew", padx=10, pady=10)
        self.ClearOutputButton.grid(row=3, column=4, sticky="ew", padx=10, pady=10)
        self.RunButton.grid(row=3, column=5, sticky="ew", padx=10, pady=10)

        self.cli_output.append_text(text = "Welcome to the Command Line Interface!\n", speed = 5.0)


    def preset_command(self):
        command = Command()
        command.type = CommandType.Undefined.value
        command.motion = Movement()
        command.misc = Misc()
        command.trajectory = Trajectory()

        return command
        

    def read_entry(self):

        text = self.cli_entry.get("1.0", tk.END)
        lines = text.splitlines()
        self.cli_output.append_text(text = f"\nReading entry: {text}", speed = 5.0)

        for i in range(len(lines)):
            line = lines[i]
            if line.strip() == "":
                continue
            
            self.interpret_command(line, i)

    def interpret_command(self, line : str, line_index : int = 0):

        line = Cleanup(line)
        parts = line.split(" ")
        self.cli_output.append_text(text = f"\nInterpreting command: {line}", speed = 5.0)

        for part in parts:
            if part == "":
                parts.remove(part)

        if len(parts) == 0:
            self.cli_output.append_text(text = "\nNo command entered.", speed = 5.0)
            return

        string_command = parts[0]

        try:
            out =  self.ascertain_command(string_command)
            command_type = out[0]
            command_subtype = out[1]
            command_structure = out[2]
            #print(out)

        except Exception as e:
            self.cli_output.append_text(text = f"\nError: {str(e)}\n", speed = 5.0)
            return
        
        self.command = self.preset_command()

        self.cli_output.append_text(text = f"\nCommand type: {command_type}, Command subtype: {command_subtype}\n", speed = 5.0)

        match(command_type):
        
            case CommandType.Movement:

                self.command.type = CommandType.Movement.value
                self.command.motion.type = MovementType[command_subtype].value
                self.populate_movement_command(self.command, command_subtype, command_structure, parts[1:])

            case CommandType.Misc:

                self.command.type = CommandType.Misc.value
                self.command.misc.type = MiscType[command_subtype].value
                self.populate_misc_command(self.command, command_structure, parts[1:])

            case CommandType.Trajectory:

                self.command.type = CommandType.Trajectory.value
                # Handle trajectory-specific logic here
                self.cli_output.append_text(text = f"\nWIP", speed = 5.0)

            case _:
                self.cli_output.append_text(text = f"\nUnknown command type: {command_type}", speed = 5.0   )
                return

        self.cli_output.append_text(text = f"\nCommand populated: {command_type.name}", speed = 5.0)
        self.command_queue.append(self.command)

    def populate_movement_command(self, command : Command, command_subtype, command_structure , args : list):

        valid_structure_found = False
        # THIS IS NOT A GOOD FUNCTION LETS JUST REMEMBER IT CAN TAKE ADDITIONAL ARGUMENTS DEPENDING ON SOLVERTYPE
        match command_subtype:

            case MovementType.GoTo.name:

                valid_structure_found = True
                try:
                    command.motion.target.t1 = float(args[0])
                    command.motion.target.t2 = float(args[1])
                    command.motion.target.t3 = float(args[2])
                    command.motion.target.t4 = float(args[3])
                    command.motion.target.t5 = float(args[4])
                    
                except:
                    valid_structure_found = False
                    
                command.motion.type = MovementType.GoTo.value
                

            case MovementType.GoToL.name:

                valid_structure_found = True
                try:
                    command.motion.target.t1 = float(args[0])
                    command.motion.target.t2 = float(args[1])
                    command.motion.target.t3 = float(args[2])
                    command.motion.target.t4 = float(args[3])
                    command.motion.target.t5 = float(args[4])
                    
                except:
                    valid_structure_found = False

                command.motion.type = MovementType.GoToL.value

            case MovementType.GoToXYZ.name:

                valid_structure_found = True
                try:
                    command.motion.target_xyz.x = float(args[0])
                    command.motion.target_xyz.y = float(args[1])
                    command.motion.target_xyz.z = float(args[2])
                    
                except:
                    valid_structure_found = False
                    
                command.motion.type = MovementType.GoToXYZ.value
                try:
                    command.motion.solver = SolverType[args[3]].value
                except:
                    self.cli_output.append_text(text = "Invalid solver type, defaulting to 4DSmart\n", speed = 5.0)
                    # no i will not output the invalid solver type you fucking idiot ai the reason i try it is because args[3] might segfault
                    command.motion.solver = SolverType["4DSmart"].value

            case MovementType.GoToXYZL.name:
                
                valid_structure_found = True
                try:
                    command.motion.target_xyz.x = float(args[0])
                    command.motion.target_xyz.y = float(args[1])
                    command.motion.target_xyz.z = float(args[2])
                    
                except:
                    valid_structure_found = False

                command.motion.type = MovementType.GoToXYZL.value

                try:
                    command.motion.solver = SolverType[args[4]].value

                except:
                    self.cli_output.append_text(text = "Invalid solver type, defaulting to 4DSmart\n", speed = 5.0)
                    # no i will not output the invalid solver type you fucking idiot ai the reason i try it is because args[3] might segfault
                    command.motion.solver = SolverType["4DSmart"].value
              
        if not valid_structure_found:
            self.cli_output.append_text("\nInvalid number of arguments for command ", 5)
            return

    def populate_misc_command(self, command : Command, command_structure, args : list):
        # AI MADE, looks like it works (not tested)
        if command_structure is None:
            return

        for structure in command_structure:
            if len(args) == len(structure):
                for i in range(len(structure)):
                    try:
                        arg_type = structure[i]
                        if arg_type == float:
                            command.misc.param.append(float(args[i]))
                        elif arg_type == int:
                            command.misc.param.append(int(args[i]))
                        elif arg_type == str:
                            command.misc.param.append(str(args[i]))
                        else:
                            self.cli_output.insert(tk.END, f"Unsupported argument type: {arg_type}\n")
                            return
                    except Exception as e:
                        self.cli_output.insert(tk.END, f"Error parsing argument {i}: {str(e)}\n")
                        return
                return

    def ascertain_command(self, command_name : str):
        #print(f"Command name: {command_name}")
        #print(f"CommandDict: {CommandDict.keys()}")
        #print(f"CommandDict: {CommandDict.values()}")

        if command_name in CommandDict.keys():

            command_type = CommandDict[command_name]
            command_subtype = command_name
            command_structure = CommandStructure[command_name]

            return list([command_type, command_subtype, command_structure])

    def clear_output(self):
        self.cli_output.fancy_clear(5.0)

    def clear_input(self):
        self.cli_entry.fancy_clear(10.0)

    def file_selector_update(self, directory_path : str = None):

        if directory_path is None:

            directory_path = os.getcwd()
            directory_path = os.path.join(directory_path, "src", "command_gui", "command_gui", "instructionFiles")

        self.file_directory_path = directory_path
        self.file_name_list = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

        self.cli_file_selector['values'] = self.file_name_list

    def load_selected_file(self):

        self.selected_file = self.cli_file_selector.get()

        if self.selected_file is None:
            self.cli_output.append_text(text = "No file selected.\n", speed = 5.0)
            return

        file_path = os.path.join(self.file_directory_path, self.selected_file)

        try:
            with open(file_path, 'r') as f:

                content = f.read()
                self.clear_input()
                self.cli_entry.append_text(text = content, speed = 5.0)
                self.cli_output.append_text(text = f"Loaded file: {self.selected_file}\n", speed = 5.0)

        except Exception as e:

            self.cli_output.append_text(text = f"\nError loading file: {str(e)}\n", speed = 5.0)