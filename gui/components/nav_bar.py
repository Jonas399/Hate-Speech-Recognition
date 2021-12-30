import tkinter as tk

from tkinter import ttk
from gui.constants import GREEN
from gui.constants import FONT
from gui.components import ConversationButton

class NavBar:

    def __init__(self, tk_parent, obj_parent):
        self.tk_parent = tk_parent
        self.obj_parent = obj_parent
        self.nav_bar = tk.Frame(self.tk_parent, bg=GREEN)
        self.nav_bar.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.nav_bar.grid_propagate(False)

        self.l_entry_var = tk.StringVar()

        self.init_nav_view()

    def init_nav_view(self):
        # parent grid config
        self.nav_bar.rowconfigure(0, weight=1)
        self.nav_bar.rowconfigure(1, weight=15)
        self.nav_bar.rowconfigure(2, weight=5)
        self.nav_bar.columnconfigure(0, weight=1)

        ## entry frame
        self.l_entry_frame = tk.Frame(self.nav_bar, bg=GREEN)
        self.l_entry_frame.grid(column=0, row=0, padx=33, pady=50, sticky='nsew')
        self.l_entry_frame.rowconfigure(0, weight=0)
        self.l_entry_frame.columnconfigure(0, weight=1)
        self.l_entry_frame.grid_propagate(False)

        ### entry
        self.l_entry = tk.Entry(self.l_entry_frame,
                                textvariable=self.l_entry_var,
                                font=FONT)
        self.l_entry.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        self.l_entry_var.set('filter conversations...')

        self.l_entry.bind('<FocusIn>', self.entry_focus_in)  # handle focus

        ## conversations list frame
        self.conv_list_container = tk.Frame(self.nav_bar, bg=GREEN)
        self.conv_list_container.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')
        self.conv_list_container.grid_propagate(False)

        self.create_conv_list(self.obj_parent.conversations)

        ## create new conversation frame
        self.l_new_conv_btn_frame = tk.Frame(self.nav_bar, bg=GREEN)
        self.l_new_conv_btn_frame.grid(column=0, row=2, padx=0, pady=0, sticky='nsew')
        self.l_new_conv_btn_frame.rowconfigure(0, weight=0)
        self.l_new_conv_btn_frame.columnconfigure(0, weight=1)
        self.l_new_conv_btn_frame.grid_propagate(False)

        ### button
        self.l_new_conv_btn = tk.Button(self.l_new_conv_btn_frame,
                                text='Create new conversation',
                                height=1,
                                width=20,
                                font=FONT)
        self.l_new_conv_btn.grid(column=0, row=0, padx=40, pady=10, sticky='nsew')


    def entry_focus_in(self, event):
        self.l_entry_var.set('')


    def create_conv_list(self, conversations):
        # scrollable cotainer
        canvas = tk.Canvas(self.conv_list_container, bg=GREEN, bd=0, relief='ridge', highlightthickness=0)
        scroll_bar = ttk.Scrollbar(self.conv_list_container, orient='vertical', command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=GREEN)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scroll_bar.set)

        self.obj_parent.conv_buttons.clear()
        # enter conversation buttons
        for conversation in conversations:
            btn = ConversationButton(scrollable_frame, self.obj_parent, conversation)
            self.obj_parent.conv_buttons.append(btn)

        canvas.pack(side='left', fill='both', expand=True, padx=0, pady=0)
        scroll_bar.pack(side='right', fill='y', padx=0, pady=0)

