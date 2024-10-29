import os

from dotenv import load_dotenv

from yandex.client import Client
from yandex.types import Button, Poll, Chat, User, Message

load_dotenv()

bot = Client(os.getenv("YANDEX_BOT_KEY"))
CHAT = "0/0/2bbbef01-e7be-4a1a-9825-97f117e1cb58"

@bot.on_message(phrase="/start")
def command_start(message):
    btn = Button(text="Проверить список активных обращений", phrase="/tickets")
    btn2 = Button(text="Зарегистрировать новое обращение")
    btn3 = Button(text="Создать опрос", phrase="/createpoll")
    btn4 = Button(text="Узнать результаты опроса", phrase="/getpollresults")
    btn5 = Button(text="Список проголосовавших", phrase="/getpollvoters")
    btn6 = Button(text="Создать чат", phrase="/chatcreate")
    btn7 = Button(text="Изменить пользователей чата", phrase="/chatedit")
    bot.send_message(message.user.login, "Выберите одно из предложенных действий", inline_keyboard=[btn, btn2, btn3, btn4, btn5, btn6, btn7])


@bot.on_message(phrase="/tickets")
def command_start(message):
    bot.send_message(message.user.login, "Введи свое имя")
    print(message.user.id)
    # bot.register_next_step_handler(message.user.login, type_your_name)


@bot.on_message(phrase="/createpoll")
def command_poll(message: Message):
    poll = Poll(title="Какой язык выберете...", answers=["C#", "JavaScript", "Python"], max_choices=2, is_anonymous=True)
    poll_id = bot.create_poll(poll=poll, login=message.user.login)
    print(poll_id)
    last_created_poll = poll_id


@bot.on_message(phrase="/getpollresults")
def command_poll(message):
    result = bot.get_poll_results(message.user.login, MESSAGE_ID_WITH_POLL)
    print(result)


@bot.on_message(phrase="/getpollvoters")
def command_poll(message):
    result = bot.get_poll_voters(message.user.login, MESSAGE_ID_WITH_POLL, 0)
    print(result)


@bot.on_message(phrase="/chatcreate")
def command_poll(message):
    chat = Chat(name="Тестовый чат с Алёшей", description="Алеша Дима и бот")
    users = [User(login=message.user.login, id=message.user.id), User(login="a.leushkin@krastsvetmet.ru", id="312c0b09-d819-955f-6558-1694275d674e")]
    chat.set_admins(users)
    # chat.set_members(users)
    chat_id = bot.create_chat(chat=chat)
    print(chat_id)


@bot.on_message(phrase="/chatedit")
def command_poll(message):
    response = bot.change_chat_users(chat_id=CHAT, remove=[User(login="a.vizulis@krastsvetmet.ru", id="")])
    print(response)


def type_your_name(message):
    # file_path = bot.get_file(message.file, "test")
    bot.send_message(message.user.login, "Вы ввели свое имя")


bot.run()
