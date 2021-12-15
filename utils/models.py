import time


class Conversation:

    def __init__(self, index, name, messages=[]):
        self.index = index
        self.name = name
        self.messages = messages

    def add_message(self, message_content, emitter):
        self.messages.append(Message(message_content, emitter))

    def delete_message(self, message):
        pass

    def change_index(self, index):
        pass

    def change_name(self, name):
        pass


class Message:

    def __init__(self, content, emitter, report=None):
        self.content = content
        self.timestamp = time.time()
        self.emitter = emitter
        self.report = report
