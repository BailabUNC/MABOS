import serial


def setup_serial(commport, baudrate):
    try:
        ser = serial.Serial(commport, baudrate, timeout=0.1)
        return ser
    except:
        print("Error in setting up serial port")


def acquire_data(ser):
    channel_data = [0, 0, 0, 0]
    for i in range(4):
        channel_data[i] = ser.readline().decode().strip()
    if channel_data[3] != '/':
        print('error in serial data')
        return
    return channel_data
