from telegram.ext import MessageFilter


class FilterInCommand(MessageFilter):
    def __init__(self, commands):
        self.commands = commands

    def filter(self, message):
        if not message.text:
            return True
        command = message.text.split("@")
        return command[0] in self.commands
