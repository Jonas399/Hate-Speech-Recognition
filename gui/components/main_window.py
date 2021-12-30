import tkinter as tk
from tkinter.constants import W

from gui.constants import GREEN, LIGHT_GREY
from gui.constants import DARK_GREY
from gui.constants import WHITE
from gui.constants import FONT
from gui.constants import FONT_BIG
from gui.utils import destroy_frame_widgets

from gui.components.chat_window import ChatWindow
from utils.bot import Bot
from utils.models import Conversation


class MainWindow:

    def __init__(self, parent: tk.Widget, active_conversation: Conversation, bot: Bot = None):
        self.parent = parent
        # self.root = root
        self.active_conversation = active_conversation
        self.bot = bot

        self.main_content = tk.Frame(self.parent, bg='#c4c4c4')
        self.main_content.rowconfigure(0, weight=1)
        self.main_content.columnconfigure(0, weight=1)
        self.main_content.grid(column=1, row=0, padx=0, pady=0, sticky='nsew')
        self.main_content.grid_propagate(False)

        self.start_view = None
        self.conversation_view = None
        self.conversation_canvas = None
        self.init_start_view()
        # self.init_main_conversation_view(self.main_content)


    def init_start_view(self):
        destroy_frame_widgets(self.main_content)

        ## container 
        container = tk.Frame(self.main_content)
        container.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        container.grid_propagate(False)
        container.rowconfigure(0, weight=1)
        container.columnconfigure(0, weight=1)

        ## starting view
        start_view = tk.Frame(container, bg=LIGHT_GREY)
        start_view.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        start_view.rowconfigure((0, 1, 2), weight=1)
        start_view.columnconfigure((0, 1, 2), weight=1)

        window_text = tk.Label(start_view, font=FONT_BIG)
        window_text['text'] = 'Create or open a conversation.'
        window_text.grid(column=1, row=0, padx=0, pady=0, sticky='nsew')


    def init_conversation_view(self):
        destroy_frame_widgets(self.main_content)
        chat= ChatWindow(self.main_content, self.active_conversation, bot=self.bot)

    
    def init_edit_conversation_view(self):
        pass


    def open_conversation(self, conversation: Conversation):
        self.active_conversation = conversation
        self.init_conversation_view()


    def close_conversation(self):
        self.init_start_view()


    def add_message(self):
        pass