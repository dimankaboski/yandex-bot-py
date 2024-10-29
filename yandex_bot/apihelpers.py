import json
import os

from requests import Session
from yandex_bot.types import Button, Poll, Chat

BASE_URL = "https://botapi.messenger.yandex.net/bot/v1"


def clear_kwargs_values(new_data):
    data = {}
    for key, value in new_data.items():
        if value:
            data.update({key:value})
    return data


def _make_request(token: str, method_url: str, method: str, data: dict = None):
    headers = {
        "Authorization": f"OAuth {token}",
    }
    s = Session()
    if not token:
        raise Exception("Token is missing")
    request_url = f"{BASE_URL}{method_url}"
    if method == "GET":
       resp = s.request(method, request_url, headers=headers, params=data) 
    elif method == "POST":
        if data:
            data = json.dumps(data)
        headers.update({"Content-Type": "application/json"})
        resp = s.request(method, request_url, headers=headers, data=data)
    data = _check_result(resp)
    s.close()
    return data


def _download_file(token: str, method_url: str, method: str, file_id: str, file_path: str):
    request_url = f"{BASE_URL}{method_url}"
    headers = {
        "Authorization": f"OAuth {token}"
    }
    s = Session()
    r = s.request(method, request_url, headers=headers, params={"file_id": file_id}, stream=True)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        raise Exception(r.json())


def _check_result(result):
    if result.status_code != 200:
        print(result)
        print(result.json())
        raise Exception("Bad request")
    return result.json()


def get_updates(token: str, last_update_id: int = 0):
    data = _make_request(token, f"/messages/getUpdates?offset={last_update_id}&limit=1", "GET")
    return data['updates']


def send_message(token: str,
                 login: str,
                 text: str,
                 **kwargs):
    data = {
        "login": login,
        "text": text
    }
    data.update(**kwargs)
    data = _make_request(token, "/messages/sendText/", "POST", data)
    return data['message_id']


def create_poll(token: str, poll: Poll, **kwargs):
    data = dict()
    data.update(poll.to_dict())
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(token, "/messages/createPoll/", "POST", data)
    return data['message_id']


def get_poll_results(token: str, message_id: int, **kwargs):
    data = {
        "message_id": int(message_id)
    }
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(token, "/polls/getResults/", "GET", data)
    return data


def get_poll_voters(token: str, message_id:int, answer_id: int, **kwargs):
    data = {
        "message_id": message_id,
        "answer_id": answer_id
    }
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(token, "/polls/getVoters/", "GET", data)
    return data


def chat_create(token: str, chat: Chat, **kwargs):
    data = {}
    data.update(**kwargs)
    data.update(chat.to_dict())
    data = _make_request(token, "/chats/create/","POST", data)
    return data["chat_id"]


def change_chat_users(token: str, data: dict):
    data = _make_request(token, "/chats/updateMembers/","POST", data)
    return data


def get_file(token: str, file_id: str, file_path: str) -> str:
    if not os.path.exists(file_path):
        raise Exception("Path not found")
    _download_file(token, method_url="/messages/getFile/", method="GET", file_id=file_id, file_path=file_path)
    return file_path

