import ctypes
import time
import platform

import ctypes

pygame = None


from threading import Thread
from ctypes import *

import time
from datetime import datetime
from .models import Product
import config


class UhdRfidScanner:
    PATH_TO_DRIVER = ""
    PORT = "/dev/ttyUSB0"
    current_data = {}
    state = False
    test = False

    def __init__(self):
        self.PATH_TO_DRIVER = config.PATHS['driver']

    def connect(self):
        if self.test:
            print("OpenSuccess")
            return
        self.Objdll = ctypes.cdll.LoadLibrary(self.PATH_TO_DRIVER)
        print(self.Objdll)
        if self.Objdll.CFCom_OpenDevice(self.PORT.encode(), 115200) == 1:   # COM$
            print("OpenSuccess")
        else:
            raise Exception("OpenError")
        self.Objdll.CFCom_ClearTagBuf()

    def start(self):
        Thread(target=self.run,daemon=True).start()
        
    def run(self):
        while True:
            if not self.state:
                time.sleep(0.5)
                continue
            self.current_data = {}
            if self.test:
                self.current_data = {'1':1,'3':1, '4': 1}
                time.sleep(2)
                continue

            arrBuffer = bytes(9182)
            iTagLength = c_int(0)
            iTagNumber = c_int(0)
            ret = self.Objdll.CFCom_GetTagBuf(arrBuffer, byref(iTagLength), byref(iTagNumber))
            if iTagNumber.value > 0:
                iIndex = int(0)
                iLength = int(0)
                bPackLength = c_byte(0)
                
                rfid_addresses = {}
                for iIndex in range(0, iTagNumber.value):
                    bPackLength = arrBuffer[iLength]
                    str3 = ""
                    i = int(0)
                    for i in range(2, bPackLength - 1):
                        str1 = hex(arrBuffer[1 + iLength + i])
                        str3 = str3 + str1 + " "
                    if str3 in rfid_addresses.keys():
                        rfid_addresses[str3] +=1
                    else:
                        rfid_addresses[str3] = 1
                #print("Found",rfid_addresses)
                self.current_data = rfid_addresses
                time.sleep(0.6)

    def getCurrentData(self):
        return self.current_data.copy()

    def on(self):
        self.state = True

    def off(self):
        self.state = False

