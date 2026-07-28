from UI.UI_blocks.fancy_typing import *
from UI.UI_blocks.paired_widgets import *
from UI.UI_blocks.dynamic_entries import *

def widget_types():
    widget_types = ["SmartText", "DynamicTextBox", "DynamicLabel", "DynamicTextEntry", "DynamicEntry", "Text", "Button", "Label", "Entry"]

# I do plan to add to this xd

def widget_dict():
    
    widget_dict = {
        "SmartText" : SmartText,
        "DynamicTextBox" : FancyTextBox,
        "DynamicLabel" : FancyLabel,
        "DynamicTextEntry" : DynamicTextEntry,
        "DynamicEntry" : DynamicEntry,
        "Text" : tk.Text,
        "Button" : tk.Button,
        "Label" : tk.Label,
        "Entry" : tk.Entry
    }

def basic_widget_list():
    return [tk.Text, tk.Button, tk.Label, tk.Entry, tk.Frame]

def widget_required_attributes(type : str):

    widget_attributes = { # I cannot be asked to do this manually now 
        "SmartText" : ["root : Tk.tk", "is_rooted : bool (Optional)", "root_origin : [row,column] (Optional)", "text_dimensions [height,width]", "do_dynamic_text : bool (Optional)", "do_build : bool (Optional)"],
        "DynamicTextBox" : ["root : Tk.tk", "text", "text_dimensions : [height,width]", "font : Font (Optional)"],
        "DynamicLabel" : ["root", "text", "font", "text_dimensions"],
        "DynamicTextEntry" : ["root", "text", "font", "text_dimensions"],
        "DynamicEntry" : ["root", "text", "font"],
        "Text" : ["root", "text", "font"],
        "Button" : ["root", "text", "font"],
        "Label" : ["root", "text", "font"],
        "Entry" : ["root", "text", "font"]
    }

    return widget_attributes[type]