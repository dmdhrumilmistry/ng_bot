from tele_ng_bot.ngrok_wrapper import NgrokWrapper

ngrok_client = NgrokWrapper()
ngrok_client.connect(
    tunnels={
        "http": [8000],
        "tcp": []
    }
)

print(ngrok_client.tunnels)
