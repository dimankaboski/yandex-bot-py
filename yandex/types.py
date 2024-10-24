import json


class JsonSerializable(object):
    def to_json(self):
        raise NotImplementedError


class Dictionaryable(object):
    def to_dict(self):
        raise NotImplementedError


class JsonDeserializable(object):
    @classmethod
    def de_json(cls, json_string):
        raise NotImplementedError


class User(JsonDeserializable, Dictionaryable, JsonSerializable): # noqa
    def __init__(self, id: str, display_name: str, login: str, robot: bool):
        self.id = id
        self.display_name = display_name
        self.login = login
        self.robot = robot

    def to_dict(self):
        return {
            "id": self.id,
            "display_name": self.display_name,
            "login": self.login,
            "is_robot": self.robot,
        }


class Message(JsonDeserializable, Dictionaryable, JsonSerializable): # noqa
    def __init__(self, message_id: str, timestamp: str, text: str, user: User, **kwargs):
        self.message_id = message_id
        self.timestamp = timestamp
        self.text = text
        self.user = user

    def __repr__(self):
        return f"Message from {self.user.login} at {self.timestamp}"

    def to_dict(self):
        return {
            "id": self.message_id,
            "timestamp": self.timestamp,
            "user": self.user.to_dict(),
            "text": self.text,
        }


class Chat(JsonDeserializable, Dictionaryable, JsonSerializable): # noqa
    def __init__(self, name: str, description: str, avatar_url: str = "", chat_id: str = ""):
        self.chat_id = chat_id
        self.name = name
        self.description = description
        self.avatar_url = avatar_url
        self.members = []
        self.admins = []
        self.subscribers = []

    def to_dict(self):
        return {
            "chat_id": self.chat_id,
            "name": self.name,
            "description": self.description,
            "avatar_url": self.avatar_url,
            "members": self.members,
            "admins": self.admins,
            "subscribers": self.subscribers,
        }

    def to_json(self):
        return json.loads(self.to_dict())

    def set_members(self, members: [User]):
        self.members = members
        return self.members

    def set_admins(self, admins: [User]):
        self.admins = admins
        return self.admins

    def set_subscribers(self, subscribers: [User]):
        self.subscribers = subscribers
        return self.subscribers


class Button(JsonDeserializable, Dictionaryable, JsonSerializable):
    def __init__(self, text: str, callback_data: dict = None, phrase: str = ""):
        self.text = text
        self.callback_data = callback_data
        if callback_data is None:
            self.callback_data = {}
        if phrase:
            self.callback_data.update(phrase=phrase)

    def to_dict(self):
        return {
            "text": self.text,
            "callback_data": self.callback_data,
        }

    def to_json(self):
        return json.dumps(self.to_dict())
