import os
import usb.core
import datetime
import time

running_time = 3 * 60 * 60  # second
now = time.time()
end_time = now + running_time

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
        printer.reset()
        date_time = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        lpr = os.popen("lpr", "w")
        message = f"#{i + 1} / {date_time}"
        lpr.write(message)
        lpr.close()
        print(message)
        time.sleep(sleep_second)
    now = time.time()
