

class BaseHandler:
    def __init__(self):
        ...


class MemoryStepHandler(BaseHandler):
    def __init__(self):
        self.handlers = {}

    def register_handler(self, user_login, callback):
        self.handlers.update({user_login: callback})

    def delete_handler(self, user_login):
        del self.handlers[user_login]

    def get_handlers(self):
        return self.handlers
