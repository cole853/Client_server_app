import threading

from communication import *


# the function to start and run the client side
# type "**file" followed by a file path to send a file to the server
# type "**bye" to stop the function
def client_program():
    host = socket.gethostname()
    port = 5000

    # make a socket for messages
    client_socket = socket.socket()
    client_socket.connect((host, port))

    # make another socket for files
    file_socket = socket.socket()
    file_socket.connect((host, 5001))

    # create an instance of the communication object for send and receive functions
    comm = communication(client_socket, file_socket, side="Server")

    # start a thread to receive messages
    receive_thread = threading.Thread(target=comm.receive_text)
    receive_thread.start()

    # start a thread to send messages
    send_thread = threading.Thread(target=comm.send_text)
    send_thread.start()

    # start a thread to receive files
    receive_file_thread = threading.Thread(target=comm.receive_file)
    receive_file_thread.start()

    # wait for threads to complete
    send_thread.join()
    receive_thread.join()
    receive_file_thread.join()

    # close sockets
    client_socket.close()
    file_socket.close()


if __name__ == '__main__':
    client_program()
