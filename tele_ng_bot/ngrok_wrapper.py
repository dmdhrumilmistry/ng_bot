from pyngrok import ngrok
import logging

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)


class NgrokWrapper:
    def __init__(self) -> None:
        self.tunnels = []

    def __create_tunnel(self, port: int, protocol: str):
        if port and protocol:
            self.tunnels.append(ngrok.connect(port, protocol))
            return True

        return False

    def connect(self, tunnels: dict = {"http": [], "tcp": []}):
        http_ports = tunnels.get('http', [])
        tcp_ports = tunnels.get('tcp', [])
        
        # expose http ports
        for http_port in http_ports:
            if self.__create_tunnel(http_port, 'http'):
                logging.info(f'HTTP {http_port} opened successfully')
            else:
                logging.error(f'Failed to open HTTP port {http_port}')

        # expose tcp ports
        for tcp_port in tcp_ports:
            if self.__create_tunnel(tcp_port, 'http'):
                logging.info(f'HTTP {tcp_port} opened successfully')
            else:
                logging.error(f'Failed to open HTTP port {tcp_port}')

