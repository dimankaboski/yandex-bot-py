import os

from dotenv import load_dotenv

from yandex.client import Client
from yandex.types import Button, Poll, Chat, User

load_dotenv()

bot = Client(os.getenv("YANDEX_BOT_KEY"))


@bot.on_message(phrase="/start")
def command_start(message):
    btn = Button(text="Проверить список активных обращений", phrase="/tickets")
    btn2 = Button(text="Зарегистрировать новое обращение")
    btn3 = Button(text="Создать опрос", phrase="/createpoll")
    btn4 = Button(text="Узнать результаты опроса", phrase="/getpollresults")
    btn5 = Button(text="Список проголосовавших", phrase="/getpollvoters")
    btn6 = Button(text="Список проголосовавших", phrase="/chatcreate")
    bot.send_message(message.user.login, "Привет! Вы начали работу с ботом", inline_keyboard=[btn, btn2, btn3, btn4, btn5, btn6])


@bot.on_message(phrase="/tickets")
def command_start(message):
    bot.send_message(message.user.login, "Введи свое имя")
    bot.register_next_step_handler(message.user.login, type_your_name)


@bot.on_message(phrase="/createpoll")
def command_poll(message):
    bot._create_poll(message.user.login, poll=Poll(title="title", answers=["1", "2"]))


@bot.on_message(phrase="/getpollresults")
def command_poll(message):
    result = bot._get_poll_results(message.user.login, 1729861577195041)
    print(result)


@bot.on_message(phrase="/getpollvoters")
def command_poll(message):
    result = bot._get_poll_voters(message.user.login, 1729861577195041, 0)
    print(result)


@bot.on_message(phrase="/chatcreate")
def command_poll(message):
    chat = Chat(name="chat", description="desc")
    users = [User(login='a.leushkin@krastsvetmet.ru', id='312c0b09-d819-955f-6558-1694275d674e')]
    chat.set_admins(users)
    chat.set_members(users)
    bot._chat_create(chat=chat)
    

def type_your_name(message):
    file_path = bot.get_file(message.file, "test")
    bot.send_message(message.user.login, "Вы ввели свое имя")


bot.run()
