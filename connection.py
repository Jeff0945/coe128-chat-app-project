import socket
import threading

ADDRESS = ('127.0.0.1', 52972)
client_connections = []


def connect_or_start_server():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.settimeout(1)

    try:
        client_socket.connect(ADDRESS)
    except:
        client_socket.close()
        start_server()


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(ADDRESS)

    run_connection_listener(server_socket)


def run_connection_listener(sock):
    connection_listener = threading.Thread(target=accept_connections, args=(sock,))
    connection_listener.start()

    print("Server connection listener started.")


def accept_connections(server_socket):
    server_socket.listen(100)

    while True:
        connection, address = server_socket.accept()
        client_connections.append(connection)

        print(f"Client {address[0]} connected")
