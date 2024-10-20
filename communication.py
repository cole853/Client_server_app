import socket
import os
import threading


# this class is used to send and receive messages and files
class communication:
    def __init__(self, socket, file_socket, side="User"):
        self.socket = socket                # the socket for messages
        self.file_socket = file_socket      # the socket for files
        self.stop_threads = False
        self.side = side                    # string to print to indicate messages from the other side of the connection

    # this function receives files only
    def receive_file(self):
        try:
            while not self.stop_threads:
                file_name = self.file_socket.recv(1024).decode()
                file_size = int(self.file_socket.recv(1024).decode())
                print(f"Receiving file: {file_name} ({file_size}, bytes)")

                with open(file_name, 'wb') as file:
                    received = 0
                    while received < file_size:
                        data = self.file_socket.recv(1024)
                        if not data:
                            break
                        file.write(data)
                        received += len(data)

                print(f"File {file_name} received successfully.")
        except:
            print("Error receiving file")

    # this function receives messages only
    def receive_text(self):
        try:
            while not self.stop_threads:
                data = self.socket.recv(1024).decode()
                if not data:
                    print("Connection closed by the server")
                    break

                # if data == "**file":
                #     receive_thread = threading.Thread(target=self.receive_file)
                #     receive_thread.start()
                # else:
                print(self.side + ": " + data)
        except:
            print("Disconnected")

    # this function sends a file
    # called in send_text() function
    def send_file(self, path):
        try:
            # self.socket.send('**file'.encode())
            file_name = os.path.basename(path)
            file_size = os.path.getsize(path)

            self.file_socket.send(file_name.encode())
            self.file_socket.send(str(file_size).encode())

            with open(path, 'rb') as file:
                while True:
                    data = file.read(1024)
                    if not data:
                        break
                    self.file_socket.send(data)

            print(f"File {file_name} sent successfully.")
        except:
            print("Error sending file")

    # this function sends a message or file
    # a new thread is created when a file is sent so that messages can continue
    def send_text(self):
        try:
            while True:
                message = input()
                if message.lower().strip() == '**bye':
                    self.stop_threads = True
                    self.socket.close()
                    self.file_socket.close()
                    break

                vals = message.lower().split(' ', 1)
                if vals[0] == '**file':
                    receive_thread = threading.Thread(target=self.send_file, args=(vals[1],))
                    receive_thread.start()
                else:
                    self.socket.send(message.encode())
        except:
            print("Error sending message")

