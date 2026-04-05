import serial
import time

class ArduinoManager:
    def __init__(self, port="COM5", baudrate=9600):
        self.serialInst = serial.Serial()
        self.serialInst.port = port
        self.serialInst.baudrate = baudrate
        self.serialInst.timeout = 1

    def connect(self):
        try:
            self.serialInst.open()
            # Arduinos reset on connection; wait 2s for it to boot
            time.sleep(2) 
            print(f"Connected to {self.serialInst.port}")
            return True
        except Exception as e:
            print(f"Failed to connect: {e}")
            return False

    def send(self, command):
        if self.serialInst.is_open:
            self.serialInst.write((command + "\n").encode('utf-8'))
        print(command)

    def close(self):
        self.serialInst.close()
