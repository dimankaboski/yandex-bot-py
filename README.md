# Yandex messenger bot python


### It is still under development and it has regular updates, do not forget to update it regularly

### Getting started
```
pip install yandex-bot-py
```
> Depends requests >= 2.32.3

#### Example

``` Python
from yandex_bot import Client, Button, Message, User

bot = Client(os.getenv("YANDEX_BOT_KEY"))

@bot.on_message(phrase="/start")
def command_start(message):
    btn = Button(text="What is your name", phrase="/name")
    bot.send_message(message.user.login, "Select an action", inline_keyboard=[btn])


@bot.on_message(phrase="/name")
def command_start(message):
    bot.send_message(message.user.login, "Type your name")
    bot.register_next_step_handler(message.user.login, type_your_name)


def type_your_name(message):
    bot.send_message(message.user.login, f"Your name is {message.text}")


bot.run()
```

### Message processing
To process all messages starting with a specific phrase, use decorator `@bot.on_message`. 
Specify in the parameters `phrase` to handle messages that begin with the specified phrase.
> `phrase` checks the first word of the text from the user

``` Python
@bot.on_message(phrase="/start")
def command_start(message):
    bot.send_message(message.user.login, f"Hello, {message.user.login}")
```

To send a message use `bot.send_message`. You can provide `chat_id` or `login` there.

```Python
bot.send_message(message.user.login, "Hello, I'm bot")
```

`inline_keyboard` is used to add buttons to a chat with a user. Just create a Button class and provide `text` (The text on the button).
You can provide `phrase` for fast binding to the processing function, or you can provide any `callback_data` to a Button and it will be returned on `Message` class in `callback_data`.

```Python
btn = Button(text="My button", phrase="/data", callback_data={"foo": "bar", "bar": "foo"})
bot.send_message(message.user.login, "Select an action", inline_keyboard=[btn])
```

### Handling next step
For example, to wait for a response from a user to a question, you can use `bot.register_next_step_handler`. This method will store the session with the current user. The method includes:
1. `user_login` - the username of the user from whom to wait for the message;
2. `callback` - the handler function

```Python
@bot.on_message(phrase="/name")
def get_user_name(message):
    bot.send_message(message.user.login, "Type your name")
    bot.register_next_step_handler(message.user.login, type_your_name)

def type_your_name(message):
    bot.send_message(message.user.login, f"Your name is {message.text}")
```