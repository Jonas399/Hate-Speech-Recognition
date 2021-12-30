"""
gui.py to use via GUI

"""
import tkinter as tk
from tkinter import ttk

from gui.constants import GREEN
from gui.components import NavBar
from gui.components import MainWindow
from utils.bot import Bot
from utils.models import Conversation


class GUI:

    def __init__(self, window, active_conversation: Conversation, 
        conversations, bot: Bot = None):
        self.window = window
        self.active_conversation = active_conversation
        self.conversations = conversations
        self.bot = bot

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
        self.nav_bar = NavBar(self.container, self)

        # main
        self.main = MainWindow(self.container, self.active_conversation, bot=self.bot)

    def button_new_conv(self):
        self.conversations.add({'New conversation': []})
        self.active_conversation = (len(self.conversations) - 1)

    def txt_field_enter(self, event):
        if self.active_conversation is not None:
            self.conversations[self.active_conversation].add('test')
        return 'break'

    def change_active_conversation(self, conversation):
        self.active_conversation = conversation

    def open_active_conversation(self):
        # print('Open conversation.')
        self.main.open_conversation(self.active_conversation)

    def close_active_conversation(self):
        # print('Closes conversation.')
        self.main.close_conversation()
