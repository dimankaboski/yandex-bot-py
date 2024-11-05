import requests

from time import sleep
import threading

from yandex_bot.types import User, Message, Chat, Button, Poll
import yandex_bot.apihelpers as api
from yandex_bot.types import User, Message, Chat, Button, File, Image
from yandex_bot.handlers import MemoryStepHandler


class Client:
    def __init__(self, api_key: str, ssl_verify: bool = True):
        self.api_key = api_key
        self.handlers = []
        self.next_step_handler = MemoryStepHandler()
        self.is_closed = False
        self.last_update_id = 0
        self.ssl_verify = ssl_verify

    def _build_handler_dict(self, handler, phrase):
        return {"function": handler, "phrase": phrase}

    def run(self):
        print("Bot initialized. Start polling...")
        self._start_polling()

    def _is_closed(self):
        return self.is_closed

    def _get_message_objects(self, message_json) -> Message:
        images = []
        file = None
        if message_json.get("images"):
            for image in message_json.get("images")[0]:
                images.append(Image(**image))
        if message_json.get("file"):
            file = File(**message_json.get("file"))
        user = User(**message_json["from"])
        if not message_json.get("text"):
            message_json["text"] = ""
        message = Message(**message_json, user=user, pictures=images, attachment=file)
        return message

    def _run_handler(self, handler, message: Message):
        handler(message)

    def _get_updates(self):
        data = api.get_updates(self, self.last_update_id + 1)
        for json_message in data:
            self.last_update_id = json_message["update_id"]
            handler = self._get_handler_for_message(json_message)
            message: Message = self._get_message_objects(json_message)
            if handler:
                self._run_handler(handler, message)
            else:
                print(f"Unhandled message {message}")

    def _get_handler_for_message(self, json_message: dict):
        next_step_handlers = self.next_step_handler.get_handlers()
        if next_step_handlers:
            next_step_handler = next_step_handlers.get(json_message["from"]["login"])
            if next_step_handler:
                self.next_step_handler.delete_handler(json_message["from"]["login"])
                return next_step_handler
        first_message_word = json_message.get("text", "").split(" ")[0]
        if not first_message_word:
            return None
        if json_message.get("callback_data") and json_message.get("callback_data").get(
            "phrase"
        ):
            first_message_word = json_message.get("callback_data").get("phrase")
        for handler in self.handlers:
            if first_message_word == handler["phrase"]:
                return handler["function"]
        return None

    def _start_polling(self):
        try:
            while not self._is_closed():
                t = threading.Thread(
                    target=self._get_updates(), name="bot_polling", daemon=True
                ).start()
                sleep(1)
        except KeyboardInterrupt:
            print("Exit Bot. Good bye.")
            self.is_closed = True

    def register_next_step_handler(self, user_login: int, callback):
        self.next_step_handler.register_handler(user_login, callback)

    def on_message(self, phrase):
        def decorator(handler):
            self.handlers.append(self._build_handler_dict(handler, phrase))
            return handler

        return decorator

    def send_message(
        self,
        text: str,
        login: str = "",
        chat_id: str = "",
        reply_message_id: int = 0,
        disable_notification: bool = False,
        important: bool = False,
        disable_web_page_preview: bool = False,
        inline_keyboard: [Button] = None,
    ):
        if not chat_id and not login:
            raise Exception("Please provide login or chat_id")
        if inline_keyboard is None:
            inline_keyboard = []
        if inline_keyboard:
            inline_keyboard = [btn.to_dict() for btn in inline_keyboard]
        data = api.send_message(
            self,
            text,
            login=login,
            chat_id=chat_id,
            reply_message_id=reply_message_id,
            disable_notification=disable_notification,
            important=important,
            disable_web_page_preview=disable_web_page_preview,
            inline_keyboard=inline_keyboard,
        )
        return data

    def create_poll(
        self,
        poll: Poll,
        chat_id: str = None,
        login: str = None,
        disable_notification: bool = False,
        important: bool = False,
        disable_web_page_preview: bool = False,
    ) -> int:
        """
        The method allows you to create surveys.
        url: https://botapi.messenger.yandex.net/bot/v1/messages/createPoll/

        :param Poll poll: Poll class
        :param str login: User login who will receive the message
        :param str chat_id: Group chat ID where to send a message
        :param message_id: Chat class
        :param answer_id: The number of the answer option for which voters are requested
        :return int: message_id contains information about the sent survey message.
        """
        if not chat_id and not login:
            raise Exception("Please provide login or chat_id")
        data = api.create_poll(
            self,
            poll,
            login=login,
            chat_id=chat_id,
            disable_notification=disable_notification,
            important=important,
            disable_web_page_preview=disable_web_page_preview,
        )
        return data

    def get_poll_results(
        self,
        message_id: int,
        chat_id: str = None,
        login: str = None,
        invite_hash: str = None,
    ) -> dict:
        """
        The method allows you to obtain the results of a user survey in a chat: the total number of voters and the number of votes cast for each answer option.
        url: https://botapi.messenger.yandex.net/bot/v1/polls/getResults/

        :param int message_id: Chat poll message ID
        :param str login: User login who will receive the message
        :param str chat_id: Group chat ID where to send a message
        :param str invite_hash: Hash of the invitation link if the bot is not already in the chat
        :return dict: The result of a successful request is a response with code 200 and a JSON body containing information about the survey results.
        """
        if not chat_id and not login:
            raise Exception("Please provide login or chat_id")
        data = api.get_poll_results(
            self,
            message_id,
            chat_id=chat_id,
            login=login,
            invite_hash=invite_hash,
        )
        return data

    def get_poll_voters(
        self,
        message_id: int,
        answer_id: int,
        login: str = None,
        chat_id: str = None,
        invite_hash: str = None,
        limit: int = None,
        cursor: int = None,
    ) -> dict:
        """
        The method allows you to obtain the number and list of survey participants who voted for a certain answer option.
        url: https://botapi.messenger.yandex.net/bot/v1/polls/getVoters/

        :param int message_id: Chat poll message ID
        :param int answer_id: The number of the answer option for which voters are requested
        :param str login: User login who will receive the message
        :param str chat_id: Group chat ID where to send a message
        :param str invite_hash: Hash of the invitation link if the bot is not already in the chat
        :param int limit: The maximum number of votes that will be received in response to a request
        :param int cursor: Voice ID, starting from which the list of voters will be formed
        :return dict: The result of a successful request is a response with code 200 and a body with JSON containing a list of voters
        """
        if not chat_id and not login:
            raise Exception("Please provide login or chat_id")
        data = api.get_poll_voters(
            self,
            message_id,
            answer_id,
            login=login,
            chat_id=chat_id,
            invite_hash=invite_hash,
            limit=limit,
            cursor=cursor,
        )
        return data

    def create_chat(self, chat: Chat, is_channel: bool = False) -> int:
        """
        Method creates a chat or channel
        url: https://yandex.ru/dev/messenger/doc/ru/api-requests/chat-create

        :param chat: Chat class
        :param is_channel: Create a chat or channel
        :return int: Created chat ID
        """
        data = api.chat_create(self, chat, is_channel=is_channel)
        return data

    def change_chat_users(
        self,
        chat_id: str,
        members: [User] = None,
        admins: [User] = None,
        subscribers: [User] = None,
        remove: [User] = None,
    ):
        data = {"chat_id": chat_id}
        if members:
            data.update(members=[{"login": user.login} for user in members])
        if admins:
            data.update(admins=[{"login": user.login} for user in admins])
        if subscribers:
            data.update(subscribers=[{"login": user.login} for user in subscribers])
        if remove:
            data.update(remove=[{"login": user.login} for user in remove])
        data = api.change_chat_users(self, data)
        return data

    def send_file(self, login): ...

    def get_file(self, file: File, save_path: str) -> str:
        file_path = f"{save_path}/{file.name}"
        data = api.get_file(self, file.id, file_path)
        return data

    def delete_message(self, message_id: int, login: str = "", chat_id: str = ""):
        if not chat_id and not login:
            raise Exception("Please provide login or chat_id")
        data = api.delete_message(
            self, message_id, login=login, chat_id=chat_id
        )
        return data

    def get_user_link(self, login: str):
        data = api.get_user_link(self, login=login)
        return data
