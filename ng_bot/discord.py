from requests import post
from json import dumps

def send_discord_message(webhook_url: str, message: dict):
    message = {
        'content':message
    }
    with post(url=webhook_url, json=message, headers={'Content-Type': 'application/json'}) as res:
        if 200 <= res.status_code < 300:
            return True

    return False
