import tkinter as tk
from typing import Dict, List, Union
import os
from UI_blocks.fancy_typing import FancyTextBox

class SmartText(tk.Frame):

    message_storage : List[str] = list()
    root : Union[tk.Tk, None] = None
    text : Union[tk.Text, FancyTextBox,None] = None
    button_1 : Union[tk.Button, None] = None
    button_2 : Union[tk.Button, None] = None
    text_index : Union[int, None] = None
    has_messages : bool = False
    is_saved : bool = False
    xpad : int = 1
    text_dimensions : List[int] = [2, 90]
    do_dyanmic_text : bool = False
    is_rooted : bool = True

    # I'll be making a temporary copy of this class to check Frame interactions

    def __init__(self, root : tk.Tk, is_rooted : bool = True, text_dimensions : List[int] = [2, 100], do_build : bool = True, do_dynamic_text : bool = False, *args, **kwargs):
        super().__init__()
        self.root = root

        self.xpad = 1

        if not do_dynamic_text:
            self.text = tk.Text(self, height = text_dimensions[0], width = text_dimensions[1])
            self.text.bind("<KeyPress>", self.message_manager)

        else:
            self.text = FancyTextBox(self, text_dimensions = text_dimensions, *args, **kwargs)

        self.button_1 = tk.Button(self, text="Submit Text", command = self.on_click_submit, height = 3, width = text_dimensions[1]//2)

        self.button_2 = tk.Button(self, text="Save Text", command = self.on_click_save, height = 3, width = text_dimensions[1]//2)

        self.is_rooted = is_rooted

        if do_build:
            self.build()

    def build(self):

        if self.is_rooted:
            self.text.grid(row = 0, column = 0, sticky="ew", padx=10, pady=10, columnspan = 2)
            self.button_1.grid(row = 0 + 1, column = 0 , sticky="ew", padx = 10)
            self.button_2.grid(row = 0 + 1, column = 0 + 1, sticky="ew", padx = 10)
        
        else:
            self.text.pack()
            self.button_1.pack()
            self.button_2.pack()
        
        #self.pack()


    def on_click_submit(self):

        msg = self.text.get("1.0", "end")
        print(msg)

        if not self.is_saved:
            self.message_storage.append(msg)

        self.text.delete("1.0", "end")
        self.is_saved = False

        if not self.has_messages:
            self.has_messages = True
            self.text_index = 0

    def on_click_save(self):

        msg = self.text.get("1.0", "end")

        if not self.is_saved and msg != "":

            self.message_storage.append(msg)
            self.text_index = len(self.message_storage) - 1
            self.is_saved = True
            self.has_messages = True

        elif msg != "":
            self.message_storage[self.text_index] = msg
            self.is_saved = True

        pass

    def message_manager(self, event : tk.Event):

        if event.keysym == "Up" and event.state == 20 and self.has_messages:

            print("Key Up Triggered")

            if not self.is_saved:
                self.on_click_save()

            self.text_index = (self.text_index + 1)%len(self.message_storage)
            self.text.delete("1.0", "end")
            self.text.insert("1.0", self.message_storage[self.text_index])

        elif event.keysym == "Down" and event.state == 20 and self.has_messages:

            print("Key Up Triggered")

            if not self.is_saved:
                self.on_click_save()

            self.text_index = (self.text_index - 1)%len(self.message_storage)
            self.text.delete("1.0", "end")
            self.text.insert("1.0", self.message_storage[self.text_index])
        pass


class LabelAndEntry(tk.Frame):

    label : Union[tk.Label, None] = None
    entry : Union[tk.Entry, None] = None
    root : Union[tk.Tk, None] = None
    label_text : str = ""
    entry_text : str = ""
    label_columnspan : int = 1
    entry_columnspan : int = 1
    entry_width : int = 50
    entry_rowspan : int = 1
    label_rowspan : int = 1
    

    def __init__(self, root : tk.Tk, label_text : str = None, entry_text : str = None, 
                 do_build : bool = True, label_columnspan :int = 1, entry_columnspan : int = 1,
                 label_rowspan : int = 1, entry_rowspan : int  = 1, *args, **kwargs):
        super().__init__()
        self.root = root

        self.label = tk.Label(self, *args, **kwargs)
        self.entry = tk.Entry(self, *args, **kwargs)

        if label_text is not None:
            self.label["text"] = label_text 
        if entry_text is not None:
            self.entry.insert("0", f"{entry_text}")
        self.label_columnspan = label_columnspan
        self.entry_columnspan = entry_columnspan
        self.label_rowspan = label_rowspan
        self.entry_rowspan = entry_rowspan

        if do_build:
            self.build()

    def build(self): # y padding should be hadled by the parent frame
        self.label.grid(row = 0, column = 0, sticky="ew", padx = 10, columnspan=self.label_columnspan, rowspan=self.label_rowspan)
        self.entry.grid(row = 0, column = self.label_columnspan + 1, sticky="ew", padx = 10, columnspan=self.entry_columnspan, rowspan=self.entry_rowspan)

    def resize(self,label_columnspan : int = 1, entry_columnspan : int = 1, do_build : bool = True):
        self.label_columnspan = label_columnspan
        self.entry_columnspan = entry_columnspan
        if do_build:
            self.build()

class LabelAndText(tk.Frame):
    # This is not done at all placeholder generated by Copilot
    label : Union[tk.Label, None] = None
    text : Union[tk.Text, None] = None
    root : Union[tk.Tk, None] = None
    label_text : str = ""
    text_text : str = ""
    label_columnspan : int = 1
    text_columnspan : int = 1
    text_width : int = 50
    text_rowspan : int = 1
    label_rowspan : int = 1

    def __init__(self, root : tk.Tk, label_text : str = None, text_text : str = None, do_build : bool = True, label_columnspan : int = 1, text_columnspan : int = 1, label_rowspan : int = 1, text_rowspan : int = 1, *args, **kwargs):
        super().__init__()
        self.root = root
        if label_text is not None:
            self.label = tk.Label(self, text = label_text, *args, **kwargs)
        if text_text is not None:
            self.text = tk.Text(self, text = text_text, *args, **kwargs)
        self.label_columnspan = label_columnspan
        self.text_columnspan = text_columnspan
        self.label_rowspan = label_rowspan
        self.text_rowspan = text_rowspan

        if do_build:
            self.build()

    def build(self):
        self.label.grid(row = 0, column = 0, sticky="ew", padx = 10, columnspan=self.label_columnspan, rowspan=self.label_rowspan)
        self.text.grid(row = 0, column = self.label_columnspan + 1, sticky="ew", padx = 10, columnspan=self.text_columnspan, rowspan=self.text_rowspan)

    def resize(self, label_columnspan : int = 1, text_columnspan : int = 1, do_build : bool = True):   
        self.label_columnspan = label_columnspan
        self.text_columnspan = text_columnspan
        if do_build:
            self.build()