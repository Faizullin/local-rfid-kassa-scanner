import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QMessageBox
from .models import Product


class ListWidgetItem(QListWidgetItem):
    def __init__(self, text):
        super().__init__()
        self.setText(text)

class ScreenWidget(QWidget):
    def __init__(self, cameraDetector = None, update_video = None):
        super().__init__()

        self.list_widget = QListWidget()
        self.list_widget.setSpacing(10)

        for i in range(20):
            self.add_item(Product(i,f'Product {i}',12))
            

        self.list_layout = QHBoxLayout()
        self.list_layout.addWidget(self.list_widget)

        self.video_label = QLabel()
        self.video_label.setAlignment(Qt.AlignCenter)
        self.video_label.setMinimumSize(640, 480)
        self.video_label.setMaximumSize(640, 480)
        self.video_layout = QHBoxLayout()
        self.video_layout.addWidget(self.video_label)

        self.main_layout = QHBoxLayout()
        self.main_layout.addLayout(self.list_layout)
        self.main_layout.addLayout(self.video_layout)

        self.setLayout(self.main_layout)

        self.update_video = update_video
        self.cameraDetector = cameraDetector
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

    def update_frame(self):
        ret, frame = self.cameraDetector.read()
        if ret:
            frame = self.update_video(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, c = frame.shape
            q_img = QPixmap.fromImage(QImage(frame.data, w, h, c*w, QImage.Format_RGB888))
            self.video_label.setPixmap(q_img)
    
    def show_frame(self,frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, c = frame.shape
        q_img = QPixmap.fromImage(QImage(frame.data, w, h, c*w, QImage.Format_RGB888))
        self.video_label.setPixmap(q_img)

    def add_item(self, product: Product):
        item = ListWidgetItem(product.name)
        self.list_widget.addItem(item)
    
    def remove_item(self, product: Product):
        item = ListWidgetItem(product.name)
        self.list_widget.addItem(item)
    
    def edit_item(self, product: Product):
        item = ListWidgetItem(product.name)
        self.list_widget.addItem(item)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_B:
            QMessageBox.information(self, 'B key pressed', 'The B key was pressed!')
