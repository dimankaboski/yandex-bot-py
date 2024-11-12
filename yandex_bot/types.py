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


class User(JsonDeserializable, Dictionaryable, JsonSerializable):  # noqa
    def __init__(self, login: str = "", id: str = "", display_name: str = "", robot: bool = False):
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

      
class File(JsonDeserializable, Dictionaryable, JsonSerializable):
    def __init__(self, id: str, name: str, size: int):
        self.id = id
        self.name = name
        self.size = size

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "size": self.size,
        }

    def __repr__(self):
        return f"<File object> {self.id}, {self.name}, size: {self.size}"


class Image(JsonDeserializable, Dictionaryable, JsonSerializable):
    def __init__(self, file_id: str, width: int, height: int, name: str = "", size: int = 0):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.name = name
        self.size = size

    def to_dict(self):
        return {
            "file_id": self.file_id,
            "width": self.width,
            "height": self.height,
            "name": self.name,
            "size": self.size,
        }

    def __repr__(self):
        return f"<Image object> {self.file_id}, {self.name}, width {self.width}x{self.height}"


class Message(JsonDeserializable, Dictionaryable, JsonSerializable): # noqa
    def __init__(self, message_id: str, timestamp: str, text: str, user: User, pictures: [Image] = None, attachment: File = None, **kwargs):
        self.message_id = message_id
        self.callback_data = None
        self.timestamp = timestamp
        self.text = text
        self.user = user
        self.file = kwargs.get("file") if kwargs.get("file") else None
        if pictures is None:
            self.images = []
        else:
            self.images = pictures
        self.file = attachment
        if kwargs.get("callback_data"):
            self.callback_data = kwargs.get("callback_data")

    def __repr__(self):
        return f"Message from {self.user.login} at {self.timestamp}, File: {self.file}, Images: {self.images}"

    def to_dict(self):
        return {
            "id": self.message_id,
            "timestamp": self.timestamp,
            "user": self.user.to_dict(),
            "text": self.text,
        }


class Chat(JsonDeserializable, Dictionaryable, JsonSerializable):  # noqa
    def __init__(
        self, name: str, description: str, avatar_url: str = "", chat_id: str = ""
    ):
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
            # "avatar_url": self.avatar_url,
            "members": [member.to_dict() for member in self.members],
            "admins": [admin.to_dict() for admin in self.admins],
            "subscribers": [subscriber.to_dict() for subscriber in self.subscribers]
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


class Poll(JsonDeserializable, Dictionaryable, JsonSerializable):

    def __init__(
        self,
        title: str,
        answers: list[str],
        max_choices: int = 1,
        is_anonymous: bool = False,
    ) -> None:
        self.title = title
        self.answers = answers
        self.max_choices = max_choices
        self.is_anonymous = is_anonymous

    def to_dict(self):
        return {
            "title": self.title,
            "answers": self.answers,
            "max_choices": self.max_choices,
            "is_anonymous": self.is_anonymous,
        }

    

