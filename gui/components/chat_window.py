import time
import tkinter as tk
from tkinter.constants import END
from textwrap import wrap

from gui.constants import BLACK, DARK_GREY, FONT, FONT_SMALL, GREEN, WHITE
from utils.models import Conversation, Message
from utils.bot import Bot

class ChatWindow:

    def __init__(self, parent: tk.Frame, conversation: Conversation, bot: Bot):
        self.parent = parent
        self.conversation = conversation
        self.message_count = 0

        self.bot = bot

        self.init_chat()


    def init_chat(self):

        ## container
        container = tk.Frame(self.parent)
        container.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        container.grid_propagate(False)
        container.rowconfigure(0, weight=15)
        container.rowconfigure(1, weight=1)
        container.columnconfigure(0, weight=1)

        # conversation window
        conversation_window = tk.Frame(container)
        conversation_window.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        conversation_window.rowconfigure(0, weight=1)
        conversation_window.columnconfigure(0, weight=1)
        
        ### messaging part
        # conversation text field frame
        conv_txt_field_frame = tk.Frame(container)
        conv_txt_field_frame.grid(column=0, row=1, padx=100, pady=(2, 30), sticky='nsew')
        conv_txt_field_frame.rowconfigure(0, weight=0)
        conv_txt_field_frame.columnconfigure(0, weight=1)
        conv_txt_field_frame.columnconfigure(1, weight=0)

        # conversation text field
        self.conv_txt_field = tk.Text(conv_txt_field_frame, height=5, width=70, 
            font=FONT, padx=10, pady=5)
        self.conv_txt_field.grid(column=0, row=0, padx=0, pady=0, sticky='nsew')
        self.conv_txt_field.bind('<Return>', self.user_send_message)

        # send button
        send_btn = tk.Button(conv_txt_field_frame, width=10, height=5, font=FONT, 
            bg=DARK_GREY, fg=WHITE, command=lambda: self.user_send_message(None))
        send_btn['text'] = 'Send'
        send_btn.grid(column=1, row=0, padx=5, pady=0, sticky='nsew')
        

        ### chat window part
        # container
        chat_window = tk.Frame(conversation_window)
        chat_window.rowconfigure(0, weight=1)
        chat_window.columnconfigure(0, weight=1)
        chat_window.grid(column=0, row=0, padx=0, pady=0)

        # canvas
        canvas_height = 915
        canvas_width = 900

        self.scrollregion_height = canvas_height * 100

        self.canvas=tk.Canvas(chat_window, bg=WHITE, width=canvas_width, height=canvas_height, 
            scrollregion=(0, 0, canvas_width, self.scrollregion_height))
        
        # scroll bar
        vbar = tk.Scrollbar(chat_window,orient='vertical')
        vbar.pack(side='right', fill='y')
        vbar.config(command=self.canvas.yview)

        self.canvas.config(width=canvas_width, height=canvas_height)
        self.canvas.config(yscrollcommand=vbar.set)
        self.canvas.pack(side='left', expand=True, fill='both')


        def on_mousewheel(event):
            self.canvas.yview_scroll(-1*int(event.delta/120), "units")
        self.canvas.bind_all('<MouseWheel>', on_mousewheel)

        # # message container
        self.message_container = tk.Frame(self.canvas, padx=10, pady=5, bg=WHITE)
        self.message_container.columnconfigure((0, 1), weight=1)
        self.canvas.create_window((0, 0), window=self.message_container, anchor='nw', 
            height=self.scrollregion_height, width=canvas_width - 20)

        # init messages
        for message in self.conversation.get_messages():
            self.add_message(message)

        if not self.conversation.get_messages():
            bot_msg = self.bot.greet()
            self.conversation.add_multiple_messages(bot_msg) 
            self.add_multiple_messages(bot_msg)
        
        self.conv_txt_field.focus()


    def add_message(self, message: Message):
        self.message_count += 1

        message_label = None

        if message.emitter == 'bot':
            container = tk.Frame(self.message_container)
            container.grid(column=0, row=self.message_count, sticky='nw', pady=1)

            message_label = tk.Label(container, font=FONT_SMALL, bg=DARK_GREY, fg=WHITE,
                pady=10, padx=15)
            message_label.grid()

            if 'contains hate speech' in message.content:
                message_label['bg'] = 'red'
            elif 'contains offensive language' in message.content:
                message_label['bg'] = 'yellow'
                message_label['fg'] = BLACK
            elif 'contains no hate speech and no offensive language' in message.content:
                message_label['bg'] = 'green'

            wrapped_strings = None

            if len(message.content) > 45:
                wrapped_strings = wrap(message.content, 45)
                for index, string in enumerate(wrapped_strings):
                    if index == 0:
                        message_label['text'] += string.strip()
                    else:
                        message_label['text'] += '\n' + string.strip()
            else:
                wrapped_strings = message.content
                message_label['text'] += message.content

            ## update scrollregion
            

        elif message.emitter == 'user':
            container = tk.Frame(self.message_container)
            container.grid(column=1, row=self.message_count, sticky='ne', pady=1)

            message_label = tk.Label(container, font=FONT_SMALL, bg=GREEN, fg=WHITE,
                pady=10, padx=15)
            message_label.grid()

            if 'contains hate speech' in message.content:
                message_label['bg'] = 'red'
            elif 'contains offensive language' in message.content:
                message_label['bg'] = 'yellow'
            elif 'contains no hate speech and no offensive language' in message.content:
                message_label['bg'] = 'green'

            wrapped_strings = None

            if len(message.content) > 45:
                wrapped_strings = wrap(message.content, 45)
                for index, string in enumerate(wrapped_strings):
                    if index == 0:
                        message_label['text'] += string.strip()
                    else:
                        message_label['text'] += '\n' + string.strip()
            else:
                wrapped_strings = message.content
                message_label['text'] += message.content

            ## update scrollregion

        else:
            raise Exception('wrong message type in Chat_window.add_message')

    
    def add_multiple_messages(self, _messages):
        print(_messages)
        if not _messages: return
        if isinstance(_messages, list) and _messages[0].emitter != 'bot': return

        for _message in _messages:
            self.conversation.add_message(_message)
            self.add_message(_message)


    def user_send_message(self, event):
        text_content = self.conv_txt_field.get('1.0', END).strip()
        if not text_content: return 'break'

        self.conv_txt_field.delete('1.0', END)

        user_msg = Message(text_content, 'user')
        self.conversation.add_message(user_msg)
        self.add_message(user_msg)

        # answer
        bot_msg = self.bot.answer(text_content)
        self.conversation.add_multiple_messages(bot_msg)
        self.add_multiple_messages(bot_msg)

        return 'break' # prevent default
