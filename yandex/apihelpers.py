import json
from requests import Session
from yandex.types import Button

BASE_URL = "https://botapi.messenger.yandex.net/bot/v1"


def _make_request(token: str, method_url: str, method: str, data: dict = None):
    if data:
        data = json.dumps(data)
    headers = {
        "Authorization": f"OAuth {token}",
        "Content-Type": "application/json"
    }
    s = Session()
    if not token:
        raise Exception("Token is missing")
    request_url = f"{BASE_URL}{method_url}"
    resp = s.request(method, request_url, headers=headers, data=data)
    data = _check_result(resp)
    s.close()
    return data


def _check_result(result):
    if result.status_code != 200:
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
