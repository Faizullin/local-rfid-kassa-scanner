import cv2,time,sys

import config
from src.camera import *
from src.uhfRfidScanner import UhdRfidScanner
from src.models import Product
from src.apiBot import ApiBot
from src.screen import *
from src.sql_db import ProductDatabase

class Ser:
    def die(self,text):
        print("DIE:",text)

ser = Ser()

class App:
    current_session_products = {}
    scanSatate = 0
    hasClient = False
    currentClient = None
    processing = False


    def __init__(self):
        self.faceDetector = FaceDetector(config=config , ser=ser)
        self.uhdRfidScanner = UhdRfidScanner()
        self.db = ProductDatabase('db.sqlite3')
        self.uhdRfidScanner.test = False #--------TEST
        self.uhdRfidScanner.connect()
        self.uhdRfidScanner.start()
        self.faceDetector.index = 0
        self.faceDetector.method = 1
        self.faceDetector.load_faces()
        self.faceDetector.on()
        self.faceDetector.start()


        self.apiBot = ApiBot()
        self.apiBot.test = False  #--------TEST
        self.apiBot.get_access_token()
        self.screen = QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        ui = Ui_MainWindow()
        ui.setupUi(self.MainWindow)
        ui.widget = ScreenWidget(cameraDetector = self.faceDetector,update_video = self.update_video , keyPressEvent = self.keyPressEvent)

    def start(self):
        MainWindow.show()
        sys.exit(self.screen.exec_())
    
    def purchase_products_by_user(self):
        products_data = []
        for key in  self.current_session_products.keys():
            products_data.append({
                'qty': 1,
                'id': key,
            })
        res = self.apiBot.purchase_by_user(user = self.currentClient,products=products_data)
        print("res",res)


    def getIdsFromUhfProducts(self,uhf_ids: dict):
        return [i for i in uhf_ids.keys()]
    
    def update_video(self):
        detected, frame = self.faceDetector.getCurrentFace()
        if frame is None:
            return False, None
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
            uhf_product_ids = self.uhdRfidScanner.getCurrentData()
            print("Current UHF", uhf_product_ids)

            if len(uhf_product_ids.keys() ) > 0:
                products = self.db.select_all_by_ids(uhf_ids = uhf_product_ids.keys())
                print("Current Products", uhf_product_ids,products)
                to_update_list = False
                for product in products:
                    if not product.id in self.current_session_products.keys():
                        self.current_session_products[product.id] = product
                        to_update_list = True
                if to_update_list:
                    self.screenWidget.updateProductsList(self.current_session_products)
            elif len(self.current_session_products.keys()) > 0:
                self.current_session_products.clear()
                self.screenWidget.updateProductsList()
        return True, frame
        
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
    
    def keyPressEvent(self,event):
        print(event.key())
        if event.key() == 16777248:
            res = self.purchase_products_by_user()
            self.current_session_products = {}
            self.screenWidget.update()

    def __del__(self):
        self.faceDetector.off()

if __name__ == '__main__':
    app = App()
    app.start()