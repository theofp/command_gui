import tkinter as tk
from tkinter import font

def Arial(size, *args):
    return font.Font(family="Arial", size=size, *args)

def Courier(size, *args):
    return font.Font(family="Courier", size=size, *args)

def Helvetica(size, *args):
    return font.Font(family="Helvetica", size=size, *args)

def Times_New_Roman(size, *args):
    return font.Font(family="Times New Roman", size=size, *args)

def Comic_Sans_MS(size, *args):
    return font.Font(family="Comic Sans MS", size=size, *args)

def Segoe_UI(size, *args):
    return font.Font(family="Segoe UI", size=size, *args)

def Segoe_UI_Light(size, *args):
    return font.Font(family="Segoe UI Light", size=size, *args)

"""
Some of the more relevant args we can pass here are:
    weigth : str = "normal", "bold", "italic"
    slant : str = "roman", "italic"
    underline : int = 0, 1 # 0 is no underline, 1 is underline
    overstrike : int = 0, 1 # 0 is no overstrike, 1 is overstrike overstrike is a line drawn through the middle of the text
"""