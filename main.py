import cv2,time,sys

import config
from src.camera import *
from src.uhfRfidScanner import UhdRfidScanner
from src.models import Product
from src.apiBot import ApiBot
from src.screen import *
from src.sql_db import ProductDatabase, UserDatabase

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
    scanMethod = 0


    def __init__(self):
        self.faceDetector = FaceDetector(config=config , ser=ser)
        self.uhdRfidScanner = UhdRfidScanner()
        self.db = ProductDatabase('db.sqlite3')
        self.user_db = UserDatabase('db.sqlite3')
        self.uhdRfidScanner.test = False
        self.uhdRfidScanner.connect()
        self.uhdRfidScanner.start()
        


        self.apiBot = ApiBot()
        self.apiBot.test = False  #--------TEST
        self.apiBot.get_access_token()
        self.screen = QApplication(sys.argv)
        self.MainWindow = QtWidgets.QMainWindow()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self.MainWindow)
        self.screenWidget = self.ui.widget = ScreenWidget(self.ui, self.ui.frame_2, keyPressEvent = self.keyPressEvent)

        self.screenWidget.setGeometry(QtCore.QRect(0, 60, 1240, 960))
        self.screenWidget.app_update = self.update

    def start(self):
        self.MainWindow.show()
        sys.exit(self.screen.exec_())
    
    def purchase_products_by_user(self):
        products_data = []
        for key in  self.current_session_products.keys():
            products_data.append({
                'qty': 1,
                'id': key,
            })
        print("request with",self.currentClient.id,products_data)
        if self.currentClient and len(products_data) > 0:
            self.ui.username_label.setText("Processing...")
            res = self.apiBot.purchase_by_user(user = self.currentClient.id ,products=products_data)
            print("res",res)
            if res:
                self.ui.username_label.setText("SUCCESS")
                # self.ui.username_label.setText("SUCESS")
    

    def update(self):
        if self.scanMethod == 0:
            return self.scanMethod, self.update_video()
        elif self.scanMethod == 1:
            return self.scanMethod, self.update_uhf_user()
        else:
            raise Exception(f"Undefined scanMethod {self.scanMethod}")
        
    def update_uhf_user(self):
        uhf_product_ids = self.uhdRfidScanner.getCurrentData()
        if len(uhf_product_ids.keys() > 0):
            uhf_id, user = self.user_db.find_user_in_ids([i for i in uhf_product_ids.keys()])
            if user is not None:
                del uhf_product_ids[uhf_id]
                self.hasClient = True
                self.currentClient = user
                self.scanSatate = 0
            elif self.scanSatate > 4:
                self.hasClient = False
                self.scanSatate = 0
            else:
                self.scanSatate += 1
            if self.hasClient:
                if len(uhf_product_ids.keys() ) > 0:
                    products = self.db.select_all_by_ids(uhf_ids = [i for i in uhf_product_ids.keys()])
                    to_update_list = False
                    for product in products:
                        if not product.id in self.current_session_products.keys():
                            self.current_session_products[product.id] = product
                            to_update_list = True
                            print("Update list needed")

                    if to_update_list: 
                        self.screenWidget.updateProductsList(self.current_session_products)
            else:
                self.current_session_products.clear()
                self.screenWidget.updateProductsList()
                self.ui.username_label.setText("")
        return True, None


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
            #print("Current UHF", uhf_product_ids)

            if len(uhf_product_ids.keys() ) > 0:
                products = self.db.select_all_by_ids(uhf_ids = [i for i in uhf_product_ids.keys()])
                #print("Current Products", products)
                to_update_list = False
                for product in products:
                    if not product.id in self.current_session_products.keys():
                        self.current_session_products[product.id] = product
                        to_update_list = True
                        print("Update list needed")

                if to_update_list: 
                    self.screenWidget.updateProductsList(self.current_session_products)
            elif len(self.current_session_products.keys()) > 0:
                pass
                #self.current_session_products.clear()
                #self.screenWidget.updateProductsList()
        else:
            self.current_session_products.clear()
            self.screenWidget.updateProductsList()
            self.ui.username_label.setText("")
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
        print("pres",event.key(),Qt.Key_Space)
        if event.key() == 16777248:
            res = self.purchase_products_by_user()
            self.current_session_products = {}
            self.screenWidget.update()

    def __del__(self):
        self.faceDetector.off()

if __name__ == '__main__':
    app = App()
    app.scanMethod = 1
    app.faceDetector.index = 0
    app.faceDetector.method = 1
    if app.scanMethod == 0:
        app.faceDetector.load_faces()
        app.faceDetector.on()
        app.faceDetector.start()
    app.start()