import sys
import socket

portNum = 54783
ipPrompt = "Please enter the Severs IP address:"
sendPrompt = "Input lowercase sentence:"
returnPrompt = "From Server: "

def main():
    #define clientSocket for later error handling
    clientSocket = None

    try:
        
        #get IP address from user
        #print(ipPrompt)
        ipAddress = input(ipPrompt)

        #Make a port and attenpt to connect with the ip address gotten from user
        clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        clientSocket.connect((ipAddress,portNum))

        #get message to send to sever
        sendMsg = input(sendPrompt)
        #send message
        clientSocket.send(sendMsg.encode())

        #listen for message from server
        serverMsg = clientSocket.recv(1024)
        print (returnPrompt, serverMsg.decode())

        #handling common errors
    except ConnectionRefusedError:
        print("Server not found or not accepting connections.")

    except socket.gaierror:
        print("Invalid hostname or DNS lookup failed.")

    except TimeoutError:
        print("Connection timed out.")

    except KeyboardInterrupt:
        print("\nClient shutting down...")
        if clientSocket is not None:
            clientSocket.close()
        sys.exit(0) 

    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    finally:
        #close socket
        if clientSocket is not None:
            clientSocket.close()

if __name__ == "__main__":
    main()