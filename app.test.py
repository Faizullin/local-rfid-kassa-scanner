import cv2,time,sys
import tkinter as tk
from PIL import Image, ImageTk
import config
from src.camera import *
from src.uhfRfidScanner import UhdRfidScanner
from src.models import Product
from src.apiBot import ApiBot
from src.screen import ScreenWidget, QApplication

class Ser:
    def die(self,text):
        print("DIE:",text)


ser = Ser()





# class SerialScanner:
#     current_session_products = []

#     def user_purchase(self, user=1,product='product'):
#         print("Make_request",user,product)

#     def read(self):
#         self.arrBuffer = bytes(9182)
#         self.iTagLength = c_int(0)
#         self.iTagNumber = c_int(0)
#         ret = Objdll.CFCom_GetTagBuf(self.arrBuffer, byref(self.iTagLength), byref(self.iTagNumber))

#     def available(self):
#         return self.iTagNumber.value > 0
    
#     def start(self):
#         self.run()

#     def update(self):
#         pass

#     def run(self):
#         #sim='0xe2 0x80 0x68 0x94 0x0 0x0 0x40 0x1d 0x93 0x36 0x89 0xb8 '
#         while True:
#             now = time.time()
#             if self.screen.keyboardQuitUpdate():
#                 return

#             self.read()
#             if self.available():
#                 iIndex = int(0)
#                 iLength = int(0)
#                 bPackLength = c_byte(0)
                
#                 for iIndex in range(0,  self.screen.iTagNumber.value):
#                     bPackLength = screen.arrBuffer[iLength]
#                     str3 = ""
#                     i = int(0)
#                     for i in range(2, bPackLength - 1):
#                         str1 = hex(screen.arrBuffer[1 + iLength + i])
#                         str3 = str3 + str1 + " "
                    
#                     session_product = Product(str3,f'Product {str3}',100)
#                     if str3 in [session_product.id for session_product in self.current_session_products]:
#                         #timer[a.index(str3)]=10000
#                         session_product.state = 0

#                     if str3 not in [session_product.id for session_product in self.current_session_products] and str3 in ids:
#                         print("YES")
#                         self.current_session_products.append(session_product)
#                         print(self.current_session_products, len(self.current_session_products))
                        

#                     # elif str3 == sim and len(a) > 0:
#                     #     print("+++++++++")
#                     #     delid = []
#                     #     chek = []
#                     #     now = datetime.now()
#                     #     for i in range(len(a)):
#                     #         delid.append(id.index(a[i]))
#                     #         chek.append(name[id.index(a[i])])
#                     #         chek.append(str(price[id.index(a[i])]))
#                     #     chek.append(str(suma))
#                     #     chek.append(now.strftime("%d/%m/%Y#%H:%M:%S"))
                        

#                     #     #save
#                     #     with open('/home/adminu/django_uhf_rfid_shop/uhf_rfid_shop/main/base.txt','a') as f:
#                     #         f.write(str((chek))+"*")
                            

#                     #     #delead
#                     #     for i in delid:
#                     #         id[i] = "0"
#                     #     a=[]
                        

#                     st=60
#                     sum_of_products=0
#                     dl=50
#                     #save
                        

#                     #screen
#                     pygame.display.update()
#                     screen.display_surface.fill((255, 255, 255))
#                     for session_product in self.current_session_products:
                        

#                         #icon
#                         icon = pygame.image.load("photo/"+session_product.id+".jpg")
#                         icon.set_colorkey((255, 255, 255))
#                         icon_small = pygame.transform.scale(icon, (50, 30))
#                         icon_ad = icon_small.get_rect(bottomright=(50, dl+25))
#                         screen.display_surface.blit(icon_small, icon_ad)
#                         pygame.display.update()
                        

#                         #data
#                         dt_string = now.strftime("%d/%m/%Y#%H:%M:%S")
#                         now_txt = screen.font.render(dt_string,True,(80,80,80))
#                         screen.display_surface.blit(now_txt, (60, 0))
                            

#                         #name price
#                         sum_of_products += session_product.price
#                         text = session_product.name + ": " +str(session_product.price) + "tg"
#                         text_data = screen.font.render( text, True,(80,80,80))
#                         screen.display_surface.blit(text_data, (st, dl))
#                         dl+=40

