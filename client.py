import socket
import sys
from datetime import date, datetime, timedelta
import time
import threading

HOST = '127.0.0.1'
PORT = int(sys.argv[1])
DRIFT = float(sys.argv[2])
MAX_DIFFERENCE = float(sys.argv[3])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
current_time = datetime.now()

# diff thread for input if time

def clock_drift():
    global current_time
    while True:
        current_time += timedelta(seconds=(1+DRIFT))
        time.sleep(1)

def call_server():
    global current_time

    sock.send("request".encode())
    serverTime = sock.recv(1024).decode()
    hour, minute, second = str(serverTime).split(":")
    # temp, hour = hour.split(" ")
    hour = int(hour)
    minute = int(minute)
    second = float(second)
    print("time after update is:","\nsecond: ", second, "\nminute: ", minute, "\nhour: ", hour, flush=True)
    
    current_time = datetime(year=int(datetime.today().year), month=int(datetime.today().month), day=int(datetime.today().day), hour=hour, minute=minute)
    current_time += timedelta(seconds=second)

    while True:
        time.sleep(MAX_DIFFERENCE/(2 * abs(DRIFT)))

        hour, minute, second = str(current_time.time()).split(":")
        hour = int(hour)
        minute = int(minute)
        second = float(second)

        print("time before update is:","\nsecond: ", second, "\nminute: ", minute, "\nhour: ", hour, flush=True)
        sock.send("request".encode())
        serverTime = sock.recv(1024).decode()

        hour, minute, second = str(serverTime).split(":")
        # temp, hour = hour.split(" ")
        hour = int(hour)
        minute = int(minute)
        second = float(second)

        print("time after update is:","\nsecond: ", second, "\nminute: ", minute, "\nhour: ", hour, flush=True)
        current_time = datetime(year=int(datetime.today().year), month=int(datetime.today().month), day=int(datetime.today().day), hour=hour, minute=minute)
        current_time += timedelta(seconds=second)

def Main():
    sock.connect((HOST, PORT))
    thread1 = threading.Thread(target=call_server)
    thread2 = threading.Thread(target=clock_drift)
    thread1.start()
    thread2.start()

if __name__ == '__main__':
    Main()