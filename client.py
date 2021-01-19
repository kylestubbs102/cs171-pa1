import socket
import sys, os
from datetime import date, datetime, timedelta
import time
import threading

HOST = '127.0.0.1'
MAX_DIFFERENCE = float(sys.argv[1])
DRIFT = float(sys.argv[2])
PORT = int(sys.argv[3])

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
current_time = datetime.now()

# diff thread for input if time
def time_thread():
    while True:
        userInput = input()
        if(userInput == "time"):
            hour, minute, second = str(current_time.time()).split(":")
            # temp, hour = hour.split(" ")
            print("Current time is: ","\nsecond: ", second, "\nminute: ", minute, "\nhour: ", hour, flush=True)
        elif (userInput == "exit"):
            # sock.close()
            os._exit(1)

def clock_drift():
    global current_time
    while True:
        current_time += timedelta(seconds=(1+DRIFT))
        time.sleep(1)

def call_server():
    global current_time

    hour0 = datetime.today().hour
    minute0 = datetime.today().minute
    second0 = datetime.today().second

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
        hour1 = int(hour)
        minute1 = int(minute)
        second1 = float(second)

        print("time before update is:","\nsecond: ", second1, "\nminute: ", minute1, "\nhour: ", hour1, flush=True)
        sock.send("request".encode())
        serverTime = sock.recv(1024).decode()

        temp0, temp1, tempSeconds = str(datetime.now().time()).split(":")
        # TT

        hour, minute, second = str(serverTime).split(":")
        # temp, hour = hour.split(" ")
        hour2 = int(hour)
        minute2 = int(minute)
        second2 = float(second)

        print("time after update is:","\nsecond: ", second2, "\nminute: ", minute2, "\nhour: ", hour2, flush=True)
        current_time = datetime(year=int(datetime.today().year), month=int(datetime.today().month), day=int(datetime.today().day), hour=hour2, minute=minute2)
        current_time += timedelta(seconds=second2)

def Main():
    sock.connect((HOST, PORT))
    thread1 = threading.Thread(target=call_server)
    thread2 = threading.Thread(target=clock_drift)
    thread1.start()
    thread2.start()
    thread3 = threading.Thread(target=time_thread)
    thread3.start()

if __name__ == '__main__':
    Main()