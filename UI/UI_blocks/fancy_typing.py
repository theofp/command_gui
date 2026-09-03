import tkinter as tk 
from tkinter.font import Font
import os
import time
from UI.UI_blocks.fonts import *
from typing import Any

def Speed2Time(speed : float) -> float:
    return 1/(20*speed)

class FancyTextBox(tk.Text):

    font : Font = None

    def __init__(self, master, text_dimensions=(10, 100), *args, **kwargs):
        # Reminder for myself: text width represents the number of characters of width

        super().__init__(master, width = text_dimensions[1], height = text_dimensions[0], *args, **kwargs)
        # through *args and **kwargs we can pass any other arguments to the Text class
        self.text_dimensions = text_dimensions
        self.font = Arial(12)

    def update_text(self, text : str, font : Font = None, speed : float = 1, is_fancy : bool = False):

        original_state = self.cget("state")

        if original_state == "disabled":
            self.config(state="normal")

        if font is not None:
            self.font = font

        self.config(font=self.font)

        if is_fancy:
            self.fancy_clear(speed)

        else:
            self.delete("1.0", "end")

        pause = Speed2Time(speed)

        for char in text:
            if char == "\n" and char == text[-1]:
                break
            self.insert("end", char)
            self.update()
            time.sleep(pause)

        self.config(state=original_state)
    
    def append_text(self, text : str, font : Font = None, speed : float = 1):

        original_state = self.cget("state")

        if original_state == "disabled":
            self.config(state="normal")

        if font is not None:
            self.font = font

        self.config(font=self.font)

        pause = Speed2Time(speed)

        for char in text:
            if char == "\n" and char == text[-1]:
                break
            self.insert("end", char)
            self.update()
            time.sleep(pause)

        self.config(state=original_state)
        
    def fancy_clear(self, speed : float = 1):

        original_state = self.cget("state")

        if original_state == "disabled":
            self.config(state="normal")

        pause = Speed2Time(speed)

        sze = len(self.get("1.0", "end"))

        while sze != 1:
            try:
                self.delete(f"end-2c", "end") # I have no idea why it has to be like this it just has to
            except:
                self.delete("end-1c", "end")
                print("Does this trigger???") # Does not even trigger
            self.update()
            sze = len(self.get("1.0", "end"))
            time.sleep(pause)

        self.config(state=original_state)

    def set_font(self, font : Font):
        self.font = font
        self.config(font=self.font)

class FancyLabel(tk.Label):

    def __init__(self, master, text_dimensions=(10, 100), *args, **kwargs):
        # Reminder for myself: text width represents the number of characters of width

        super().__init__(master, width = text_dimensions[1], height = text_dimensions[0], *args, **kwargs)
        # through *args and **kwargs we can pass any other arguments to the Text class
        self.text_dimensions = text_dimensions
        self.config(width=self.text_dimensions[0], height=self.text_dimensions[1])
        self.font = Arial(12)
        self.config(font=self.font)
        self["text"] = "Default Text"

    def update_text(self, text : str, font : Font = None, speed : float = 1, is_fancy : bool = False):

        if font is not None:
            self.font = font

        self.config(font=self.font)

        if is_fancy:
            self.fancy_clear(speed)

        else:
            self["text"] = ""

        pause = Speed2Time(speed)

        for char in text:
            if char == "\n" and char == text[-1]:
                break
            self["text"] += char
            self.update()
            time.sleep(pause)
    
    def append_text(self, text : str, font : Font = None, speed : float = 1):

        if font is not None:
            self.font = font

        self.config(font=self.font)

        pause = Speed2Time(speed)

        for char in text:
            if char == "\n" and char == text[-1]:
                break
            self["text"] += char
            self.update()
            time.sleep(pause)
        
    def fancy_clear(self, speed : float = 1):

        pause = Speed2Time(speed)

        size = len(self["text"])

        for i in range(size):
            self["text"] = self["text"][:-1]
            self.update()
            time.sleep(pause)

    def set_font(self, font : Font):
        self.font = font
        self.config(font=self.font)

