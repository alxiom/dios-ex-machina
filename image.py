import os
import time

printer_name = "POS__Receipt_Printer"
running_time = 3 * 60 * 60  # second
now = time.time()
end_time = now + running_time

image_length = 20
image_cnt = 0
sleep_second = 12.0

print("Start Printing")
while end_time - now > 0:
    os.system(f"lpr -P {printer_name} pic/pic{image_cnt % image_length:03d}.jpeg")
    image_cnt += 1
    print(f"image_cnt={image_cnt} print pic{image_cnt % image_length:03d}.jpeg")
    time.sleep(sleep_second)
    now = time.time()

