import sys, urllib.request
from PyQt5.QtWidgets import QApplication, QMainWindow, QListWidget, QListWidgetItem, QHBoxLayout, QLabel, QPushButton, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtNetwork import QNetworkAccessManager, QNetworkRequest
from PyQt5.QtCore import Qt, QByteArray, QUrl

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the list widget
        self.list_widget = QListWidget()

        # Create some sample data for the list
        items = [
            {
                'name': 'Item 1',
                'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg',
                'count': 0
            },
            {
                'name': 'Item 2',
                'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg',
                'count': 0
            },
            {
                'name': 'Item 3',
                'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg',
                'count': 0
            }
        ]

        self.network_manager = QNetworkAccessManager()
        self.network_manager.finished.connect(self.handle_image_loaded)
        # Add the items to the list
        for item_data in items:
            self.add_item(item_data)
            # Load the image from a URL
            # pixmap = QPixmap(item_data['image_url'])
            # imgData = urllib.request.urlopen(item_data['image_url']).read()
            # pixmap.loadFromData(imgData)

            # # Create a new widget for the list item
            # widget = QWidget()
            # layout = QHBoxLayout()

            # # Create a label for the image
            # image_label = QLabel()
            # image_label.setPixmap(pixmap)
            # layout.addWidget(image_label)

            # # Create a label for the text
            # text_label = QLabel(item_data['name'])
            # layout.addWidget(text_label)

            # # Create a label for the count
            # count_label = QLabel(str(item_data['count']))
            # layout.addWidget(count_label)

            # # Create the increment button
            # increment_button = QPushButton('+')
            # increment_button.clicked.connect(lambda _, label=count_label: self.increment_count(label))
            # layout.addWidget(increment_button)

            # # Create the decrement button
            # decrement_button = QPushButton('-')
            # decrement_button.clicked.connect(lambda _, label=count_label: self.decrement_count(label))
            # layout.addWidget(decrement_button)

            # widget.setLayout(layout)

            # # Add the widget to the list
            # item = QListWidgetItem()
            # item.setSizeHint(widget.sizeHint())
            # self.list_widget.addItem(item)
            # self.list_widget.setItemWidget(item, widget)

            #  # Load the image asynchronously
            # request = QNetworkRequest(QUrl(item_data['image_url']))
            # request.setAttribute(QNetworkRequest.User, image_label)
            # self.network_manager.get(request)

        # Set the list widget as the central widget of the window
        self.setCentralWidget(self.list_widget)

    def increment_count(self, label):
        count = int(label.text())
        count += 1
        label.setText(str(count))

    def decrement_count(self, label):
        count = int(label.text())
        count -= 1
        label.setText(str(count))

    def handle_image_loaded(self, reply):
        # Get the image label from the reply
        image_label = reply.request().attribute(QNetworkRequest.User)
        if not image_label:
            return

        # Load the pixmap from the reply data
        data = reply.readAll()
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(data))

        # Set the pixmap in the image label
        image_label.setPixmap(pixmap)
        image_label.setAlignment(Qt.AlignCenter)

    def add_item(self,item_data = {'image_url': 'https://upload.wikimedia.org/wikipedia/en/a/a9/Example.jpg','name':"N",'count':0}):
        pixmap = QPixmap(item_data['image_url'])
        imgData = urllib.request.urlopen(item_data['image_url']).read()
        pixmap.loadFromData(imgData)

        # Create a new widget for the list item
        widget = QWidget()
        layout = QHBoxLayout()

        # Create a label for the image
        image_label = QLabel()
        image_label.setPixmap(pixmap)
        layout.addWidget(image_label)

        # Create a label for the text
        text_label = QLabel(item_data['name'])
        layout.addWidget(text_label)

        # Create a label for the count
        count_label = QLabel(str(item_data['count']))
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
        request = QNetworkRequest(QUrl(item_data['image_url']))
        request.setAttribute(QNetworkRequest.User, image_label)
        self.network_manager.get(request)

    def keyPressEvent(self, event):
        print("J",event.key(),Qt.Key_Enter )
        if event.key() == 16777220:
            self.add_item()

if __name__ == '__main__':
    # Create the application and window
    app = QApplication(sys.argv)
    window = MyWindow()
    window.setWindowTitle('Image List')

    # Show the window and run the application
    window.show()
    sys.exit(app.exec_())
