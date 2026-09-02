import tkinter as tk

from pyparsing import line
from tables import Enum
from UI.UI_blocks.fancy_typing import FancyTextBox
from motion_msgs.msg import Command
from motion_msgs.msg import Movement
from motion_msgs.msg import Misc
from motion_msgs.msg import Trajectory
import inspect
from UI.UI_tools.CommandEnums import*
from UI.UI_tools.CommandLists import Commands, CommandStructure


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

    active_command : Command = None
    command_queue : list[Command] = []

    cli_entry : FancyTextBox = None
    cli_output : FancyTextBox = None

    ClearButton : tk.Button = None
    RunButton : tk.Button = None

    def __init__(self, root : tk.Tk):

        super().__init__(master = root)
        self.root = root

        self.grid_propagate(False)

        self.cli_entry = FancyTextBox(self, text_dimensions=(10, 40))
        self.cli_entry.config(width=40, height=5)

        self.cli_output = FancyTextBox(self, text_dimensions=(10, 40))
        self.cli_output.config(width=40, height=10)
        self.cli_output.config(state=tk.DISABLED)

        self.ClearButton = tk.Button(
            self,
            text="Clear Output",
            command=self.clear_output
        )

        self.RunButton = tk.Button(
            self,
            text="Run Command",
            command=self.read_entry
        )

        self.cli_entry.grid(row=0, column=0, rowspan=2, sticky="nsew", padx=10, pady=10)
        self.cli_output.grid(row=1, column=1, columnspan=2, sticky="nsew", padx=10, pady=10)

        self.ClearButton.grid(row=0, column=1, sticky="ew", padx=10, pady=10)
        self.RunButton.grid(row=0, column=2, sticky="ew", padx=10, pady=10)


    def preset_command(self):

        self.active_command.type = CommandType.Undefined.value
        self.active_command.motion = Movement()
        self.active_command.misc = Misc()
        self.active_command.trajectory = Trajectory()

    def read_entry(self):

        text = self.cli_entry.get("1.0", tk.END)
        lines = text.splitlines()

        for i in range(len(lines)):
            line = lines[i]
            if line.strip() == "":
                continue
            self.cli_output.insert(tk.END, f"> {line}\n")
            self.interpret_command(line, i)

    def interpret_command(self, line : str, line_index : int = 0):

        line = Cleanup(line)
        parts = line.split(" ")

        for part in parts:
            if part == "":
                parts.remove(part)

        if len(parts) == 0:
            self.cli_output.insert(tk.END, "No command entered.\n")
            return

        string_command = parts[0]
        try:
            command_type, command_subtype, command_structure =  self.ascertain_command(string_command)
        except Exception as e:
            self.cli_output.insert(tk.END, f"Error: {str(e)}\n")
            return

        command = self.preset_command()

        case = CommandType[command_type]

        match(case):
        
            case CommandType.Movement:

                command.type = CommandType.Movement.value
                command.motion.type = MovementType[command_subtype].value
                self.populate_movement_command(command, command_subtype, command_structure, parts[1:])

            case CommandType.Misc:

                command.type = CommandType.Misc.value
                command.misc.type = MiscType[command_subtype].value
                self.populate_misc_command(command, command_structure, parts[1:])

            case CommandType.Trajectory:

                command.type = CommandType.Trajectory.value
                # Handle trajectory-specific logic here

            case _:
                self.cli_output.insert(tk.END, f"Unknown command type: {command_type}\n")
                return

    def populate_movement_command(self, command : Command, command_subtype, command_structure , args : list):

        valid_structure_found = False
        # THIS IS NOT A GOOD FUNCTION LETS JUST REMEMBER IT CAN TAKE ADDITIONAL ARGUMENTS DEPENDING ON SOLVERTYPE
        match command_subtype:

            case MovementType.GoTo.name:

                valid_structure_found = True
                for i in range(5):
                    try:
                        command.motion.target.append(float(args[i]))
                        
                    except:
                        valid_structure_found = False
                        break

                command.motion.type = MovementType.GoTo.value
                

            case MovementType.GoToL.name:

                valid_structure_found = True
                for i in range(5):
                    try:
                        command.motion.target.append(float(args[i]))
                        
                    except:
                        valid_structure_found = False
                        break
                command.motion.type = MovementType.GoToL.value

            case MovementType.GoToXYZ.name:

                valid_structure_found = True
                for i in range(3):
                    try:
                        command.motion.target.append(float(args[i]))
                        
                    except:
                        valid_structure_found = False
                        break
                command.motion.type = MovementType.GoToXYZ.value
                try:
                    command.motion.solver = SolverType[args[3]].value
                except:
                    self.cli_output.insert(tk.END, f"Invalid solver type, defaulting to 4DSmart") 
                    # no i will not output the invalid solver type you fucking idiot ai the reason i try it is because args[3] might segfault
                    command.motion.solver = SolverType["4DSmart"].value

            case MovementType.GoToXYZL.name:
                
                valid_structure_found = True
                for i in range(4):
                    try:
                        command.motion.target.append(float(args[i]))
                        
                    except:
                        valid_structure_found = False
                        break
                command.motion.type = MovementType.GoToXYZL.value
                try:
                    command.motion.solver = SolverType[args[4]].value
                except:
                    self.cli_output.insert(tk.END, f"Invalid solver type, defaulting to 4DSmart") 
                    # no i will not output the invalid solver type you fucking idiot ai the reason i try it is because args[3] might segfault
                    command.motion.solver = SolverType["4DSmart"].value
              
        if not valid_structure_found:
            self.cli_output.insert(tk.END, f"Invalid number of arguments for command \n")
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

    def ascertain_command(self, command : str):

        if command in Commands:
            command_type = Commands[command]
            command_subtype = command
            command_structure = CommandStructure[command]

            return command_type, command_subtype, command_structure

    def clear_output(self):
        self.cli_output.delete("1.0", tk.END)

            