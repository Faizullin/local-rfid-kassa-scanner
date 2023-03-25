import ctypes
import time
import platform

import ctypes

pygame = None


from pygame.locals import *
from ctypes import *

import time
from datetime import datetime
from .models import Product


class UhdRfidScanner:
    PATH_TO_DRIVER = "./data/driver/raspberry/libCFComApi.so"
    PORT = "/dev/ttyUSB0"

    def connect(self):
        self.Objdll = ctypes.cdll.LoadLibrary(self.PATH_TO_DRIVER)
        print(self.Objdll)
        if self.Objdll.CFCom_OpenDevice(self.PORT.encode(), 115200) == 1:   # COM$
            print("OpenSuccess")
        else:
            raise Exception("OpenError")
        self.Objdll.CFCom_ClearTagBuf()
    
    def update(self):
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
            print("Found",rfid_addresses)
            return len(rfid_addresses.keys())>0,rfid_addresses
        return False,None
                