#                     str_sum_of_products_data ="Total: " + str(sum_of_products) + "tg"#suma to > str 
#                     sum_data = screen.font.render( str_sum_of_products_data, True,(80,80,80))#text suma
#                     screen.display_surface.blit(sum_data, (st, dl+10))       
            

#             time.sleep(0.0001)
#             if len(self.current_session_products) > 0: 
#                 if(self.screen.keyboardPurchaseUpdate()):
#                     for i in range(len(self.current_session_products)):
#                         self.current_session_products[i].state += 1
#                         if(self.current_session_products[i].state >= 90):
#                             self.current_session_products.pop(i)
#                     screen.display_surface.fill((255, 255, 255))





class App:
    current_session_products = []
    scanSatate = 0
    hasClient = False
    currentClient = None
    processing = False


    def __init__(self):
        self.faceDetector = FaceDetector(config=config , ser=ser)
        self.uhdRfidScanner = UhdRfidScanner()
        #self.uhdRfidScanner.connect()
        self.uhdRfidScanner.start()
        self.faceDetector.index = 1
        self.faceDetector.method = 1
        self.faceDetector.load_faces()
        self.faceDetector.on()
        self.apiBot = ApiBot()
        self.apiBot.get_access_token()
        self.screen = QApplication(sys.argv)
        self.screenWidget = ScreenWidget(cameraDetector = self.faceDetector,update_video = self.update_video)
        self.screenWidget.show()
        self.screen.exec_()
    
    def purchase_products_by_user(self):
        res = self.apiBot.purchase_by_user(user = self.currentClient,products=self.current_session_products)
        print("res",res)


    def getIdsFromUhfProducts(self,uhf_ids: dict):
        return [i for i in uhf_ids.keys()]
    
    def update_video(self, frame):
        frame = self.faceDetector.resize(frame, width=500)
        detected, frame = self.faceDetector.detect_face(frame)
        if detected:
            self.hasClient = True
            self.currentClient = detected
            self.scanSatate = 0
            self.uhdRfidScanner.on()
        elif self.scanSatate > 4:
            self.hasClient = False
            self.scanSatate = 0
            self.uhdRfidScanner.off()
        else:
            self.scanSatate += 1

        if self.hasClient:
            print("GET Products")
            uhf_product_ids = self.uhdRfidScanner.getCurrentData()
            if len(uhf_product_ids.keys() ) > 0:
                product_ids = self.getIdsFromUhfProducts(uhf_product_ids)
                for product_id in product_ids:
                    if not product_id in self.current_session_products.keys():
                        self.current_session_products[product_id] = 1
                    else:
                        self.current_session_products[product_id] += 1
                products = self.apiBot.get_products_by_ids(ids = product_ids)
                print(products)
                #self.screen_update(products)
        return frame
        
    def add_product(self, product):
        item_frame = tk.Frame(self.master)
        item_frame.pack(side=tk.TOP, fill=tk.X)
        
        label = tk.Label(item_frame, text=product.name)
        label.pack(side=tk.LEFT)
        remove_button = tk.Button(item_frame, text="Remove",  command=lambda obj=product: self.remove_product(obj))
        remove_button.pack(side=tk.RIGHT)
        increase_button = tk.Button(item_frame, text="+",  command=lambda obj=product: self.increase_button(obj))
        increase_button.pack(side=tk.RIGHT)
        decrease_button = tk.Button(item_frame, text="-",  command=lambda obj=product: self.decrease_button(obj))
        decrease_button.pack(side=tk.RIGHT)
        self.listbox.insert(tk.END, product.name)

    def remove_product(self, index):
        self.current_session_products.remove()
        self.listbox.delete(index)
        #self.listbox.delete(self.listbox.get(0, tk.END).index(obj.name))

    def increase_button(self,product: Product):
        product.quantity += 1
        pass
    def decrease_button(self,product: Product):
        if product.quantity <= 1:
            product.quantity = 1
        else:
            product.quantity -= 1

    def __del__(self):
        self.faceDetector.off()

app = App()