import serial
import time
import struct

ARDUINO_UNO = serial.Serial(port="COM7", baudrate=9600, timeout=0.1)

def send_angle(theta: float, phi: float) -> bytes:   
    binary_data = struct.pack("<ff", theta, phi)
    ARDUINO_UNO.write(binary_data)
    time.sleep(0.05)
    data = ARDUINO_UNO.readline()
    return data

def main():
    print("Hello from solarfour!")
    while True:
        try:
            theta = float(input("Enter theta: "))
            phi = float(input("Enter phi : "))
            response = send_angle(theta=theta, phi=phi)
            print(response.decode("utf-8"))
        except ValueError:
            print("Enter float data")


if __name__ == "__main__":
    main()
