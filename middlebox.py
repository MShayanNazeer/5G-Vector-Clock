import socket
import threading

# Configuration
LISTENING_PORT = 8805
DESTINATION_HOST = '127.0.0.1'  # Replace with the actual destination host
DESTINATION_PORT = 5001  # Replace with the actual destination port

def handle_client(client_socket):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.connect((DESTINATION_HOST, DESTINATION_PORT))

        # Start a thread to receive data from the server and send it to the client
        def forward_to_client():
            while True:
                data = server_socket.recv(4096)
                if not data:
                    break
                print(f"Forwarding data from server to client: {data.decode('utf-8', 'ignore')}")
                client_socket.sendall(data)

        # Start a thread to receive data from the client and send it to the server
        def forward_to_server():
            while True:
                data = client_socket.recv(4096)
                if not data:
                    break
                print(f"Received data from client: {data.decode('utf-8', 'ignore')}")
                server_socket.sendall(data)

        # Start the threads
        threading.Thread(target=forward_to_client, daemon=True).start()
        threading.Thread(target=forward_to_server, daemon=True).start()

def start_proxy():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
        proxy_socket.bind(('10.10.1.1', LISTENING_PORT))
        proxy_socket.listen(5)
        print(f"Proxy server listening on 10.10.1.1:{LISTENING_PORT}")

        while True:
            client_socket, addr = proxy_socket.accept()
            print(f"Accepted connection from {addr}")
            threading.Thread(target=handle_client, args=(client_socket,), daemon=True).start()

if __name__ == '__main__':
    start_proxy()
