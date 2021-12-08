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

        # container
        self.container = tk.Frame(self.window, width=w_width, height=w_height)
        self.container.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        self.container.pack_propagate(False)

        # nav-menu
        self.nav_menu = tk.Frame(self.container, bg='#234235', width=w_width/4, height=w_height)
        self.nav_menu.grid(row=0, column=0, sticky='nsew')
        self.nav_menu.grid_rowconfigure((0, 2), weight=1)
        self.nav_menu.grid_rowconfigure(1, weight=5)
        self.nav_menu.grid_columnconfigure(0, weight=1)
        self.nav_menu.pack_propagate(False)

        ## button
        self.filter_input = tk.Entry(self.nav_menu)
        self.filter_input.insert(1, 'filter conversations...')
        self.filter_input.grid(column=0, row=1, padx=10, pady=5, sticky='nsew')



        ## frame

        # main
        self.main_content = tk.Frame(self.container, bg='#C4C4C4', width=w_width/4*3, height=w_height)
        self.nav_menu.grid(row=0, column=0, sticky='nsew')

        self.conversation_window = tk.Frame(self.main_content, bg='#ffffff')

        self.message_window = tk.Frame(self.main_content, bg='#ffffff')
    
    
