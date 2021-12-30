import time


class Message:
    
    def __init__(self, content, emitter, report=None):
        self.content = content
        self.timestamp = time.time()
        self.emitter = emitter
        self.report = report

    def __str__(self):
        return f'{self.timestamp} - content: {self.content}, emitter: {self.emitter}, report: {True if self.report is not None else False}'


class Conversation:

    def __init__(self, index, name, messages=[]):
        self._index = index
        self._name = name
        self._messages = messages

    def add_message(self, message: Message):
        self._messages.append(message)

    def add_multiple_messages(self, _messages):
        for _message in _messages:
            self.add_message(_message)

    def delete_message(self, message):
        pass

    def change_index(self, index):
        pass

    def change_name(self, name):
        pass

    def get_messages(self):
        return self._messages

    def get_name(self):
        return self._name

    def get_index(self):
        return self._index



