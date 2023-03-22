import ctypes
import time
import platform

import ctypes
from ctypes import *

import pygame, sys
import pygame as pg


from pygame.locals import *
from ctypes import *

import time
from datetime import datetime


url = '127.0.0.1:8000'


# datetime object containing current date and time
now = datetime.now()

pygame.init()
display_surface = pygame.display.set_mode((1008, 1920))
pygame.display.set_caption('LIST!')

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

display_surface.fill(white)
pygame.display.flip()
# rise = pg.image.load('rise2.png')
# rise.set_colorkey((255, 255, 255))
# rise_small = pygame.transform.scale(rise, (50, 30))
# rise_icon = rise_small.get_rect(bottomright=(50, 70))
# display_surface.blit(rise_small, rise_icon)
# pygame.display.update()#updat

font = pygame.font.Font('freesansbold.ttf', 20)


Objdll = cdll.LoadLibrary("./libCFComApi.so")
print(Objdll)


if Objdll.CFCom_OpenDevice("/dev/ttyUSB0".encode(), 115200) == 1:   # open device
    print("OpenSuccess")
else:
    print("OpenError")



Objdll.CFCom_ClearTagBuf()    # start to get data

icon_arr=['champune.png','suhariki1.png','choazh.png','chokaz.png','colgate.png',
      'dadasok.png','IMG_2058-removebg-preview.png','lays.png','vaphli.png','vaphli2.png','bag.png','bag.png']

a=[]

shifer="231kodsfawfjfds32jo42n422o24n5p2j52n2ds"

sim='0xe2 0x80 0x68 0x94 0x0 0x0 0x40 0x1d 0x93 0x36 0x89 0xb8 '

id=['0xe2 0x0 0x0 0x1d 0x62 0x3 0x1 0x75 0x25 0x0 0x99 0xb ',
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x50 0x13 0x1f 0xd2 0x15 0xe0 ',
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x50 0x13 0x1f 0xd2 0x15 0xbc ',#3
    '0xe2 0x0 0x0 0x1d 0x62 0x3 0x1 0x86 0x26 0x0 0xa2 0xd9 ',
    '0xe2 0x0 0x0 0x1d 0x62 0x3 0x1 0x95 0x25 0x20 0xb2 0xa9 ',
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x50 0x6 0xe5 0xf6 0x1d 0x68 ',#6
    '0xe2 0x0 0x0 0x1d 0x62 0x3 0x1 0x72 0x26 0x0 0x91 0x82 ',
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x40 0x13 0x1f 0xd2 0x15 0xbe ',
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x40 0x6 0xe5 0xf6 0x21 0x4e ',#9
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x40 0x6 0xe5 0xf6 0x21 0x2d ',
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x40 0x13 0x1f 0xd2 0x15 0xcf ',
    '0xe2 0x80 0x68 0x94 0x0 0x0 0x50 0x6 0xe5 0xf6 0x25 0x12 ',#12
    ]

name=['Шампунь wash&go', 'Хрус team кальмар', 'Яшкино шоколад ', 'Шоколад Казахстан', 'Colgate зубная паста 50мл', 'Сок DaDa 0.5л',
      'Сливки 250мл','Lays паприка 81г','Яшкино вафельный сендвич','Яшкино Мягкие вафли','test','Alpen']

price=[400, 350, 170, 110, 570, 170, 380,165,550,3200,9999,670]

deltime=0
timer=[]
while True:
    now = datetime.now()
    #pygame
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
    
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
            
            if str3 in a:
                timer[a.index(str3)]=10000
            #read base
            with open('/home/adminu/django_uhf_rfid_shop/uhf_rfid_shop/main/base.txt') as f:
                lines = f.readline()
            lines=str(lines)
            basetxt = lines[2:-2]
            print(basetxt)
            #main
            print("a"+str3+'a')
            if str3 not in a and str3 in id:
                print("YES")
                a.append(str3)
                print(a)
                timer.append(10000)
                print(len(a))
                
            #basetxt chek
            elif str3 == sim and len(a) > 0:
                print("+++++++++")
                delid = []
                chek = []
                now = datetime.now()
                for i in range(len(a)):
                    delid.append(id.index(a[i]))
                    chek.append(name[id.index(a[i])])
                    chek.append(str(price[id.index(a[i])]))
                chek.append(str(suma))
                chek.append(now.strftime("%d/%m/%Y#%H:%M:%S"))
                
                #save
                with open('/home/adminu/django_uhf_rfid_shop/uhf_rfid_shop/main/base.txt','a') as f:
                    f.write(str((chek))+"*")
                    
                #delid
                for i in delid:
                    id[i] = "0"
                a=[]
                



            
            #int
            st=60
            suma=0
            dl=50
                
            #screen
            pygame.display.update()#update
            display_surface.fill((255, 255, 255))
            for k in a:
                in_id=id.index(k)
                
                #icon
                icon = pygame.image.load(icon_arr[in_id])
                icon.set_colorkey((255, 255, 255))
                icon_small = pygame.transform.scale(icon, (50, 30))
                icon_ad = icon_small.get_rect(bottomright=(50, dl+25))
                display_surface.blit(icon_small, icon_ad)
                pygame.display.update()#updat
                
                #data
                dt_string = now.strftime("%d/%m/%Y#%H:%M:%S")
                now_txt = font.render(dt_string,True,(80,80,80))
                display_surface.blit(now_txt, (60, 0))
                    
                #name price
                suma+=price[in_id]
                text = name[in_id] + ": " +str(price[in_id]) + "tg"
                text1 = font.render( text, True,(80,80,80))
                display_surface.blit(text1, (st, dl))
                dl+=40
                    
            #Summa
            strsuma="Total: " + str(suma) + "tg"#suma to > str 
            suma1 = font.render( strsuma, True,(80,80,80))#text suma
            display_surface.blit(suma1, (st, dl+10))#print suma       
    
    #timer
    time.sleep(0.0001)
    if len(a) > 0:    
        for i in range(len(timer)):
            timer[i]=timer[i]-1
            if timer[i]<=0:
                del a[i]
                del timer[i]
                display_surface.fill((255, 255, 255))
                break


        
        
    










