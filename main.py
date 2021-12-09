"""
main.py to test via console

"""

from gui import GUI

import tkinter as tk



if __name__ == '__main__':

    # do some starting stuff
    active_conversation = None
    conversations = []

    # init Frame
    root = tk.Tk()
    frame = GUI(root, active_conversation, conversations)

    root.mainloop()
