import tkinter as tk 
import os
from UI.alphabet_support import SpecialChars, SpecialCharsNoNums
from typing import Callable, Any, Union

class DynamicTextEntry(tk.Text):

    validator : Callable[[str],bool] = None
    no_nums : bool = True
    field_value : Any = None
    is_border_red : bool = False   
    is_validator_bound : bool = False 

    def __init__(self, root, text_dimensions=(10, 100), validator : Callable[[str],bool] = None ,*args, **kwargs):
        super().__init__(root, width = text_dimensions[1], height = text_dimensions[0], *args, **kwargs)
        self.text_dimensions = text_dimensions

        if validator is not None:
            self.validator = validator
            self.is_validator_bound = True
            self.bind("<KeyPress>", self.field_validation)
            self.bind("<FocusIn>", lambda event : self.highlight(event_type = "focus"))
            self.bind("<FocusOut>", lambda event : self.highlight(event_type = "unfocus"))

    def field_validation(self, event : tk.Event, validator : Callable[[str],bool] = None, color : str = "red"):

        if validator is None and self.is_validator_bound:
            validator = self.validator
        elif validator is None and not self.is_validator_bound:
            print("No validator bound to this object")
            return
            # This should be an exception (handled by an)

        entry = self.get("1.0", "end")
        typeset_entry = self.typeset(entry, self.no_nums)

        if validator(typeset_entry):
            self.field_value = typeset_entry
            self.highlight(color = "white", event_type = "unhighlight")
        else:
            self.is_border_red = True
            self.highlight(color = color)
        
        pass

    def set_validator(self, validator : Callable[[str], bool]):
        self.validator = validator
        self.is_validator_bound = True
        self.bind("<KeyPress>", self.field_validation)        

    def typeset(self, entry : str, no_nums : bool = True)->str:
        typeset_entry : str = ""
        if no_nums:
            self.special_chars = SpecialCharsNoNums()
        else:
            self.special_chars = SpecialChars()

        lentry = list(entry)

        for i in range(len(lentry)):  # slight optimization, not having to create a new strin gon every loop iteration
            if lentry[i] in self.special_chars:
                lentry[i] = ""

        typeset_entry = "".join(lentry)            
        return typeset_entry
    
    def highlight(self, color : str = "red", event_type : str = None):

        if event_type is None:
            self.config(highlightbackground=color, highlightcolor=color, highlightthickness=2)

        if event_type == "focus":
            self.config(highlightthickness=2)

        if event_type == "unfocus":
            self.config(highlightthickness=1)

        if event_type == "unhighlight":
            self.config(highlightbackground="white", highlightcolor="white", highlightthickness=0)

class DynamicEntry(tk.Entry):
    
    validator : Callable[[str],bool] = None
    no_nums : bool = True
    field_value : Any = None
    is_border_red : bool = False   
    is_validator_bound : bool = False 
    id = None

    def __init__(self, root, text_dimensions = 50, validator : Callable[[str],bool] = None ,*args, **kwargs):
        super().__init__(root, width = text_dimensions, *args, **kwargs)
        self.text_dimensions = text_dimensions

        if validator is not None:
            self.validator = validator
            self.is_validator_bound = True
            self.bind("<KeyPress>", self.field_validation)
            self.bind("<FocusIn>", lambda : self.highlight(event_type = "focus"))
            self.bind("<FocusOut>", lambda : self.highlight(event_type = "unfocus"))

    def field_validation(self, event : tk.Event, validator : Callable[[str],bool] = None, color : str = "red"):

        if validator is None and self.is_validator_bound:
            validator = self.validator
        elif validator is None and not self.is_validator_bound:
            print("No validator bound to this object")
            return
            # This should be an exception (handled by an)

        entry = self.get()
        typeset_entry = self.typeset(entry, self.no_nums)

        if validator(typeset_entry):

            self.field_value = typeset_entry
            self.highlight(color = "white", event_type = "unhighlight")
        else:
            self.is_border_red = True
            self.highlight(color = color)
        
        pass

    def set_validator(self, validator : Callable[[str], bool]):
        self.validator = validator
        self.is_validator_bound = True
        self.bind("<KeyPress>", self.field_validation)
        self.bind("<FocusIn>", lambda : self.highlight(event_type = "focus"))
        self.bind("<FocusOut>", lambda : self.highlight(event_type = "unfocus"))


    def typeset(self, entry : str, no_nums : bool = True)->str:
        typeset_entry : str = ""

        if no_nums:
            self.special_chars = SpecialCharsNoNums()
        else:
            self.special_chars = SpecialChars()

        lentry = list(entry)

        for i in range(len(lentry)):  # slight optimization, not having to create a new strin gon every loop iteration
            if lentry[i] in self.special_chars:
                lentry[i] = ""

        typeset_entry = "".join(lentry)            
        return typeset_entry
    
    def highlight(self, color : str = "red", event_type : str = None):
        if event_type is None:
            self.config(highlightbackground=color, highlightcolor=color, highlightthickness=2)

        if event_type == "focus":
            self.config(highlightthickness=2)

        if event_type == "unfocus":
            self.config(highlightthickness=1)

        if event_type == "unhighlight":
            self.config(highlightbackground="white", highlightcolor="white", highlightthickness=0)

