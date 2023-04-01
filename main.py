import cv2,time,sys
from PIL import Image, ImageTk
import config
from src.camera import *
from src.uhfRfidScanner import UhdRfidScanner
from src.models import Product
from src.apiBot import ApiBot
from src.screen import ScreenWidget, QApplication
from src.sql_db import ProductDatabase

class Ser:
    def die(self,text):
        print("DIE:",text)

ser = Ser()

class App:
    current_session_products = []
    scanSatate = 0
    hasClient = False
    currentClient = None
    processing = False


    def __init__(self):
        self.faceDetector = FaceDetector(config=config , ser=ser)
        self.uhdRfidScanner = UhdRfidScanner()
        self.db = ProductDatabase('db.sqlite3')
        self.uhdRfidScanner.connect()
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
                products = self.db.select_all_by_ids(ids = uhf_product_ids)
                for product in products:
                    if not product['id'] in self.current_session_products.keys():
                        self.current_session_products[product['id']] = 1
                    else:
                        self.current_session_products[product['id']] += 1
                self.purchase_products_by_user()
                print(products)
                #self.screen_update(products)
        return frame
        
    def add_product(self, product):
        pass

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
if __name__ == '__main__':
    app = App()