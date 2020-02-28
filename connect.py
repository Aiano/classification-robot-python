import serial

ser = None


def init_serial():
    global ser
    try:
        ser = serial.Serial("/dev/ttyUSB0", 9600, timeout=5)
    except Exception as exc:
        print(exc)
        print("Plz check out you serial port.")
        exit(1)


def write_serial(data: str):
    global ser
    if ser is None:
        print("Error occur in function write_serial : Serial hasn't been inited.")
        exit(1)
    ser.write(data.encode('utf-8'))


def read_line_serial():
    global ser
    if ser is None:
        print("Error occur in function read_line_serial : Serial hasn't been inited.")
        exit(1)
    data = ser.readline()

    return data.decode('utf-8')
