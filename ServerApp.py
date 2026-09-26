import socket
from OllamaClient import ask

import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

PORT = 54783
BUFFER_SIZE = 4096


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(("", PORT))
        server_socket.listen(1)

        print("The server is running...")

        try:
            while True:
                connection_socket, address = server_socket.accept()

                with connection_socket:
                    try:
                        prompt = connection_socket.recv(BUFFER_SIZE).decode("utf-8")
                        response = ask("qwen3:4b", prompt)
                        connection_socket.sendall(response.encode("utf-8"))
                    except Exception as error:
                        print(f"Client error: {error}")

        except KeyboardInterrupt:
            print("\nServer shutting down...")


if __name__ == "__main__":
    main()