class Dynamizer():

    # This makes the above classes obsolete and is a more flexible solution
    # i will however keep the above classes at least until i've tested this one

    parent : Union[tk.Text,tk.Entry] = None # says parent but you can pass any widget regardless of position in the hierarchy
    validator : Callable[[str],bool] = None
    no_nums : bool = True
    value : Any = None
    validator_support_data : Any = None
    do_block : bool = False # blocking is only supported for my custom classes


    def __init__(self, parent, validator : Callable[[str],bool] = None, no_nums : bool = True, do_block : bool = True, validator_support_data : Any = None):
        self.parent = parent
        self.validator = validator
        self.no_nums = no_nums

        if no_nums:
            self.special_chars = SpecialCharsNoNums()
        else:
            self.special_chars = SpecialChars()

        if self.validator is not None:
            self.bind_validator()

        if validator_support_data is not None:
            self.validator_support_data = validator_support_data

        if do_block:
            self.do_block = True

    def bind_validator(self, validator : Callable[[str],bool] = None):

        if validator is None:
            if self.validator is None:
                print("No validator bound to this object")
                return
        else:
            self.validator = validator

        if isinstance(self.parent, tk.Entry):
            print("It's an entry!")
            self.parent.bind("<KeyPress>", lambda event : self.validate_entry_delay_wrapper(color="red", event=event))
            self.parent.bind("<FocusIn>", lambda event : self.highlight(event_type = "focus", event=event))
            self.parent.bind("<FocusOut>", lambda event : self.highlight(event_type = "unfocus", event=event))

        elif isinstance(self.parent, tk.Text):
            print("It's a text!")
            self.parent.bind("<KeyPress>", lambda event : self.validate_text_delay_wrapper(color="red", event=event))
            self.parent.bind("<FocusIn>", lambda event : self.highlight(event_type = "focus", event=event))
            self.parent.bind("<FocusOut>", lambda event : self.highlight(event_type = "unfocus", event=event))

        else:
            print("Parent widget not supported")

    def highlight(self, color : str = "red", event_type : str = None, event : tk.Event = None):
        if event_type is None:
            self.parent.config(highlightbackground=color, highlightcolor=color, highlightthickness=2)
        if event_type == "focus":
            self.parent.config(highlightthickness=2)
        if event_type == "unfocus":
            self.parent.config(highlightthickness=1)
        if event_type == "unhighlight":
            self.parent.config(highlightbackground="white", highlightcolor="white", highlightthickness=0)

    def validate_entry_delay_wrapper(self, event : tk.Event, color : str = "red"):
        self.parent.after(50, lambda : self.validate_entry(event, color))
    
    def validate_text_delay_wrapper(self, event : tk.Event, color : str = "red"):
        self.parent.after(50, lambda : self.validate_text(event, color))

    # Why do we need the wrappers to delay action? because the event is triggered before the text is updated

    def validate_entry(self, event : tk.Event, color : str = "red"):
        entry = self.parent.get()
        is_validated = False
        value = None
        
        if self.validator_support_data is not None:
            is_validated, value = self.validator(self.typeset(entry), self.validator_support_data)
        else:
            is_validated, value = self.validator(self.typeset(entry))

        if is_validated:
            self.highlight(color = "white", event_type = "unhighlight")
            self.value = value
        else:
            self.highlight(color = color)

    def validate_text(self, event : tk.Event, color : str = "red"):
        entry = self.parent.get("1.0", "end")
        is_validated = False
        value = None

        if self.validator_support_data is not None:
            is_validated, value = self.validator(self.typeset(entry), self.validator_support_data)
        else:
            is_validated, value = self.validator(self.typeset(entry))

        if is_validated:
            self.highlight(color = "white", event_type = "unhighlight")
        else:
            self.highlight(color = color)

    def typeset(self, entry : str)->str:
        typeset_entry : str = ""

        lentry = list(entry)

        for i in range(len(lentry)):
            if lentry[i] in self.special_chars:
                #print("Special char found " + str(repr(lentry[i])[1:-1]))
                lentry[i] = ""
        typeset_entry = "".join(lentry)
        #print(typeset_entry + " is there a line break")
        # hint there is no line break
        return typeset_entry
    
