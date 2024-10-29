import os

from dotenv import load_dotenv

from yandex_bot.client import Client
from yandex_bot.types import Button, Poll, Chat, User, Message

load_dotenv()

bot = Client(os.getenv("YANDEX_BOT_KEY"))


@bot.on_message(phrase="/start")
def command_start(message):
    btn = Button(text="What is your name", phrase="/name")
    bot.send_message(message.user.login, "Select an action", inline_keyboard=[btn])


@bot.on_message(phrase="/name")
def command_start(message):
    bot.send_message(message.user.login, "Type your name")
    bot.register_next_step_handler(message.user.login, type_your_name)


@bot.on_message(phrase="/createpoll")
def command_poll(message: Message):
    poll = Poll(title="Question", answers=["Answer 1", "Answer 2", "Answer 3"], max_choices=1, is_anonymous=True)
    message_id = bot.create_poll(poll=poll, login=message.user.login)


@bot.on_message(phrase="/getpollresults")
def command_poll(message):
    result = bot.get_poll_results(0, message.user.login)
    print(result)


@bot.on_message(phrase="/getpollvoters")
def command_poll(message):
    result = bot.get_poll_voters(0, 0, message.user.login)


@bot.on_message(phrase="/chatcreate")
def command_poll(message):
    chat = Chat(name="Chata Number 1", description="Description")
    users = [User("login1"), User("login2")]
    chat.set_admins(users)
    chat_id = bot.create_chat(chat=chat)


@bot.on_message(phrase="/chatedit")
def command_poll(message):
    response = bot.change_chat_users(chat_id="", remove=[User(login="login1")])


def type_your_name(message):
    bot.send_message(message.user.login, f"Your name is {message.text}")


bot.run()
