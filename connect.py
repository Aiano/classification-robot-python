import serial
import threading
import queue
import time
from inverse_kinematic.inverse_kinematic import *

ser = None
lock = None
que = queue.Queue(maxsize=0)
is_threading = True
now_x = 10
now_y = 10
now_z = 1
min_delay_time = 0.05


def init_serial():
    global ser, lock, is_threading
    try:
        ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=5)
        lock = threading.Lock()
        t1 = threading.Thread(target=send_loop)
        is_threading = True
        t1.start()
    except Exception as exc:
        print(exc)
        print("Plz check out you serial port.")
        exit(1)


def write_serial(x: float, y: float, z: float, delay_seconds: float, catch_condition: bool):
    # catch_condition :
    #   True -> catch
    #   False -> non_catch
    # delay_second :
    #   min delay_second=0.05
    global que, lock, ser, now_x, now_y, now_z
    if ser is None:
        print("Error occur in function write_serial : Serial hasn't been inited.")
        exit(1)
    times = int(delay_seconds / min_delay_time)
    for i in range(1, times + 1, 1):
        (a1, a2, a3, a4) = inverse_kinematic((x - now_x) / times * i + now_x, (y - now_y) / times * i + now_y,
                                             (z - now_z) / times * i + now_z)
        que.put((a1, a2, a3, a4, catch_condition))
        time.sleep(min_delay_time)
    now_x = x
    now_y = y
    now_z = z


def send_loop():
    # que:
    # (a1,a2,a3,a4,is_catch)
    global ser, que, lock, is_threading

    if ser is None:
        print("Error occur in function send_loop : Serial hasn't been inited.")
        exit(1)
    while is_threading:
        if not que.empty():
            lock.acquire()
            (a1, a2, a3, a4, is_catch) = que.get()
            lock.release()
            data = "#" + str(a1) + "@" + str(a2) + "@" + str(a3) + "@" + str(a4) + "@" + str(int(is_catch)) + "@\n"
            print(data)
            ser.write(data.encode("utf-8"))
        time.sleep(0.02)


def destroy_serial():
    global ser, is_threading
    is_threading = False
    ser.close()


def read_line_serial():
    global ser
    if ser is None:
        print("Error occur in function read_line_serial : Serial hasn't been inited.")
        exit(1)
    data = ser.readline()

    return data.decode('utf-8')
