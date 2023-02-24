# Run as a Service

This README contains instructions how to run ng_bot as a service on Debian based distros.

## Instructions

- Create directory for storing .env file

    ```bash
    mkdir ~/.ng_bot
    ```

- Add secrets to `~/.ng_bot/.env`

    ```bash
    nano ~/.ng_bot/.env

    # Add below configuration to file
    NGROK_AUTH_TOKEN='your_auth_token'
    TELE_BOT_TOKEN='telegram_bot_token'
    ALLOWED_USER_IDS=tele_user_id1, tele_user_id2, tele_user_id3
    DISCORD_WEBHOOK_URL='webhook-url'
    ```

- Copy `ng_bot.service` file to `/etc/systemd/system/` directory 

    ```bash
    sudo cp ng_bot.service /etc/systemd/system/
    ```

- Configure service file based on your needs.

- Reload systemd and start `ng_bot` service

    ```bash
    # reload systemd:
    $ sudo systemctl daemon-reload

    # Then, start your service using the following command:
    $ sudo systemctl start ng_bot

    # You can check the status of your service with:
    $ sudo systemctl status ng_bot

    # To enable your service to start automatically at boot, use the following command:
    $ sudo systemctl enable ng_bot
    ```
