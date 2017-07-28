#!/usr/bin/python3
# coding: utf-8
import os
import sys

#designer -qt=4 main.ui
from PyQt5 import uic
from PyQt5 import QtCore, QtGui, QtWidgets

import elwidget
import el
import json

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        uic.loadUi('main.ui', baseinstance=self)
        self.elwidget = self.findChild(elwidget.QMyWidget, 'elwidget')
        self.label = self.findChild(QtWidgets.QLabel, 'label')

        self.jsonfilenames = [f.path for f in os.scandir('test') if f.name.endswith('.json') and f.is_file()]
        self.current = -1
        self.next()
        
    def previous(self):
        if not self.jsonfilenames:
            return
        self.current = (self.current - 1) % len(self.jsonfilenames)
        self.open()
    def next(self):
        if not self.jsonfilenames:
            return
        self.current = (self.current + 1) % len(self.jsonfilenames)
        self.open()
    def open(self):
        if not self.jsonfilenames:
            return
        fname = self.jsonfilenames[self.current]
        self.label.setText(fname)
        obj = json.load(open(fname))
        self.elwidget.setel(el.EL(**obj))
        self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
