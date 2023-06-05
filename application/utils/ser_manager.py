import serial

class SerialManager:
    def __init__(self):
        self.ser = None
    def setup_serial(self, commport, baudrate):
        try:
            self.ser = serial.Serial(commport, baudrate, timeout=0.1)
            return self.ser
        except:
            print("Error in setting up serial port")

    def acquire_data(self):
        return self.ser.readline().decode().strip()
