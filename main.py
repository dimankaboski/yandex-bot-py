import os

from yandex.client import Client

from yandex.types import Button

bot = Client(os.getenv("YANDEX_BOT_KEY"))


@bot.on_message(phrase="/start")
def command_start(message):
    btn = Button(text="Проверить список активных обращений", phrase="/tickets")
    btn2 = Button(text="Зарегистрировать новое обращение")
    bot.send_message(message.user.login, "Привет! Вы начали работу с ботом", inline_keyboard=[btn, btn2])


@bot.on_message(phrase="/tickets")
def command_start(message):
    bot.send_message(message.user.login, "Введи свое имя")
    bot.register_next_step_handler(message.user.login, type_your_name)


def type_your_name(message):
    print(message.text)
    bot.send_message(message.user.login, "Вы ввели свое имя")


bot.run()
