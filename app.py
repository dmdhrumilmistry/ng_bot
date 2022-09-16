from tele_ng_bot.ngrok_wrapper import NgrokWrapper

import logging
logging.getLogger("ngrok_wrapper").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

ngrok_client = NgrokWrapper()
ngrok_client.connect(
    tunnels={
        "http": [8000],
        "tcp": []
    }
)

ngrok_client.start()