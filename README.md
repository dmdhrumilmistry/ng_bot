# Usage

- Create Ngrok account

- Complete Sign Up process

- Add new API key and AUTH TOKEN from [dashboard](https://dashboard.ngrok.com/api)

- Store variables in `.env` file

  ```bash
  NGROK_AUTH_TOKEN='your_auth_token'
  TELE_BOT_TOKEN='telegram_bot_token'
  ALLOWED_USER_IDS=tele_user_id1, tele_user_id2, tele_user_id3
  ```

  > Above variables can also be stored in environment variables

- Start application

  ```bash
  python3 -m tele_ng_bot
  ```
