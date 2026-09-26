import socket

PORT = 54783
BUFFER_SIZE = 4096


def main():
    client_socket = None

    try:
        ip_address = input("Please enter the server's IP address: ")

        client_socket = socket.create_connection(
            (ip_address, PORT),
            timeout=10
        )

        # Ollama may take longer than the connection timeout to respond.
        client_socket.settimeout(None)

        prompt = input("Input prompt: ")
        client_socket.sendall(prompt.encode("utf-8"))

        response_chunks = []

        # The server closes this connection after sending its response.
        while True:
            chunk = client_socket.recv(BUFFER_SIZE)

            if not chunk:
                break

            response_chunks.append(chunk)

        response = b"".join(response_chunks).decode("utf-8")
        print("From server:", response)

    except ConnectionRefusedError:
        print("Server not found or not accepting connections.")
    except socket.gaierror:
        print("Invalid hostname or DNS lookup failed.")
    except TimeoutError:
        print("Connection timed out.")
    except KeyboardInterrupt:
        print("\nClient shutting down...")
    except Exception as error:
        print(f"Error: {error}")
    finally:
        if client_socket is not None:
            client_socket.close()


if __name__ == "__main__":
    main()