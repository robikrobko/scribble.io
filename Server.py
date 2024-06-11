import socket
import select

LOGIN_PREFIX = b"CHAT LOGIN "

class Client():
    def __init__(self, server, client_sock, address):
        self._server = server
        self._address = address
        self._socket = client_sock
        self._name = None
        self._buffer = b''
        print("KLIENT VYTVORENY")

    @property
    def socket(self):
        return self._socket

    def received_message(self, message):
        print(self._name, message)
        self._server.send_message(message)
        # Extract IP from the message and notify the server
        ip_address = self.extract_ip_from_message(message)
        if ip_address:
            self._server.notify_ip(ip_address)

    def extract_ip_from_message(self, message):
        # Assuming the message format is "COMMAND IP_ADDRESS"
        parts = message.split()
        if len(parts) == 2 and self.is_valid_ip(parts[1]):
            return parts[1]
        return None

    def is_valid_ip(self, ip):
        try:
            socket.inet_aton(ip)
            return True
        except socket.error:
            return False

    def close(self):
        self._socket.close()
        self._server.remove_client(self)
        print(f"KLIENT ODPOJENY {self._name}")

    def send_message(self, message):
        self.socket.send(message.encode())

    def received(self):
        data = self.socket.recv(1024)
        if not data:
            self.close()
        self._buffer += data
        while b'\n' in self._buffer:
            line, self._buffer = self._buffer.split(b'\n', 1)
            if self._name is None:
                if line.startswith(LOGIN_PREFIX):
                    name = line.removeprefix(LOGIN_PREFIX)
                    if name:
                        self._name = name.decode()
                        print(f"KLIENT PRIHLASENY: {self._name}")
                        continue
                return
            self.received_message(line.decode())

class Server():
    def __init__(self):
        self._server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._server_socket.bind(("0.0.0.0", 20000))
        self._server_socket.listen(1)
        self._clients = []
        self._points = {}
        print("SERVER VYTVORENY")

    def send_message(self, message):
        for client in self._clients:
            client.send_message(message)

    def remove_client(self, client):
        self._clients.remove(client)

    def notify_ip(self, ip_address):
        notify_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        notify_message = "ADD POINTS"
        notify_port = 30000  # Replace with the desired port number
        notify_socket.sendto(notify_message.encode(), (ip_address, notify_port))
        notify_socket.close()
        self.award_points(ip_address)
        print(f"NOTIFICATION SENT TO {ip_address}:{notify_port}")

    def award_points(self, ip_address):
            if ip_address in self._points:
                self._points[ip_address] += 10
            else:
                self._points[ip_address] = 10
            print(f"Points awarded to {ip_address}: {self._points[ip_address]}")

    def run(self):
        while True:
            waiting_sockets = [self._server_socket]
            for client in self._clients:
                waiting_sockets.append(client.socket)
            read_sockets = select.select(waiting_sockets, [], [], 5)[0]
            if self._server_socket in read_sockets:
                client_socket, address = self._server_socket.accept()
                self._clients.append(Client(self, client_socket, address))
            for client in self._clients:
                if client.socket in read_sockets:
                    client.received()

server = Server()
server.run()
