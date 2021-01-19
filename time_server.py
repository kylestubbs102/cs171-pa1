import socket
import sys, os
import threading
from datetime import datetime, timedelta
import time

HOST = '127.0.0.1'
DELAY = float(sys.argv[1])
PORT = int(sys.argv[2])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, PORT))

# diff thread for input if time
def time_thread(conn, addr):
    while True:
        userInput = input()
        if(userInput == "time"):
            hour, minute, second = str(datetime.now().time()).split(":")
            # temp, hour = hour.split(" ")
            print("Current time is: ","\nsecond: ", second, "\nminute: ", minute, "\nhour: ", hour, flush=True)
        elif (userInput == "exit"):
            # conn.close()
            os._exit(1)


def handle_client(conn, addr):
    while True:
        clientMessage = conn.recv(1024).decode()

        time.sleep(DELAY)
        
        # current_time = str(datetime.now().time())
        hour, minute, second = str(datetime.now()).split(":")
        temp, hour = hour.split(" ")
        print("Server connected to " + str(addr),"\nsecond: ", second, "\nminute: ", minute, "\nhour: ", hour, flush=True)

        time.sleep(DELAY)

        current_time = str(datetime.now().time())
        conn.send(current_time.encode())

def Main():
    sock.listen()
    while True:
        conn, addr = sock.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        thread1 = threading.Thread(target=time_thread, args=(conn, addr))
        thread1.start()

if __name__ == '__main__':
    Main()