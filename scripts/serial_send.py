import serial

def main():
    port = 'COM7'
    baudrate = 9600
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
    except serial.SerialException:
        print(f"Cannot open {port}")
        return

    while True:
        user_input = input("Enter azimuth,altitude: ")
        parts = user_input.split(',')
        if len(parts) != 2:
            print("not valid")
            continue
        azimuth_str = parts[0].strip()
        altitude_str = parts[1].strip()
        if azimuth_str.lstrip('-').replace('.', '', 1).isdigit() and altitude_str.lstrip('-').replace('.', '', 1).isdigit():
            azimuth = float(azimuth_str)
            altitude = float(altitude_str)
            ser.write(f"{azimuth},{altitude}\n".encode())
        else:
            print("not valid")

if __name__ == "__main__":
    main()
