import cv2, urllib.request
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QWidget, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QMessageBox, QPushButton
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import Qt, QByteArray, QUrl
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

    def add_item(self, product: Product = None):
        
        item_data = {'imagel': 'https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg','title':"Unknown",'quantity':0}
        if not product:
            product = item_data
        pixmap = QPixmap(product.imageUrl)
        imgData = urllib.request.urlopen(product.imageUrl).read()
        pixmap.loadFromData(imgData)

        # Create a new widget for the list item
        widget = QWidget()
        layout = QHBoxLayout()

        # Create a label for the image
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # Create a label for the text
        text_label = QLabel(product.name)
        layout.addWidget(text_label)

        # Create a label for the count
        count_label = QLabel(str(product.quantity))
        layout.addWidget(count_label)

        # Create the increment button
        increment_button = QPushButton('+')
        increment_button.clicked.connect(lambda _, label=count_label: self.increment_count(label))
        layout.addWidget(increment_button)

        # Create the decrement button
        decrement_button = QPushButton('-')
        decrement_button.clicked.connect(lambda _, label=count_label: self.decrement_count(label))
        layout.addWidget(decrement_button)

        widget.setLayout(layout)

        # Add the widget to the list
        item = QListWidgetItem()
        item.setSizeHint(widget.sizeHint())
        self.list_widget.addItem(item)
        self.list_widget.setItemWidget(item, widget)

            # Load the image asynchronously
        request = QNetworkRequest(QUrl(product.imageUrl))
        request.setAttribute(QNetworkRequest.User, image_label)
        self.network_manager.get(request)
    
    def remove_item(self, product: Product):
        item = ListWidgetItem(product.name)
        self.list_widget.addItem(item)
    
    def edit_item(self, product: Product):
        item = ListWidgetItem(product.name)
        self.list_widget.addItem(item)

    def increment_count(self, label):
        count = int(label.text())
        count += 1
        label.setText(str(count))

    def decrement_count(self, label):
        count = int(label.text())
        count -= 1
        label.setText(str(count))
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_B:
            QMessageBox.information(self, 'B key pressed', 'The B key was pressed!')
