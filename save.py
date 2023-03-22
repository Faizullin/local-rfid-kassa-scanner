import ctypes
from ctypes import *

import tkinter as tk
from tkinter import simpledialog

from sqlite_save import save_n_p
from sqlite_save import arr_str3, arr_name, arr_price

from download_photo import save_photo
#box window
ROOT = tk.Tk()
ROOT.withdraw()

#USER_INP = simpledialog.askstring(title="Test",
#                                 prompt="What's your Name?:")




#start
Objdll = cdll.LoadLibrary("./libCFComApi.so")
print(Objdll)


if Objdll.CFCom_OpenDevice("/dev/ttyUSB0".encode(), 115200) == 1:   # open device
    print("OpenSuccess")
else:
    print("OpenError")
arr=[]
def update():
    global arr
    arr = arr_str3()
    





update()
print(arr)




arr2=[]



arrstr3=[]
while True:
    #uhf
    arrBuffer = bytes(9182)
    iTagLength = c_int(0)
    iTagNumber = c_int(0)
    ret = Objdll.CFCom_GetTagBuf(arrBuffer, byref(iTagLength), byref(iTagNumber))
    if iTagNumber.value > 0:
        iIndex = int(0)
        iLength = int(0)
        bPackLength = c_byte(0)
        
        #id find uhf
        for iIndex in range(0,  iTagNumber.value):
            bPackLength = arrBuffer[iLength]

            str3 = ""
            i = int(0)
            for i in range(2, bPackLength - 1):
                str1 = hex(arrBuffer[1 + iLength + i])
                str3 = str3 + str1 + " "
            #read base


            #main
            print(arr)
            print(str3)
            arrstr3.append(str3)
            if len(str3) > 3 and str3 not in arr and str3 not in arr2:
                arr2.append(str3)
                update()
                
                name = simpledialog.askstring(title="Name",
                                  prompt="Product name?:")
                

                price = simpledialog.askstring(title="Price",
                                  prompt="Product price?:")
                

                url = simpledialog.askstring(title="Phot",
                                  prompt="Product photo url?:")
                

                save_photo(name,url)

                
                
  
                
                if str(name) != "None":
                    print("yes")
                    save_n_p(name,price,str3)
                    arrstr3=[]