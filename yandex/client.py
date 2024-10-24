import requests

from time import sleep
import threading

from yandex.types import User, Message, Chat, Button
from yandex.apihelpers import get_updates, send_message
from yandex.handlers import MemoryStepHandler


class Client:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.handlers = []
        self.next_step_handler = MemoryStepHandler()
        self.is_closed = False
        self.last_update_id = 0

    def _build_handler_dict(self, handler, phrase):
        return {
            'function': handler,
            'phrase': phrase
        }

    def run(self):
        print("Bot initialized. Start polling...")
        self._start_polling()
        # self.runner = threading.Thread(target=, name="bot_polling").start()

    def _is_closed(self):
        return self.is_closed

    def _get_message_objects(self, message_json) -> Message:
        user = User(**message_json["from"])
        message = Message(**message_json, user=user)
        return message

    def _run_handler(self, handler, message: Message):
        try:
            handler(message)
        except Exception as e:
            raise Exception

    def _get_updates(self):
        data = get_updates(self.api_key, self.last_update_id + 1)
        for json_message in data:
            self.last_update_id = json_message['update_id']
            handler = self._get_handler_for_message(json_message)
            message: Message = self._get_message_objects(json_message)
            if handler:
                self._run_handler(handler, message)
            else:
                print(f"Unhandled message {message}")

    def _get_handler_for_message(self, json_message: dict):
        next_step_handlers = self.next_step_handler.get_handlers()
        if next_step_handlers:
            next_step_handler = next_step_handlers.get(json_message["from"]['login'])
            if next_step_handler:
                self.next_step_handler.delete_handler(json_message["from"]['login'])
                return next_step_handler
        first_message_word = json_message['text'].split(" ")[0]
        if json_message.get("callback_data") and json_message.get("callback_data").get("phrase"):
            first_message_word = json_message.get("callback_data").get("phrase")
        for handler in self.handlers:
            if first_message_word == handler['phrase']:
                return handler['function']
        return None

    def _start_polling(self):
        try:
            while not self._is_closed():
                t = threading.Thread(target=self._get_updates(), name="bot_polling", daemon=True).start()
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

    def send_message(self, login: str,
                     text: str,
                     reply_message_id: int = 0,
                     disable_notification: bool = False,
                     important: bool = False,
                     disable_web_page_preview: bool = False,
                     inline_keyboard: [Button] = None):
        if inline_keyboard is None:
            inline_keyboard = []
        if inline_keyboard:
            inline_keyboard = [btn.to_dict() for btn in inline_keyboard]
        data = send_message(self.api_key, login, text, reply_message_id=reply_message_id, disable_notification=disable_notification,
                            important=important, disable_web_page_preview=disable_web_page_preview, inline_keyboard=inline_keyboard)
        return data

    def create_chat(self, chat: Chat, is_channel: bool = False) -> str:
        """
        Method creates a chat or channel
        url: https://yandex.ru/dev/messenger/doc/ru/api-requests/chat-create
        :param chat: Chat class
        :param is_channel: Create a chat or channel
        :return: chat_id
        """
        method = "/chats/create/"
        try:
            r = requests.post(BASE_URL + method, headers=self.headers, data=chat.to_json())
            data = r.json()
        except Exception as e:
            return "error"
        return data.get("chat_id")
