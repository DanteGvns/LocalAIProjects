import sys
from socket import *

#needed import for ctrl + c stopping
import signal
signal.signal(signal.SIGINT, signal.SIG_DFL)

portNum = 54783
severRunning = "The Sever is Running..."

def main():

    #Make a port and listen
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',portNum))
    serverSocket.listen(1)

    #show the server is running
    print(severRunning)

    #start loop of always waiting for a connection
    while True:
        try:
            #accept client and opent a client spesific socket
            connectionSocket, addr = serverSocket.accept()

            #read in 1024 bytes of data and store it as a string
            sentence = connectionSocket.recv(1024).decode()

            #capitalize that string
            capitalizedSentence = sentence.upper()

            #send it back to that client socket
            connectionSocket.send(capitalizedSentence.encode())
        except KeyboardInterrupt:
            print("\nServer shutting down...")
            serverSocket.close()
            sys.exit(0)    
        except Exception as e:
            print(f"Error: {e}")
        finally:
            #close client spesific socket, main lister remains open and loop restarts
            connectionSocket.close()

        
if __name__ == "__main__":
    main()