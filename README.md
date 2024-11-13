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
    bot.send_message("Select an action", login=message.user.login, inline_keyboard=[btn])


@bot.on_message(phrase="/name")
def command_start(message):
    bot.send_message("Type your name", login=message.user.login)
    bot.register_next_step_handler(message.user.login, type_your_name)


def type_your_name(message):
    bot.send_message(f"Your name is {message.text}", login=message.user.login)


bot.run()
```

### Message processing
To process all messages starting with a specific phrase, use decorator `@bot.on_message`. 
Specify in the parameters `phrase` to handle messages that begin with the specified phrase.
> `phrase` checks the first word of the text from the user

``` Python
@bot.on_message(phrase="/start")
def command_start(message):
    bot.send_message(f"Hello, {message.user.login}", login=message.user.login)
```

To send a message use `bot.send_message`. You can provide `chat_id` or `login` there.

```Python
bot.send_message("Hello, I'm bot", login=message.user.login)
```

```Python
bot.send_message("Hello, I'm bot", chat_id="12512571242")
```

`inline_keyboard` is used to add buttons to a chat with a user. Just create a Button class and provide `text` (The text on the button).
You can provide `phrase` for fast binding to the processing function, or you can provide any `callback_data` to a Button and it will be returned on `Message` class in `callback_data`.

```Python
btn = Button(text="My button", phrase="/data", callback_data={"foo": "bar", "bar": "foo"})
bot.send_message("Select an action", login=message.user.login, inline_keyboard=[btn])
```
You can also `delete_message()` in chats and channels where the bot is located.
Pass the `message_id` and the `login` or `chat_id` to the method. Return `message_id` deleted message
```Python
data = bot.delete_message(12356532, login="test@login.com")
```
### Handling next step
For example, to wait for a response from a user to a question, you can use `bot.register_next_step_handler()`. This method will store the session with the current user. The method includes:
1. `user_login` - the username of the user from whom to wait for the message;
2. `callback` - the handler function

```Python
@bot.on_message(phrase="/name")
def get_user_name(message):
    bot.send_message("Type your name", login=message.user.login)
    bot.register_next_step_handler(message.user.login, type_your_name)

def type_your_name(message):
    bot.send_message(f"Your name is {message.text}", login=message.user.login)
```
### Unhandled messages

To process messages for which no handler is specified, use the decorator `@bot.unhandled_message()`. By default, messages without a handler are not processed in any way

```Python
@bot.unhandled_message()
def unhandled(message: Message):
    print(message)
```



### Send file or image
The method allows you to send files to private or group chats. 

`send_file()` example. Returns a dictionary containing the `message id` and `file id`
```Python
data = bot.send_file("files/test.txt", login="login@login.ru")
```
`send_image()` example. Returns the `message id` with the sent image.
```Python
data = bot.send_image("files/test.jpg", login="login@login.ru")
```

### Chats
`create_chat()`

The method allows you to create a chat or channel, add its description and icon, assign administrators, add members (for the chat) or subscribers (for the channel).
```Python
@bot.on_message(phrase="/create_chat")
def command_create_chat(message: Message):
    chat = Chat(name="Test chat 1", description="Description")
    users = [User(login="login1@login.ru"), User(login="login2@login.ru")]
    chat.set_admins(users)
    chat_id = bot.create_chat(chat=chat)
```
`change_chat_users()`

The method allows you to add and remove participants to the chat, add and remove subscribers to the channel, as well as appoint chat or channel administrators.

```Python
data = bot.change_chat_users("3424234", admins=[User(login="login2")], 
                            remove=[User(login="login")])
```