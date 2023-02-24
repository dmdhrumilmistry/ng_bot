# Ng-Bot

Ngrok Bot (Ng-Bot) publishes updated ngrok URLs to telegram chat ids and restricts other users to access the bot or on discord using webhook url.

> `Note`: This bot may be used for malicious purposes too. Its upto users how they use this tool/bot. Author is not responsible for user's action in any manner.

## Installation

### Using pip

- Install from pypi

  ```bash
  python3 -m pip install ng-bot
  ```

  **OR**

- Install from main branch

  ```bash
  python3 -m pip install git+https://github.com/dmdhrumilmistry/ng_bot.git
  ```

### Manual

- Clone repo

  ```bash
  git clone --depth=1 https://github.com/dmdhrumilmistry/ng_bot.git
  ```

- Change directory

  ```bash
  cd ng_bot
  ```

- Install package

  ```bash
  python3 -m pip install .
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
  DISCORD_WEBHOOK_URL='webhook-url' 
  ```

  > Above variables can also be stored in environment variables

- Start application

  ```bash
  # for telegram
  python3 -m ng_bot --http 8080 --tcp 22 4444 --platform telegram

  # for discord
  python3 -m ng_bot --tcp 22 --platform discord
  ```

## Security

- Disable password based authentication in `/etc/ssh/ssh_config`
  
  ```config
  PasswordAuthentication no
  ```

- Add client's public key to server's `~/.ssh/authorized_keys` file

> Now only users with authorized public key can access server
