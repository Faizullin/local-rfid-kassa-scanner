import cv2,time,sys
import tkinter as tk
from PIL import Image, ImageTk
import config
from src.camera import *
from src.uhfRfidScanner import UhdRfidScanner
from src.models import Product
from src.apiBot import ApiBot

class Ser:
    def die(self,text):
        print("DIE:",text)


ser = Ser()
faceDetector = FaceDetector(config=config , ser=ser)
uhdRfidScanner = UhdRfidScanner()
uhdRfidScanner.connect()
faceDetector.index = 1
faceDetector.method = 1
faceDetector.load_faces()
faceDetector.on()




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
    def __init__(self, master):
        self.scanner = uhdRfidScanner
        self.items = [
            Product(1,"meat",12),
            Product(2,"bread",12),
            Product(3,"hallo",12),
        ]

        self.listbox = tk.Listbox(master)
        self.scrollbar = tk.Scrollbar(master, orient=tk.VERTICAL, command=self.listbox.yview)
        self.listbox.config(yscrollcommand=self.scrollbar.set)
        
        # Add items to the listbox
        for item in self.items:
            item_frame = tk.Frame(master)
            item_frame.pack(side=tk.TOP, fill=tk.X)
           
            label = tk.Label(item_frame, text=item.name)
            label.pack(side=tk.LEFT)
            remove_button = tk.Button(item_frame, text="Remove",  command=lambda obj=item: self.listbox.delete(self.listbox.get(0, tk.END).index(obj.name)))
            remove_button.pack(side=tk.RIGHT)
            self.listbox.insert(tk.END, item.name)           


        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.video = faceDetector


        self.frame = tk.Frame(master, width=1500, height=1100)
        self.frame.pack_propagate(0)
        self.frame.pack(side=tk.TOP, anchor=tk.NE)
        self.canvas = tk.Canvas(self.frame, width=1200, height=900)
        self.canvas.pack()

        self.update_video()


    def update_video(self):
        ret, frame = self.video.read()
        if ret:
            frame = self.video.resize(frame, width=500)
            detected,frame = self.video.detect_face(frame)
            if detected:
                print("GET Products")
                self.scanner.update()




            img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(img)
            img_tk = ImageTk.PhotoImage(img)
            self.canvas.create_image(0, 0, image=img_tk, anchor=tk.NW)
            self.canvas.img_tk = img_tk
        
        # Schedule the next update
        self.canvas.after(10, self.update_video)
        
    def remove_item(self, index):
        del self.items[index]
        self.listbox.delete(index)

root = tk.Tk()
app = App(root)
root.mainloop()
faceDetector.off()