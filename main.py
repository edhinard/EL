#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import sys

#designer -qt=4 main.ui

from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        uic.loadUi('main.ui', baseinstance=self)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
