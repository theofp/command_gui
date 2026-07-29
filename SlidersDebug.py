#!/usr/bin/env python3

from UI.JointSliderUI import JointSliderUI
import tkinter as tk
from std_msgs.msg import Float32MultiArray


def main(*args, **kwargs):
    window = tk.Tk()
    window.title("Barebones UI")
    window.geometry("500x700")
    UI = JointSliderUI(window)
    window.mainloop()


if __name__ == "__main__":
    main()