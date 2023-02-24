from argparse import ArgumentParser
from ng_bot.ngrok_wrapper import NgrokWrapper
from threading import Thread
from textwrap import dedent
from time import sleep
from requests import get
from requests.exceptions import ConnectionError
from os import getenv
from sys import exit

from .bot import tlbot, send_notification_to_allowed_ids
from .discord import send_discord_message


import logging


logging.getLogger("tele_ng_bot.ngrok_wrapper").setLevel(logging.WARNING)
logger = logging.getLogger(__name__)
ngrok_client = NgrokWrapper()

DISCORD_WEBHOOK_URL = getenv('DISCORD_WEBHOOK_URL', None)


def start_ngrok(http_ports: list[int] = [], tcp_ports: list[int] = []):
    ngrok_client.connect(
        tunnels={
            "http": http_ports,
            "tcp": tcp_ports
        }
    )
    ngrok_client.start()


def send_new_urls_notification(notify_on: str = 'telegram'):
    tunnels_data = ngrok_client.get_tunnels_links()
    message = ''
    for tunnel_data in tunnels_data:
        message += dedent(f'''
        name: {tunnel_data.get('name', None)}
        url: {tunnel_data.get('url', None)}
        addr: {tunnel_data.get('addr', None)}
        --------------------------------
        ''')
    
    match notify_on:
        case 'telegram':
            send_notification_to_allowed_ids(message)
        case 'discord':
            send_discord_message(DISCORD_WEBHOOK_URL, message)


def get_tunnels_data():
    tunnels_data = []
    try:
        response = get(
            url='http://localhost:4040/api/tunnels',
            headers={
            'Accept': 'application/json',
            },
        )
        if 200 <= response.status_code < 300:
            tunnels = response.json().get('tunnels', [])
            for tunnel in tunnels:
                tunnels_data.append(
                    {
                        'name': tunnel.get('name', None),
                        'url': tunnel.get('public_url', None),
                        'addr': tunnel.get('config', {}).get('addr')
                    }
                )
        else:
            logger.warning(
                f'API responded with status code: {response.status_code}')
    except ConnectionError:
        logger.error("Connection Error: ngrok is still starting")

    return tunnels_data


def poll_ngrok_url_change(platform:str):
    prev_urls = []
    while True:
        new_urls = [tunnel_data.get('url', None)
                    for tunnel_data in get_tunnels_data()]

        is_new_url = False
        for new_url in new_urls:
            if new_url not in prev_urls:
                is_new_url = True
                prev_urls.append(new_url)

        if is_new_url:
            send_new_urls_notification(notify_on=platform)

        sleep(5)


def main(http_ports: list[int], tcp_ports: list[int], platform: str):
    threads = []

    threads.append(Thread(target=start_ngrok, args=(http_ports, tcp_ports,)))
    threads.append(Thread(target=get_tunnels_data))
    threads.append(Thread(target=poll_ngrok_url_change, args=(platform,)))

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join(timeout=1.0)

    match platform:
        case 'telegram':
            tlbot.infinity_polling()


if __name__ == '__main__':

    parser = ArgumentParser(
        prog='ng_bot',
    )

    parser.add_argument('--http', dest='http_ports', default=[], nargs='+',
                        type=int, help='web services ports separated by spaces')
    parser.add_argument('--tcp', dest='tcp_ports', default=[], nargs='+',
                        type=int, help='tcp services ports separated by spaces')
    parser.add_argument('-p', '--platform', dest='platform', default='telegram', choices=[
                        'telegram', 'discord'], type=str, help='instructs program to notify on speified platform')

    args = parser.parse_args()

    if not (args.http_ports or args.tcp_ports):
        parser.print_help()
        exit()

    main(
        http_ports=args.http_ports,
        tcp_ports=args.tcp_ports,
        platform=args.platform,
    )
