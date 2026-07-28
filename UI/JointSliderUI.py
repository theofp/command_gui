import tkinter as tk
from UI.UI_blocks.dynamic_entries import DynamicNumberEntry
from UI.UI_tools.field_validators import *

class JointSliderUI(tk.Frame):

    root : tk.Tk = None
    n_sliders = 5
    pi = 3.1415
    pi2 = pi/2
    sliders = list() # Tk.Scale objects
    labels = list()  # Tk.Label objects
    entries = list() # UI.DynamicEntry objects

    slider_labels_txt = [
        "theta 1 (shoulder)",
        "theta 2 (shoulder)", 
        "theta 3 (elbow)", 
        "theta 4 (wrist)", 
        "theta 5 (wrist)"]

    u_bound = [ pi2,  pi2,  pi2,  pi2,  pi2]
    l_bound = [-pi2, -pi2, -pi2, -pi2, -pi2]

    def __init__(self, root : tk.Tk):

        super.__init__(master = root)
        self.root = root

        for i in range(5):

            s = tk.Scale(
                self.root,
                from_= self.l_bound[i],
                to=self.u_bound[i],
                orient=tk.HORIZONTAL
            )
            s.id = i+1
            s.parent = self

            l = tk.Label(
                self.root,
                text=self.slider_labels_txt[i]
                )
            l.id = i+1
            l.parent = self

        e = DynamicNumberEntry(root=self.root)

        def validator(value, lower=self.l_bound[i], upper=self.u_bound[i]):
            try:
                x = float(value)
            except ValueError:
                return False

            return lower <= x <= upper

        e.set_validator(validator)

        self.sliders.append(s)
        self.labels.append(l)
        self.entries.append(e)

    def get_slider_values(self):

        out = list()
        for i in range(5):
            out.append(self.sliders[i].get())
        return out



