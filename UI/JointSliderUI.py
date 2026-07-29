import tkinter as tk
from UI.UI_blocks.dynamic_entries import DynamicNumberEntry
from UI.UI_tools.field_validators import *

class JointSliderUI(tk.Frame):

    root : tk.Tk = None
    n_sliders = 5
    pi = 3.1415
    pi2 = pi/2


    slider_labels_txt = [
        "theta 1 (shoulder)",
        "theta 2 (shoulder)", 
        "theta 3 (elbow)", 
        "theta 4 (wrist)", 
        "theta 5 (wrist)"]

    u_bound = [ pi2,  pi2,  pi2,  pi2,  pi2]
    l_bound = [-pi2, -pi2, -pi2, -pi2, -pi2]

    def __init__(self, root : tk.Tk):

        self.sliders = [] # Tk.Scale objects
        self.labels = []  # Tk.Label objects
        self.entries = [] # UI.DynamicEntry objects

        super().__init__(master = root)
        self.root = root

        for i in range(5):

            s = tk.Scale(
                self.root,
                from_= self.l_bound[i],
                to=self.u_bound[i],
                orient=tk.HORIZONTAL,
                command=lambda value, index = i: self.slider_callback(index,value),
                resolution=0.001
            )
            s.id = i
            s.parent = self

            l = tk.Label(
                self.root,
                text=self.slider_labels_txt[i]
                )
            l.id = i
            l.parent = self

            e = DynamicNumberEntry(root=self.root)
            e.id = i
            e.config(width=10)

            def validator_(value, lower=self.l_bound[i], upper=self.u_bound[i], id = i):
                try:
                    x = float(value)
                except ValueError:
                    return False
                queerie = (lower <= x <= upper)
                if queerie:
                    self.sliders[id].set(x) # this might not work though given how python is run it should

                return queerie

            e.set_validator(validator = validator_)

            self.sliders.append(s)
            self.labels.append(l)
            self.entries.append(e)

            row = 2 * i

            l.grid(
                row=row,
                column=0,
                sticky="w",
                padx=10,
                pady=(10, 0)
            )

            s.grid(
                row=row + 1,
                column=0,
                sticky="w",
                padx=10,
                pady=(0, 10)
            )

            e.grid(
                row=row + 1,
                column=1,
                padx=(5, 10),
                pady=(0, 10)
            )


        self.columnconfigure(0, weight=1)

    def get_slider_values(self):

        out = list()
        for i in range(5):
            out.append(self.sliders[i].get())
        return out

    def slider_callback(self, index, value):
        self.entries[index].set_text_wrapper(value)



#+----------------------+---------+
#| theta 1 (shoulder)   |         |
#| [-----slider------]  | [entry] |
#+----------------------+---------+
#
#+----------------------+---------+
#| theta 2 (shoulder)   |         |
#| [-----slider------]  | [entry] |
#+----------------------+---------+
