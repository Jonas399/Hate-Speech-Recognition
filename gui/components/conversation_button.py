from ..constants import FONT

import tkinter as tk


# Fonts
FONT = 'Helvetica 14'


class ConversationButton:  # TODO: inherit -> ? now: mb not

    def on_click(self, event):
        print(self.conversation.name)

    def __init__(self, parent, conversation, active_conversation):
        self.parent = parent
        self.conversation = conversation
        self.active_conversation = active_conversation

        btn = tk.Button(parent,
                        text=conversation.name,
                        height=1,
                        width=25,
                        font=FONT)

        btn.grid(column=0, row=conversation.index, padx=40, pady=5, sticky='nsew')
        btn.bind('<Button-1>', self.on_click)

