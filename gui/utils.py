"""
Tkinter Utils
"""
import tkinter as tk


def destroy_frame_widgets(frame: tk.Frame):
    if frame is None: return

    widgets = frame.winfo_children()
    for widget in widgets:
        widget.destroy()
    