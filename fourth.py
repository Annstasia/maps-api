from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
import requests
import sys


def new_request(x, y, delta_x, delta_y, l, pt=''):
    try:
        map_request = "http://static-maps.yandex.ru/1.x/"
        params = {
            'll': '{},{}'.format(x, y),
            'spn': '{},{}'.format(delta_x, delta_y),
            'l': l
        }
        if pt:
            params['pt'] = pt + ',pm2rdl'
        response = requests.get(map_request, params=params)
        if l == 'map':
            map_file = "map.png"
            with open(map_file, "wb") as file:
                file.write(response.content)
        elif l == 'sat':
            map_file = "sat.jpg"
            with open(map_file, "wb") as file:
                file.write(response.content)
        else:
            map_file = "sat_skl.jpg"
            with open(map_file, "wb") as file:
                file.write(response.content)
        return map_file
    except Exception as e:
        print(e)
        sys.exit(1)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(900, 600)
        MainWindow.setStyleSheet("background-color: white;")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 600, 450))
        self.label_2.setStyleSheet("background-color: rgb(255, 250, 238)")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 0, 141, 41))
        self.pushButton.setStyleSheet("background-color: rgb(255, 241, 212);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(750, 50, 141, 41))
        self.pushButton_2.setStyleSheet("background-color: rgb(152, 217, 182);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(750, 100, 141, 41))
        self.pushButton_3.setStyleSheet("background-color: rgb(212, 245, 255);")
        self.pushButton_3.setObjectName("pushButton_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 900, 18))
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
        self.pushButton.setText(_translate("MainWindow", "Схема"))
        self.pushButton_2.setText(_translate("MainWindow", "Спутник"))
        self.pushButton_3.setText(_translate("MainWindow", "Гибрид"))


class Map_window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        try:
            super().__init__()
            self.setupUi(self)
            self.x = 37.618865
            self.y = 55.769600
            self.delta_x = 0.0008
            self.delta_y = 0.0008 * 450 / 600
            self.layer = 'sat'
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))
            self.pushButton.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pushButton_2.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pushButton_3.setFocusPolicy(QtCore.Qt.NoFocus)
            self.pushButton.clicked.connect(self.layer_map)
            self.pushButton_2.clicked.connect(self.layer_sat)
            self.pushButton_3.clicked.connect(self.layer_sat_skl)
            self.show()
        except Exception as e:
            print(e)

    def layer_map(self):
        if self.pushButton.sender():
            self.layer = 'map'
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))

    def layer_sat(self):
        if self.pushButton_2.sender():
            try:
                self.layer = 'sat'
                self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
                self.label_2.setPixmap(QPixmap(self.map))
            except Exception as e:
                print(e)

    def layer_sat_skl(self):
        if self.pushButton_3.sender():
            self.layer = 'sat,skl'
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))

    def keyPressEvent(self, e):
        if e.key() == 16777238 and self.delta_x > 0.0009:
                self.delta_x /= 2
                self.delta_y /= 2
                self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
                self.label_2.setPixmap(QPixmap(self.map))
        elif e.key() == 16777239 and -180 < self.x - 2 * self.delta_x \
                < self.x + 2 * self.delta_x < 180 \
                    and -90 < self.y - 2 * self.delta_y < self.y + 2 * self.delta_y < 90:
            self.delta_x *= 2
            self.delta_y *= 2
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))
        elif e.key() == Qt.Key_Up and self.y + 2 * self.delta_y < 90:
            self.y += 2 * self.delta_y
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))
        elif e.key() == Qt.Key_Down and self.y - 2 * self.delta_y > -90:
            self.y -= 2 * self.delta_y
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))
        elif e.key() == Qt.Key_Right:
            self.x += 2 * self.delta_x
            if self.x > 180:
                self.x = 360 - self.x
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))
        elif e.key() == Qt.Key_Left:
            self.x -= 2 * self.delta_x
            if self.x < -180:
                self.x = 360 + self.x
            self.map = new_request(self.x, self.y, self.delta_x, self.delta_y, self.layer)
            self.label_2.setPixmap(QPixmap(self.map))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Map_window()
    ex.show()
    sys.exit(app.exec_())