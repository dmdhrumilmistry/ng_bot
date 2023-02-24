from pyngrok import ngrok
from prettytable.prettytable import PrettyTable
from os import getenv


import logging

logging.getLogger("pyngrok").setLevel(logging.WARNING)
logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

class NgrokWrapper:
    def __init__(self) -> None:
        NGROK_AUTH_TOKEN = getenv('NGROK_AUTH_TOKEN', None)
        if not NGROK_AUTH_TOKEN:
            raise ValueError(
                f'NGROK_AUTH_TOKEN needs to be set in environment variable or .env file inside project folder')

        ngrok.set_auth_token(NGROK_AUTH_TOKEN)

        self.tunnels = []

    def __create_tunnel(self, port: int, protocol: str):
        if port and protocol:
            self.tunnels.append(ngrok.connect(port, protocol, bind_tls=True))
            return True

        return False

    def connect(self, tunnels: dict):
        http_ports = tunnels.get('http', [])
        tcp_ports = tunnels.get('tcp', [])

        # expose http ports
        for http_port in http_ports:
            if self.__create_tunnel(http_port, 'http'):
                logger.info(f'HTTPS {http_port} opened successfully')
            else:
                logger.error(f'Failed to open HTTP port {http_port}')

        # expose tcp ports
        for tcp_port in tcp_ports:
            if self.__create_tunnel(tcp_port, 'tcp'):
                logger.info(f'TCP {tcp_port} opened successfully')
            else:
                logger.error(f'Failed to open TCP port {tcp_port}')

    def get_tunnels_links(self) -> list:
        tunnel_details = []
        tunnels = ngrok.get_tunnels()

        for tunnel in tunnels:
            tunnel_details.append(
                {
                    'name': tunnel.name,
                    'url': tunnel.public_url,
                    'addr': tunnel.config.get('addr')
                }
            )
        
        return tunnel_details

    def print_tunnel_links(self):
        tunnel_links = self.get_tunnels_links()
        table = PrettyTable(['Name', 'Ngrok Link','Addr'])
        for tunnel in tunnel_links:
            table.add_row([tunnel.get('name', None), tunnel.get('url', None), tunnel.get('addr', None)])

        print(table)

    def start(self, print_links: bool = True):
        if print_links:
            self.print_tunnel_links()

        ngrok_process = ngrok.get_ngrok_process()
        try:
            ngrok_process.proc.wait()
        except KeyboardInterrupt:
            logger.info("Closing Ngrok processes")
            ngrok.kill()
