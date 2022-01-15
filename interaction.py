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

distance_threshold = 1000.0
block_threshold = 1.0
skip_threshold = 1.0
print_threshold = 5.0

printer_available = False
lines = "\n" * 20
open_timer = [now, now]
block_timer = [now]

while end_time - now > 0:
    now = time.time()
    if arduino.readable():
        res = arduino.readline()
        try:
            distance = float(res) if len(res) > 0 else float("inf")
        except Exception as e:
            print(e)
            distance = float("inf")

        open_duration = open_timer[-1] - open_timer[0]

        print(f"{now:10.2f} / {distance:4.1f} / {open_duration:2.2f} / {printer_available}")

        if distance < distance_threshold:
            if now - block_timer[-1] < skip_threshold:
                block_timer.append(now)
                if len(block_timer) > 2:
                    block_timer.pop(1)
                block_duration = block_timer[-1] - block_timer[0]
                if block_duration > block_threshold and printer_available:
                    print("print!")
                    printer_available = False
                    lpr = os.popen("lpr", "w")
                    lpr.write(f"void time: {open_duration:.2f} sec{lines}.")
                    lpr.close()
                    block_timer[0] = now
            else:
                block_timer = [now]
        else:
            if now - open_timer[-1] < skip_threshold:
                open_timer.append(now)
                if len(open_timer) > 2:
                    open_timer.pop(1)
                printer_available = open_duration > print_threshold
            else:
                open_timer = [now, now]
