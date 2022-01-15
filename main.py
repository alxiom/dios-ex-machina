import os
import usb.core
import datetime
import time

running_time = 3 * 60 * 60  # second
now = time.time()
end_time = now + running_time


def parse_text(file_name, slicing=20):
    text = []
    with open(file_name, "r", encoding="utf-8") as text_file:
        read_line = text_file.readlines()
        for line in read_line:
            line = line.strip()
            if len(line) > 0:
                line_slice = [line[i:i + slicing] for i in range(0, len(line), slicing)]
                text.extend(line_slice)
    return text


text_wave = parse_text("text_wave.txt")
text_click = parse_text("text_click.txt")

text_wave_length = len(text_wave)
text_click_length = len(text_click)

text_wave_cnt = 0
text_click_cnt = 0

sleep_second = 3.0
id_vendor = 0x1fc9
id_product = 0x2016
printers = []
devices = usb.core.find(idVendor=id_vendor, idProduct=id_product, find_all=True)
for i, device in enumerate(devices):
    print(f"Printer #{i + 1}")
    print(f"Bus: {device.bus}")
    print(f"Address: {device.address}")
    print("--")
    printers.append(usb.core.find(idVendor=id_vendor, idProduct=id_product, bus=device.bus, address=device.address))

print("Start Printing")
while end_time - now > 0:
    for i, printer in enumerate(printers):
        if i == 0:
            message = text_wave[text_wave_cnt % text_wave_length]
            text_wave_cnt += 1
        elif i == 1:
            message = text_click[text_click_cnt % text_click_length]
            text_click_cnt += 1
        else:
            date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
            message = f"#{i + 1} / {date_time}"
        printer.reset()
        lpr = os.popen("lpr", "w")
        lpr.write(message)
        lpr.close()
        print(i, message)
        time.sleep(sleep_second)
    now = time.time()
