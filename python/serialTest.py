import serial

ser = serial.Serial('/dev/ttyACM0', 9600)
print(ser.name)

while True:
    print(ser.readline().decode("utf-8"))