# Tele-Ng-Bot

Telegram Ngrok Bot (Tele-Ng-Bot) publishes updated ngrok URLs to telegram chat ids and restricts other users to access the bot.

> `Note`: This bot may be used for malicious purposes too. Its upto users how they use this tool/bot. Author is not responsible for user's action in any manner.

## Installation

- Clone repo

  ```bash
  git clone --depth=1 https://github.com/dmdhrumilmistry/tele-ng-bot.git
  ```

- Change directory

  ```bash
  cd tele-ng-bot
  ```

- Install requirements

  ```bash
  python3 -m pip install -r requirements.txt
  ```

## Usage

- Create Ngrok account

- Complete Sign Up process

- Add new AUTH TOKEN from [dashboard](https://dashboard.ngrok.com/get-started/your-authtoken)

- Store variables in `.env` file

  ```bash
  NGROK_AUTH_TOKEN='your_auth_token'
  TELE_BOT_TOKEN='telegram_bot_token'
  ALLOWED_USER_IDS=tele_user_id1, tele_user_id2, tele_user_id3
  ```

  > Above variables can also be stored in environment variables

- Start application

  ```bash
  python3 -m tele_ng_bot --http 8080 --tcp 22 4444
  ```
