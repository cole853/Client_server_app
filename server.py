import threading

from communication import *


# the function to start and run the server side
# type "**file" followed by a file path to send a file to the client
# type "**bye" to stop the function
def server_program():
    host = socket.gethostname()
    port = 5000

    # make a socket for messages
    server_socket = socket.socket()
    server_socket.bind((host, port))

    # create connection with the client
    server_socket.listen(2)
    print("Waiting for connection...")
    conn, address = server_socket.accept()
    print("Message connection from: " + str(address))

    # make a socket for files
    file_socket = socket.socket()
    file_socket.bind((host, 5001))

    # create connection with the client
    file_socket.listen(2)
    file_conn, file_address = file_socket.accept()

    # create an instance of the communication object for send and receive functions
    comm = communication(conn, file_conn)

    # start thread to receive messages
    receive_thread = threading.Thread(target=comm.receive_text)
    receive_thread.start()

    # start thread to send messages
    send_thread = threading.Thread(target=comm.send_text)
    send_thread.start()

    # start thread to receive files
    receive_file_thread = threading.Thread(target=comm.receive_file)
    receive_file_thread.start()

    # wait for threads to finish
    receive_thread.join()
    send_thread.join()
    receive_file_thread.join()

    # close sockets
    conn.close()
    file_conn.close()


if __name__ == '__main__':
    server_program()
