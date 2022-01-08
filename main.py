import os
import usb.core
import datetime
import time

is_print = False
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
while is_print:
    for i, printer in enumerate(printers):
        printer.reset()
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        lpr = os.popen("lpr", "w")
        lpr.write(f"#{i + 1}\n\n현재 시간\n\n{now}\n\n--\n\n")
        lpr.close()
        time.sleep(sleep_second)
