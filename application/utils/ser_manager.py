import serial


def setup_serial(commport, baudrate):
    try:
        ser = serial.Serial(commport, baudrate, timeout=0.1)
        return ser
    except:
        print("Error in setting up serial port")


def acquire_data(ser):
    return ser.readline().decode().strip()
