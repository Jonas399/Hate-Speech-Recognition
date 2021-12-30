from ..constants import FONT

import tkinter as tk


# Fonts
FONT = 'Helvetica 14'


class ConversationButton:  # TODO: inherit -> ? now: mb not

    def __init__(self, tk_parent, obj_parent, conversation):
        self.tk_parent = tk_parent
        self.obj_parent = obj_parent
        self.conversation = conversation
        self.active = True

        self.btn = tk.Button(tk_parent,
                             text=conversation.get_name(),
                             height=1,
                             width=25,
                             font=FONT,
                             activebackground='#b3b3b3')

        self.btn.grid(column=0, row=self.conversation.get_index(), padx=40, pady=5, sticky='nsew')
        self.btn.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        if self.obj_parent.active_conversation == self.conversation:
            self.deactivate_button()
            self.obj_parent.close_active_conversation()
            self.obj_parent.active_conversation = None
        else:
            if self.obj_parent.active_conversation is not None:
                self.obj_parent.close_active_conversation()
                self.obj_parent.conv_buttons[self.obj_parent.active_conversation.get_index() - 1].deactivate_button()
            self.activate_button()
            self.obj_parent.active_conversation = self.conversation
            self.obj_parent.open_active_conversation()

    def get_button(self):
        return self.btn

    def get_conversation_name(self):
        return self.conversation.get_name()

    def activate_button(self):
        self.btn.config(bg='#b3b3b3')
        self.btn.grid()

    def deactivate_button(self):
        self.btn.config(bg='snow')
        self.btn.grid()

