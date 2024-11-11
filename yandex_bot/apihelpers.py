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


def _make_request(client, method_url: str, method: str, data: dict = None):
    headers = {
        "Authorization": f"OAuth {client.api_key}",
    }
    s = Session()
    if not client.api_key:
        raise Exception("Token is missing")
    request_url = f"{BASE_URL}{method_url}"
    if method == "GET":
       resp = s.request(method, request_url, headers=headers, params=data, verify=client.ssl_verify) 
    elif method == "POST":
        if data:
            data = json.dumps(data)
        headers.update({"Content-Type": "application/json"})
        resp = s.request(method, request_url, headers=headers, data=data, verify=client.ssl_verify)
    data = _check_result(resp)
    s.close()
    return data


def _download_file(client, method_url: str, method: str, file_id: str, file_path: str):
    request_url = f"{BASE_URL}{method_url}"
    headers = {
        "Authorization": f"OAuth {client.api_key}"
    }
    s = Session()
    r = s.request(method, request_url, headers=headers, params={"file_id": file_id}, stream=True, verify=client.ssl_verify)
    if r.status_code == 200:
        with open(file_path, 'wb') as f:
            for chunk in r:
                f.write(chunk)
    else:
        raise Exception(r.json())


def _make_file_request(client, method_url: str, data: dict):
    request_url = f"{BASE_URL}{method_url}"
    headers = {
        "Authorization": f"OAuth {client.api_key}",
    }
    s = Session()
    if not client.api_key:
        raise Exception("Token is missing")
    resp = s.request("POST", request_url, headers=headers, files=data, verify=client.ssl_verify)
    data = _check_result(resp)
    s.close()
    return data

def _check_result(result):
    if result.status_code != 200:
        raise Exception(f"Bad request: {result.json()}")
    return result.json()


def get_updates(client, last_update_id: int = 0):
    data = _make_request(client, f"/messages/getUpdates?offset={last_update_id}&limit=5", "GET")
    return data['updates']


def send_message(client,
                 text: str,
                 **kwargs):
    data = {
        "text": text
    }
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(client, "/messages/sendText/", "POST", data)
    return data['message_id']


def create_poll(client, poll: Poll, **kwargs):
    data = dict()
    data.update(poll.to_dict())
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(client, "/messages/createPoll/", "POST", data)
    return data['message_id']


def get_poll_results(client, message_id: int, **kwargs):
    data = {
        "message_id": int(message_id)
    }
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(client, "/polls/getResults/", "GET", data)
    return data


def get_poll_voters(client, message_id:int, answer_id: int, **kwargs):
    data = {
        "message_id": message_id,
        "answer_id": answer_id
    }
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(client, "/polls/getVoters/", "GET", data)
    return data


def chat_create(client, chat: Chat, **kwargs):
    data = {}
    data.update(**kwargs)
    data.update(chat.to_dict())
    data = _make_request(client, "/chats/create/","POST", data)
    return data["chat_id"]


def change_chat_users(client, data: dict):
    data = _make_request(client, "/chats/updateMembers/","POST", data)
    return data


def get_file(client, file_id: str, file_path: str) -> str:
    if not os.path.exists(file_path):
        raise Exception("Path not found")
    _download_file(client, method_url="/messages/getFile/", method="GET", file_id=file_id, file_path=file_path)
    return file_path


def delete_message(client, message_id: int, **kwargs):
    data = {
        "message_id": message_id
    }
    data.update(clear_kwargs_values(kwargs))
    data = _make_request(client, "/messages/delete/", "POST", data)
    return data["message_id"]


def get_user_link(client, login: str):
    data = {
        "login": login
    }
    data = _make_request(client, "/users/getUserLink/", "GET", data)
    return data


def send_file(client, **kwargs):
    data = {}
    data.update(clear_kwargs_values(kwargs))
    file_path = os.path.join(data['document'])
    data['document'] = open(file_path, "rb")
    data = _make_file_request(client, method_url="/messages/sendFile/", data=data)
    return data


def send_image(client, **kwargs):
    data = {}
    data.update(clear_kwargs_values(kwargs))
    file_path = os.path.join(data['image'])
    data['image'] = open(file_path, "rb")
    data = _make_file_request(client, method_url="/messages/sendImage/", data=data)
    return data
