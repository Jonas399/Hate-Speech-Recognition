"""
gui.py to use via GUI

"""
import tkinter as tk
from tkinter import ttk

GREEN = '#234235'
FONT = 'Helvetica 14'

class GUI():

    def entry_focus_in(self, event):
        self.l_entry_var.set('')

    def button_new_conv(self):
        self.conversations.add({'New conversation':[]})
        self.active_conversation = (len(self.conversations) - 1)

    def txt_field_enter(self, event):
        self.conversations[self.active_conversation].add('test')
        return 'break'

    def __init__(self, window, active_conversation, conversations):
        self.window = window
        self.active_conversation = active_conversation
        self.conversations = conversations

        self.l_entry_var = tk.StringVar()

        # init constants
        w_width = 1500
        w_height = 1100

        # set title
        self.window.title('Hate Speech Detection Bot')

        # get screen geometry
        s_width = self.window.winfo_screenwidth() # width of screen
        s_height = self.window.winfo_screenheight() # height of screen

        w_x = (s_width/2) - (w_width/2)
        w_y = (s_height/2) - (w_height/2)

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

        # left_bar
        self.left_bar = tk.Frame(self.container, bg=GREEN)
        self.left_bar.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.left_bar.rowconfigure(0, weight=1)
        self.left_bar.rowconfigure(1, weight=15)
        self.left_bar.rowconfigure(2, weight=5)
        self.left_bar.columnconfigure(0, weight=1)
        self.left_bar.grid_propagate(False)

        ## entry frame
        self.l_entry_frame = tk.Frame(self.left_bar, bg=GREEN)
        self.l_entry_frame.grid(column=0, row=0, padx=33, pady=50, sticky='nsew')
        self.l_entry_frame.rowconfigure(0, weight=0)
        self.l_entry_frame.columnconfigure(0, weight=1)
        self.left_bar.grid_propagate(False)

        ### entry
        self.l_entry = tk.Entry(self.l_entry_frame,
                                textvariable=self.l_entry_var,
                                font=FONT)
        self.l_entry.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')
        self.l_entry_var.set('filter conversations...')

        self.l_entry.bind('<FocusIn>', self.entry_focus_in) # handle focus

        ## conversations list frame
        self.l_conv_list_frame = tk.Frame(self.left_bar, bg=GREEN)
        self.l_conv_list_frame.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')
        self.l_conv_list_frame.grid_propagate(False)


        ## create new conversation frame
        self.l_new_conv_btn_frame = tk.Frame(self.left_bar, bg=GREEN)
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

        #####

        # main_content
        self.main_content = tk.Frame(self.container, bg='#c4c4c4')
        self.main_content.grid(column=1, row=0, padx=0, pady=0, sticky='nsew')
        self.main_content.rowconfigure(0, weight=15)
        self.main_content.rowconfigure(1, weight=1)
        self.main_content.columnconfigure(0, weight=1)
        self.main_content.grid_propagate(False)

        ## conversation window
        self.conv_window = tk.Frame(self.main_content)
        self.conv_window.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')

        ## conversation text field frame
        self.conv_txt_field_frame = tk.Frame(self.main_content)
        self.conv_txt_field_frame.grid(column=0, row=1, padx=0, pady=0, sticky='nsew')
        self.conv_txt_field_frame.rowconfigure(0, weight=0)
        self.conv_txt_field_frame.columnconfigure(0, weight=0)

        ### conversation text field
        self.conv_txt_field = tk.Text(self.conv_txt_field_frame, width=90, height=7, font=FONT)
        self.conv_txt_field.grid(column=0, row=0, padx=10, pady=5, sticky='nsew')

        self.conv_txt_field.bind('<Return>', self.txt_field_enter)

    
    
