"""
gui.py to use via GUI

"""
import tkinter as tk
from tkinter import ttk

class GUI():

    def __init__(self, window):
        self.window = window

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
        self.window.grid_rowconfigure(0, weight=1)
        self.window.grid_columnconfigure(0, weight=1)

        # container
        self.container = tk.Frame(self.window, bg='#ad8088')
        self.container.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.grid_columnconfigure(1, weight=3)
        self.container.grid_propagate(False)

        # left_bar
        self.left_bar = tk.Frame(self.container, bg='#234235')
        self.left_bar.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.left_bar.grid_propagate(False)

        ## entry frame
        self.l_entry_frame = tk.Frame(self.left_bar)

        ## conversations list frame
        self.l_conv_list_frame = tk.Frame(self.left_bar)

        ## create new conversation frame
        self.l_new_conv_btn_frame = tk.Frame(self.left_bar)


        # main_content
        self.main_content = tk.Frame(self.container, bg='#C4C4C4')
        self.main_content.grid(column=1, row=0, padx=0, pady=0, sticky='nsew')
        self.main_content.grid_propagate(False)

        ##
    
    
