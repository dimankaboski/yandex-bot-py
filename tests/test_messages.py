import pytest

from yandex_bot import Button, Poll, Chat, User, Message, Client


@pytest.fixture
def json_message():
    return {'message_id': 1111111111, 'timestamp': 52352323523, 'chat': {'type': 'private'}, 'from': {'id': '320fesf-gesg342-gsegse523-hrtyu67580', 'display_name': 'Display name', 'login': 'login@login.ru', 'robot': False}, 'update_id': 1242141241, 'callback_data': {'phrase': '/hello'}, 'text': 'Hello'}


@pytest.fixture
def user():
    return User(login="login@login.ru")


@pytest.fixture
def message(user):
    return Message(message_id="1242141241", timestamp="timestamp", text="text message",
                   user=user)


@pytest.fixture
def client():
    return Client(api_key="TEST", ssl_verify=False, timeout=10)


def test_client(client):
    assert client.api_key == "TEST"
    assert client.ssl_verify is False
    assert client.timeout == 10


def test_build_handler_dict(client):
    @client.on_message(phrase="/start")
    def start(fix_message):
        return fix_message.text
    assert client._build_handler_dict(start, "/start") == {"function": start, "phrase": "/start"}


def test_message_handler(client):
    @client.on_message(phrase="/start")
    def start(message):
        return message
    for handler in client.handlers:
        assert handler['phrase'] == "/start"
        assert handler['function'] == start


def test_next_step_handler(client, user):
    def next_step():
        ...
    client.register_next_step_handler(user.login, next_step)
    handlers = client.next_step_handler.get_handlers()
    assert handlers.get(user.login) == next_step


def test_run_handler(client, message):
    @client.on_message(phrase="/start")
    def start(fix_message):
        return fix_message.text
    assert client._run_handler(start, message) == message.text


def test_delete_handler(client, user):
    def next_step():
        ...
    client.register_next_step_handler(user.login, next_step)
    handlers = client.next_step_handler.get_handlers()
    assert len(handlers) == 1
    client.next_step_handler.delete_handler(user.login)
    assert len(handlers) == 0


def test_get_handler_for_message(client, json_message):
    @client.on_message(phrase="/hello")
    def hello(fix_message):
        return "handled"
    assert client._get_handler_for_message(json_message=json_message) == hello


def test_get_message_objects(client, json_message):
    msg_obj = client._get_message_objects(message_json=json_message)
    assert type(msg_obj) is Message
    assert msg_obj.callback_data == {'phrase': '/hello'}
