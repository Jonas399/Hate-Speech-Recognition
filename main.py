"""
main.py to test via console

"""

from gui import GUI
from utils.models import Conversation

import tkinter as tk


if __name__ == '__main__':

    conv_1 = Conversation(1, 'conv_1')
    conv_1.add_message('Hello my friend.', 'bot')

    conv_2 = Conversation(2, 'conv_2')
    conv_2.add_message('Hello traveler.', 'bot')

    # do some starting stuff
    active_conversation = None
    conversations = [conv_1, conv_2]

    print(conversations)

    # init Frame
    root = tk.Tk()
    frame = GUI(root, active_conversation, conversations)

    root.mainloop()
