"""
gui.py to use via GUI

"""
import tkinter as tk
from tkinter import ttk

# from components.conversation_button import ConversationButton

# Colors
GREEN = '#234235'

# Fonts
FONT = 'Helvetica 14'


# TODO: factor out to component module
class ConversationButton:  # TODO: inherit -> ? now: mb not

    def __init__(self, parent, conversation, root):
        self.parent = parent
        self.conversation = conversation
        self.active = True
        self.root = root

        self.btn = tk.Button(parent,
                             text=conversation.name,
                             height=1,
                             width=25,
                             font=FONT,
                             activebackground='#b3b3b3')

        self.btn.grid(column=0, row=self.conversation.index, padx=40, pady=5, sticky='nsew')
        self.btn.bind('<Button-1>', self.on_click)

    def on_click(self, event):
        if self.root.active_conversation == self.conversation:
            self.deactivate_button()
            self.root.active_conversation = None
        else:
            if self.root.active_conversation is not None:
                self.root.conv_buttons[self.root.active_conversation.index - 1].deactivate_button()
            self.activate_button()
            self.root.active_conversation = self.conversation

    def get_button(self):
        return self.btn

    def get_conversation_name(self):
        return self.conversation.name

    def activate_button(self):
        self.btn.config(bg='#b3b3b3')
        self.btn.grid()

    def deactivate_button(self):
        self.btn.config(bg='snow')
        self.btn.grid()


class NavBar:

    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.nav_bar = tk.Frame(self.parent, bg=GREEN)
        self.nav_bar.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.nav_bar.grid_propagate(False)

        self.init_nav_view(self.nav_bar, self.root.conversations)

    def init_nav_view(self, parent, conversations):
        # parent grid config
        parent.rowconfigure(0, weight=1)
        parent.rowconfigure(1, weight=15)
        parent.rowconfigure(2, weight=5)
        parent.columnconfigure(0, weight=1)

        ## entry frame
        self.l_entry_frame = tk.Frame(parent, bg=GREEN)
        self.l_entry_frame.grid(column=0, row=0, padx=33, pady=50, sticky='nsew')
        self.l_entry_frame.rowconfigure(0, weight=0)
        self.l_entry_frame.columnconfigure(0, weight=1)
        self.l_entry_frame.grid_propagate(False)

        ### entry
        self.l_entry = tk.Entry(self.l_entry_frame,
                                textvariable=self.root.l_entry_var,
                                font=FONT)
        self.l_entry.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        self.root.l_entry_var.set('filter conversations...')

        self.l_entry.bind('<FocusIn>', self.entry_focus_in)  # handle focus

        ## conversations list frame
        self.conv_list_container = tk.Frame(parent, bg=GREEN)
        self.conv_list_container.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')
        self.conv_list_container.grid_propagate(False)

        self.create_conv_list(self.conv_list_container, conversations, self.root)

        ## create new conversation frame
        self.l_new_conv_btn_frame = tk.Frame(parent, bg=GREEN)
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
        self.root.l_entry_var.set('')

    def create_conv_list(self, parent, conversations, root):
        # scrollable cotainer
        canvas = tk.Canvas(parent, bg=GREEN, bd=0, relief='ridge', highlightthickness=0)
        scroll_bar = ttk.Scrollbar(parent, orient='vertical', command=canvas.yview)

        scrollable_frame = tk.Frame(canvas, bg=GREEN)
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        canvas.create_window((0, 0), window=scrollable_frame, anchor='nw')
        canvas.configure(yscrollcommand=scroll_bar.set)

        root.conv_buttons.clear()
        # enter conversation buttons
        for conversation in conversations:
            btn = ConversationButton(scrollable_frame, conversation, root)
            root.conv_buttons.append(btn)

        canvas.pack(side='left', fill='both', expand=True, padx=0, pady=0)
        scroll_bar.pack(side='right', fill='y', padx=0, pady=0)


class Main:

    def __init__(self, parent, root):
        self.parent = parent
        self.main_content = tk.Frame(self.parent, bg='#c4c4c4')
        self.main_content.grid(column=1, row=0, padx=0, pady=0, sticky='nsew')
        self.main_content.grid_propagate(False)

        self.init_start_view(self.main_content)
        # self.init_main_conversation_view(self.main_content)

    def init_start_view(self, parent):
        ## parent grid config
        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

        ## starting view
        self.start_window = tk.Frame(parent)
        self.start_window.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')

    def init_conversation_view(self, parent):
            # parent grid config
            parent.rowconfigure(0, weight=15)
            parent.rowconfigure(1, weight=1)
            parent.columnconfigure(0, weight=1)

            # conversation window
            conv_window = tk.Frame(parent)
            conv_window.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')

            # conversation text field frame
            conv_txt_field_frame = tk.Frame(parent)
            conv_txt_field_frame.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')
            conv_txt_field_frame.rowconfigure(0, weight=0)
            conv_txt_field_frame.columnconfigure(0, weight=0)

            # conversation text field
            conv_txt_field = tk.Text(conv_txt_field_frame, width=90, height=7, font=FONT)
            conv_txt_field.grid(column=0, row=0, padx=10, pady=5, sticky='nsew')

            conv_txt_field.bind('<Return>', txt_field_enter)


class GUI:



    def button_new_conv(self):
        self.conversations.add({'New conversation': []})
        self.active_conversation = (len(self.conversations) - 1)

    def txt_field_enter(self, event):
        if self.active_conversation is not None:
            self.conversations[self.active_conversation].add('test')
        return 'break'

    def __init__(self, window, active_conversation, conversations):
        self.window = window
        self.active_conversation = active_conversation
        self.conversations = conversations

        self.l_entry_var = tk.StringVar()
        self.conv_buttons = []

        # init constants
        w_width = 1500
        w_height = 1100

        # set title
        self.window.title('Hate Speech Detection Bot')

        # get screen geometry
        s_width = self.window.winfo_screenwidth()  # width of screen
        s_height = self.window.winfo_screenheight()  # height of screen

        w_x = (s_width / 2) - (w_width / 2)
        w_y = (s_height / 2) - (w_height / 2)

        # set window geometry and pos @start
        self.window.geometry('%dx%d+%d+%d' % (w_width, w_height, w_x, w_y))
        self.window.resizable(False, False)
        self.window.rowconfigure(0, weight=1)
        self.window.columnconfigure(0, weight=1)

        # container
        self.container = tk.Frame(self.window, bg=GREEN)
        self.container.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.container.rowconfigure(0, weight=1)
        self.container.columnconfigure(0, weight=1)
        self.container.columnconfigure(1, weight=3)
        self.container.grid_propagate(False)

        # nav_bar
        nav_bar = NavBar(self.container, self)

        # main
        main = Main(self.container, self)