# networking.py

import socket
from threading import Thread


def client_thread(client_socket, addr, on_message_received):
    print(f"Connection from {addr}")
    while True:
        message = client_socket.recv(1024).decode()
        if not message:
            break
        on_message_received(message)
    client_socket.close()


def start_server(host, port, on_message_received):
    """Starts a simple server that listens for incoming messages and uses the callback function."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        # Start a new thread for each client
        Thread(target=client_thread, args=(client_socket, addr, on_message_received)).start()


def send_message(host, port, message):
    """Sends a message to the specified server."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((host, port))
        if isinstance(message, str):
            message = message.encode()  # Encode string to bytes if not already bytes
        client.send(message)

# Example usage
if __name__ == "__main__":
    import threading

    # Start the server in a separate thread
    server_thread = threading.Thread(target=start_server, args=('localhost', 12345))
    server_thread.start()

    # Send a message from the client
    send_message('localhost', 12345, "Hello, Server!")
