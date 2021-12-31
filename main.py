"""
main.py

"""

import os
import sys
import tkinter as tk

from gui import GUI
from utils.bot import Bot
from utils.models import Conversation
from utils.preprocessing import prepare_model_data
from classifiers.jonasnet import JonasNetClassifier

if __name__ == '__main__':

    sys_argv = sys.argv[1:]

    build = True if 'build' in sys_argv  else False

    if 'install' in sys_argv:
        import nltk
        nltk.download('stopwords')
        print('Successfully installed.')
    elif build:
        # init model
        os_dir = os.path.abspath(os.curdir)
        data_dir = os_dir + '/data/labeled_data.csv'
        x_train, x_val, y_train, y_val = prepare_model_data(data_dir)

        model = JonasNetClassifier(os_dir, x_train, x_val, y_train, y_val, build=build)
    else:
        # init conversations
        conv_1 = Conversation(1, 'conversation 1')

        # init model
        os_dir = os.path.abspath(os.curdir)
        data_dir = os_dir + '/data/labeled_data.csv'
        x_train, x_val, y_train, y_val = prepare_model_data(data_dir)

        model = JonasNetClassifier(os_dir, x_train, x_val, y_train, y_val, build=build)

        # do some starting stuff
        active_conversation = None
        conversations = [conv_1]

        # init bot
        bot = Bot(model)

        # init Frame
        root = tk.Tk()
        frame = GUI(root, active_conversation, conversations, bot=bot)

        root.mainloop()