class DynamizerAsAttr(Dynamizer):
    
    def __init__(self, parent, validator : Callable[[str],bool] = None, no_nums : bool = True, validator_support_data : Any = None):
        super().__init__(parent, validator, no_nums, validator_support_data)

    def get_value(self):
        if isinstance(self,Dynamizer):
            return self.value
        else:
            attr_list = list(dir(self))
            for attr in attr_list:
                if isinstance(attr, Dynamizer):
                    return attr.get_value()
        # This is heavy but since it should only be querried once every so often it should be aight


class DynamicNumberEntry(tk.Entry):
    
    validator : Callable[[str],bool] = None
    no_nums : bool = False
    field_value : Any = None
    is_border_red : bool = False   
    is_validator_bound : bool = False 
    id = None

    def __init__(self, root, text_dimensions = 50, validator : Callable[[str],bool] = None ,*args, **kwargs):
        super().__init__(root, width = text_dimensions, *args, **kwargs)
        self.text_dimensions = text_dimensions

        if validator is not None:
            self.validator = validator
            self.is_validator_bound = True
            self.bind("<KeyPress>", self.field_validation_delay_wrapper(event=None, validator=None, color=None))
            self.bind("<FocusIn>", lambda : self.highlight(event_type = "focus"))
            self.bind("<FocusOut>", lambda : self.highlight(event_type = "unfocus"))

    def field_validation_delay_wrapper(self, event : tk.Event, validator : Callable[[str],bool] = None, color : str = "red"):
        self.after(50, lambda : self.field_validation(event, validator = validator, color = color))

    def field_validation(self, event : tk.Event, validator : Callable[[str],bool] = None, color : str = "red"):

        if validator is None and self.is_validator_bound:
            validator = self.validator
        elif validator is None and not self.is_validator_bound:
            print("No validator bound to this object")
            return
            # This should be an exception (handled by an) # an what?

        entry = self.get()
        typeset_entry = self.typeset(entry)

        if validator(typeset_entry):

            self.field_value = typeset_entry
            self.highlight(color = "white", event_type = "unhighlight")
            self.is_border_red = False
        else:
            self.is_border_red = True
            self.highlight(color = color)
        
        pass

    def set_validator(self, validator : Callable[[str], bool]):
        self.validator = validator
        self.is_validator_bound = True
        self.bind("<KeyPress>", self.field_validation)
        self.bind("<FocusIn>", lambda : self.highlight(event_type = "focus"))
        self.bind("<FocusOut>", lambda : self.highlight(event_type = "unfocus"))


    def typeset(self, entry : str, no_nums : bool = False)->str:
        typeset_entry : str = ""

        if no_nums:
            self.special_chars = SpecialCharsNoNums()
        else:
            self.special_chars = SpecialChars()

        lentry = list(entry)

        for i in range(len(lentry)):  # slight optimization, not having to create a new string on every loop iteration
            if lentry[i] in self.special_chars:
                lentry[i] = ""

        typeset_entry = "".join(lentry)            
        return typeset_entry
    
    def highlight(self, color : str = "red", event_type : str = None):
        if event_type is None:
            self.config(highlightbackground=color, highlightcolor=color, highlightthickness=2)

        if event_type == "focus":
            self.config(highlightthickness=2)

        if event_type == "unfocus":
            self.config(highlightthickness=1)

        if event_type == "unhighlight":
            self.config(highlightbackground="white", highlightcolor="white", highlightthickness=0)

    def set_text(self, text):
        self.delete(0, tk.END)
        self.insert(0, f"{float(text):.3f}")