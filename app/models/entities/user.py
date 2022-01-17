from ..base_entity import BaseEntity


class User(BaseEntity):
    def __init__(self, current_handler=None, step=None, handler_data={}, **kwargs):
        super().__init__(**kwargs)
        self.current_handler = current_handler
        self.step = step
        self.handler_data = handler_data

    def __str__(self):
        return self.get("name") if self.get("name") else ""

    def __repr__(self):
        return f"<User {self.data}>"

    def clear_context(self):
        self.current_handler = None
        self.message_history = []
        self.handler_data = {}
        self.step = None

    def get_message_history(self):
        return getattr(self, "message_history", [])

    def add_to_history(self, text):
        message_history = self.get_message_history()
        if self.history_top() != text:
            message_history += [text]
        self.message_history = message_history

    def has_history(self):
        return len(self.get_message_history()) > 0

    def history_top(self):
        message_history = self.get_message_history()
        return message_history[-1] if len(message_history) else None

    def history_pop(self):
        return self.message_history.pop()

    def clear_message_history(self):
        self.message_history = []
        self.last_message_id = None
