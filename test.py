import sys, urllib.request
from src.sql_db import ProductDatabase
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QWidget

class ImageWidget(QWidget):
    def __init__(self, image_path):
        super().__init__()
        self.label = QLabel(self)
        pixmap = QPixmap(image_path)
        imgData = urllib.request.urlopen(image_path).read()

        pixmap.loadFromData(imgData)
        self.label.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    db = ProductDatabase('db.sqlite3')
    data = db.select_all_by_ids(['1'])
    widgets = []
    for d in data:
        widgetI = ImageWidget(d['image'])
        widgetI.show()
        widgets.append(widgetI)
    sys.exit(app.exec_())