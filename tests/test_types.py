import pytest

from yandex_bot import Button, Poll, Chat, User, Message, Image, File


@pytest.fixture(scope='module')
def user():
    return User(login="login@login.ru", id="fwaf-fwaf-gawg-egsg", 
    display_name="Name", robot=False)


@pytest.fixture(scope='module')
def message(user):
    return Message(message_id="2131", timestamp="414141414", text="text message",
                    user=user, callback_data={'foo': 'bar'})


@pytest.fixture(scope='module')
def poll():
    return Poll(title="Test poll", answers=["an 1", "an 2"],
                max_choices=1, is_anonymous=False)


@pytest.fixture(scope='module')
def button():
    return Button(text="Button 1", callback_data={'btn': "11"}, phrase="/start")


@pytest.fixture(scope='module')
def chat():
    return Chat(name="Name chat", description="Test", avatar_url="/url/img.jpg")


@pytest.fixture(scope='module')
def image():
    return Image(file_id="111", width=200, height=300, name="Name image", size=411234)


@pytest.fixture(scope='module')
def file():
    return File(id="1112", name="Name file", size=112341)


def test_dictionaryable(user, message, poll, button, chat, image, file):
    assert user.to_dict() == {
            "id": "fwaf-fwaf-gawg-egsg",
            "display_name": "Name",
            "login": "login@login.ru",
            "is_robot": False,
    }
    assert message.to_dict() == {
            "id": "2131",
            "timestamp": "414141414",
            "user": user.to_dict(),
            "text": "text message",
    }
    assert poll.to_dict() == {
            "title": "Test poll",
            "answers": ["an 1", "an 2"],
            "max_choices": 1,
            "is_anonymous": False,
    }
    assert button.to_dict() == {
            "text": "Button 1",
            "callback_data": {'btn': "11", "phrase": "/start"},
    }
    assert chat.to_dict() == {
            "chat_id": "",
            "name": "Name chat",
            "description": "Test",
            # "avatar_url": "/url/img.jpg",
            "members": [],
            "admins": [],
            "subscribers": [],
    }
    assert image.to_dict() == {
            "file_id": "111",
            "width": 200,
            "height": 300,
            "name": "Name image",
            "size": 411234,
    }
    assert file.to_dict() == {
            "id": "1112",
            "name": "Name file",
            "size": 112341,
    }


def test_chat_add_users(chat):
    user1 = User(login="test.test")
    user2 = User(login="test.test2")
    user3 = User(login="test.test3")
    chat.set_admins([user1])
    chat.set_members([user2])
    chat.set_subscribers([user3])
    assert chat.admins == [user1]
    assert chat.members == [user2]
    assert chat.subscribers == [user3]