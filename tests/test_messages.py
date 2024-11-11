import pytest

from yandex_bot import Button, Poll, Chat, User, Message, Client


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


def test_get_message_objects(client, message):
    ...
