import serial
import time
import os

running_time = 3 * 60 * 60  # second
now = time.time()
end_time = now + running_time

arduino = serial.Serial(
    port="/dev/cu.usbserial-1D1140",
    baudrate=115200,
    timeout=0.1,
)

distance_limit = 1500.0
void_limit = 7.0
block_limit = 1.0
print_limit = 1.0

void_time = 0.0
block_time = 0.0
previous_time = now
lines = "\n" * 20
printer_available = True

while end_time - now > 0:
    now = time.time()
    if arduino.readable():
        res = arduino.readline()
        try:
            distance = float(res) if len(res) > 0 else float("inf")
        except Exception as e:
            print(e)
            distance = float("inf")

        if distance > distance_limit:
            void_time += now - previous_time
            printer_available = void_time > print_limit
        else:
            if printer_available:
                block_time += now - previous_time
            if block_time > block_limit and void_time > void_limit and printer_available:
                print("print!")
                lpr = os.popen("lpr", "w")
                lpr.write(f"void time: {void_time:.2f} sec{lines}.")
                lpr.close()
                void_time = 0.0
                block_time = 0.0
                printer_available = False

        print(f"{now:10.2f} / {distance:4.1f} / {void_time:2.2f} / {block_time:2.2f} / {printer_available}")
        previous_time = now
