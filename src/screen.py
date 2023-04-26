import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
import urllib.request, requests
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QComboBox, QWidget, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QMessageBox, QPushButton,QVBoxLayout, QSizePolicy
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import Qt, QByteArray, QUrl, QSize
from src.models import Product


class ListWidgetItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

class ScreenWidget(QWidget):
    def __init__(self, ui ,frame, keyPressEvent = None):
        super().__init__(frame)

        self.ui = ui
        self.keyPressEvent = keyPressEvent
        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_image_loaded)

        self.list_widget = QListWidget()
        self.list_widget.setFixedWidth(500)
        self.list_widget.setSpacing(10)

        self.list_layout = QHBoxLayout()
        self.list_layout.addWidget(self.list_widget)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        # self.video_label.setMinimumSize(640, 480)
        # self.video_label.setMaximumSize(640*3, 480*3)

        self.video_label.setFixedSize(640 *2, 480*2)
        self.video_layout = QHBoxLayout()
        self.video_layout.addWidget(self.video_label)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.list_layout)
        self.main_layout.addLayout(self.video_layout)

        self.setLayout(self.main_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

    def update_frame(self):
        method, ret, frame = self.app_update()
        if method == 0:
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, c = frame.shape
                q_img = QPixmap.fromImage(QImage(frame.data, w, h, c*w, QImage.Format_RGB888))
                self.video_label.setPixmap(q_img)
        elif method == 1:
            pass
    def app_update(self):
        pass
    
    def show_frame(self,frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = frame.shape
        q_img = QPixmap.fromImage(QImage(frame.data, w, h, c*w, QImage.Format_RGB888))
        self.video_label.setPixmap(q_img)

    def updateProductsList(self,productsDict: dict = {}):
        self.list_widget.clear()
        for product in productsDict.values():
            self.add_item(product=product)

    def add_item(self, product: Product = None):
        if not product:
            product = Product(id=0, name='Unknown',price=132,image_url='https://thumbs.dreamstime.com/b/meat-vector-illustration-white-background-30463413.jpg')

        widget = QWidget()
        layout = QHBoxLayout()

        if product.image_url:
            image_label = QLabel()
            image = QImage(product.image_url)
            image.loadFromData(requests.get(product.image_url).content)

            pixmap = QPixmap(image)
            scaled_pixmap = pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
            image_label.setAlignment(Qt.AlignCenter)

            # image_label = QLabel()
            # pixmap = QPixmap(product.image_url)
            # image_label.setPixmap(pixmap)
            layout.addWidget(image_label)

        name_label = QLabel(product.name)
        layout.addWidget(name_label)

        total_price = product.price * product.quantity
        total_price_label = QLabel(str(total_price))
        layout.addWidget(total_price_label)

        self.ui.total_price_label.setText(str( int(self.ui.total_price_label.text()) + total_price ))

        count_label = QLabel(str(product.quantity))
        layout.addWidget(count_label)

        increment_button = QPushButton('+')
        increment_button.setFixedWidth(40)
        increment_button.clicked.connect(lambda _, count_label=count_label, total_price_label = total_price_label, 
            product = product: self.increment_count(count_label, total_price_label,product))
        layout.addWidget(increment_button)

        decrement_button = QPushButton('-')
        decrement_button.setFixedWidth(40)
        decrement_button.clicked.connect(lambda _, count_label=count_label, total_price_label = total_price_label,
            product = product: self.decrement_count(count_label, total_price_label, product))
        layout.addWidget(decrement_button)

        widget.setLayout(layout)

        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

        # if product.image_url:
        #     request = QNetworkRequest(QUrl(product.image_url))
        #     request.setAttribute(QNetworkRequest.User, image_label)
        #     self.network_manager.get(request)
    
    def remove_item(self, product: Product):
        item = ListWidgetItem(product.name)
        self.list_widget.addItem(item)

    def increment_count(self, count_label, total_price_label, product):
        count = int(count_label.text())
        count += 1
        total_price = product.price * count
        count_label.setText(str(count))
        total_price_label.setText(str(total_price))
        self.ui.total_price_label.setText(str( int(self.ui.total_price_label.text()) + product.price))


    def decrement_count(self, count_label, total_price_label, product):
        count = int(count_label.text())
        count -= 1
        if count < 1:
            return
        total_price = product.price * count
        count_label.setText(str(count))
        total_price_label.setText(str(total_price))
        self.ui.total_price_label.setText(str( int(self.ui.total_price_label.text()) - product.price))

    def keyPressEvent(self, event):
        pass

    def handle_image_loaded(self, reply):
        image_label = reply.request().attribute(QNetworkRequest.User)
        if not image_label:
            return
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(data))
        scaled_pixmap = pixmap.scaled(QSize(100, 100), Qt.KeepAspectRatio, Qt.SmoothTransformation)
        image_label.setPixmap(scaled_pixmap)
        image_label.setAlignment(Qt.AlignCenter)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1800, 900)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.frame = QtWidgets.QFrame(self.frame_2)
        self.frame.setGeometry(QtCore.QRect(0, 10, 830, 40))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(0, 0, 80, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";")
        self.label.setObjectName("label")
        self.username_label = QtWidgets.QLabel(self.frame)
        self.username_label.setGeometry(QtCore.QRect(80, 0, 300, 40))
        self.username_label.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.username_label.setObjectName("username_label")
        self.username_label.setText("")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(450, 0, 80, 40))
        self.label_3.setStyleSheet("font: 20pt \"MS Shell Dlg 2\";")
        self.label_3.setObjectName("label_3")
        self.total_price_label = QtWidgets.QLabel(self.frame)
        self.total_price_label.setGeometry(QtCore.QRect(530, 0, 100, 40))
        self.total_price_label.setStyleSheet("font: 16pt \"MS Shell Dlg 2\";")
        self.total_price_label.setObjectName("total_price_label")
        self.total_price_label.setText('0')

        self.dropdown = QComboBox(self.frame)
        self.dropdown.setGeometry(QtCore.QRect(530, 0, 500, 40))
        self.dropdown.setStyleSheet("font: 12pt \"MS Shell Dlg 2\";")
        self.dropdown.setObjectName("scan_method_dropdown")
        self.dropdown.addItem('Face Recognition')
        self.dropdown.addItem('UHF scan')
        self.dropdown.activated.connect(self.onActivated)
        
        #self.widget = QtWidgets.QWidget(self.frame_2)
        self.widget = None#ScreenWidget(self, self.frame_2)

        #self.widget.setGeometry(QtCore.QRect(0, 60, 961, 501))
        #self.widget.setObjectName("widget")
        self.verticalLayout.addWidget(self.frame_2)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setEnabled(True)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 981, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "User:"))
        self.label_3.setText(_translate("MainWindow", "Total"))
    def onActivated(self):
        pass


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
