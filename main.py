import os
import usb.core
import datetime

is_print = False

printers = []
devices = usb.core.find(idVendor=0x1fc9, idProduct=0x2016, find_all=True)
for i, device in enumerate(devices):
    print(f"Printer #{i + 1}")
    print(f"Bus: {device.bus}")
    print(f"Address: {device.address}")
    print("--")
    printers.append(usb.core.find(idVendor=0x1fc9, idProduct=0x2016, bus=device.bus, address=device.address))

print("Start Printing")
while is_print:
    for printer in printers:
        printer.reset()
        now = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        lpr = os.popen("lpr", "w")
        lpr.write(f"현재 시간\n\n{now}\n\n--\n\n")
        lpr.close()
