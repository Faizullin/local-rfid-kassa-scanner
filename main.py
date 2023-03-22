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

from sqlite_save import arr_str3, arr_name, arr_price


url = '127.0.0.1:8000'


# datetime object containing current date and time
now = datetime.now()




Objdll = cdll.LoadLibrary("./libCFComApi.so")
print(Objdll)


if Objdll.CFCom_OpenDevice("/dev/ttyUSB0".encode(), 115200) == 1:   # open device
    print("OpenSuccess")
else:
    print("OpenError")



Objdll.CFCom_ClearTagBuf()    # start to get data

icon_arr=['champune.png','suhariki1.png','choazh.png','chokaz.png','colgate.png',
      'dadasok.png','IMG_2058-removebg-preview.png','lays.png','vaphli.png','vaphli2.png','bag.png','bag.png']



shifer="231kodsfawfjfds32jo42n422o24n5p2j52n2ds"



id = arr_str3()

name = arr_name()

price = arr_price()


class Product:
    id = ''
    name = ''
    price = 0
    state = 0
    
    def __init__(self,id,name,price):
        self.id = id
        self.name = name
        self.price = price



deltime=0
timer=[]
class Screen:
    display_surface = None
    font = None

    def start(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((1008, 1920))
        pygame.display.set_caption('LIST!')
    
        white = (255, 255, 255)
        green = (0, 255, 0)
        blue = (0, 0, 128)

        self.display_surface.fill(white)
        pygame.display.flip()
        # rise = pg.image.load('rise2.png')
        # rise.set_colorkey((255, 255, 255))
        # rise_small = pygame.transform.scale(rise, (50, 30))
        # rise_icon = rise_small.get_rect(bottomright=(50, 70))
        # display_surface.blit(rise_small, rise_icon)
        # pygame.display.update()#updat

        self.font = pygame.font.Font('freesansbold.ttf', 20)

    def keyboardQuitUpdate(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                return 1
        pygame.display.update()
        return 0
    
    def keyboardPurchaseUpdate(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1
        return 0
    
    

class MainScanner:
    screen = None
    current_session_products = []

    def user_purchase(self, user=1,product='product'):
        print("Make_request",user,product)

    def read(self):
        self.arrBuffer = bytes(9182)
        self.iTagLength = c_int(0)
        self.iTagNumber = c_int(0)
        ret = Objdll.CFCom_GetTagBuf(self.arrBuffer, byref(self.iTagLength), byref(self.iTagNumber))

    def available(self):
        return self.iTagNumber.value > 0
    
    def start(self):
        self.run()

    def run(self):
        sim='0xe2 0x80 0x68 0x94 0x0 0x0 0x40 0x1d 0x93 0x36 0x89 0xb8 '
        while True:
            now = time.time()

            if self.screen.keyboardQuitUpdate():
                return;

            self.read()
            if self.available():
                iIndex = int(0)
                iLength = int(0)
                bPackLength = c_byte(0)
                
                for iIndex in range(0,  self.screen.iTagNumber.value):
                    bPackLength = screen.arrBuffer[iLength]
                    str3 = ""
                    i = int(0)
                    for i in range(2, bPackLength - 1):
                        str1 = hex(screen.arrBuffer[1 + iLength + i])
                        str3 = str3 + str1 + " "
                    
                    session_product = Product(str3,f'Product {str3}',100)
                    if str3 in [session_product.id for session_product in self.current_session_products]:
                        #timer[a.index(str3)]=10000
                        session_product.state = 0

                    if str3 not in [session_product.id for session_product in self.current_session_products] and str3 in ids:
                        print("YES")
                        self.current_session_products.append(session_product)
                        print(self.current_session_products, len(self.current_session_products))
                        

                    # elif str3 == sim and len(a) > 0:
                    #     print("+++++++++")
                    #     delid = []
                    #     chek = []
                    #     now = datetime.now()
                    #     for i in range(len(a)):
                    #         delid.append(id.index(a[i]))
                    #         chek.append(name[id.index(a[i])])
                    #         chek.append(str(price[id.index(a[i])]))
                    #     chek.append(str(suma))
                    #     chek.append(now.strftime("%d/%m/%Y#%H:%M:%S"))
                        

                    #     #save
                    #     with open('/home/adminu/django_uhf_rfid_shop/uhf_rfid_shop/main/base.txt','a') as f:
                    #         f.write(str((chek))+"*")
                            

                    #     #delead
                    #     for i in delid:
                    #         id[i] = "0"
                    #     a=[]
                        

                    st=60
                    sum_of_products=0
                    dl=50
                    #save
                        

                    #screen
                    pygame.display.update()
                    screen.display_surface.fill((255, 255, 255))
                    for session_product in self.current_session_products:
                        

                        #icon
                        icon = pygame.image.load("photo/"+session_product.id+".jpg")
                        icon.set_colorkey((255, 255, 255))
                        icon_small = pygame.transform.scale(icon, (50, 30))
                        icon_ad = icon_small.get_rect(bottomright=(50, dl+25))
                        screen.display_surface.blit(icon_small, icon_ad)
                        pygame.display.update()
                        

                        #data
                        dt_string = now.strftime("%d/%m/%Y#%H:%M:%S")
                        now_txt = screen.font.render(dt_string,True,(80,80,80))
                        screen.display_surface.blit(now_txt, (60, 0))
                            

                        #name price
                        sum_of_products += session_product.price
                        text = session_product.name + ": " +str(session_product.price) + "tg"
                        text_data = screen.font.render( text, True,(80,80,80))
                        screen.display_surface.blit(text_data, (st, dl))
                        dl+=40

                    str_sum_of_products_data ="Total: " + str(sum_of_products) + "tg"#suma to > str 
                    sum_data = screen.font.render( str_sum_of_products_data, True,(80,80,80))#text suma
                    screen.display_surface.blit(sum_data, (st, dl+10))       
            

            time.sleep(0.0001)
            if len(self.current_session_products) > 0: 
                if(self.screen.keyboardPurchaseUpdate()):
                    for i in range(len(self.current_session_products)):
                        self.current_session_products[i].state += 1
                        if(self.current_session_products[i].state >= 90):
                            self.current_session_products.pop(i)
                    screen.display_surface.fill((255, 255, 255))


            
        
    










screen = Screen()
mainScanner = MainScanner()
mainScanner.screen = screen

mainScanner.start()