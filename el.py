#! /usr/bin/env python3
# coding: utf-8

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

#designer -qt=4 el.ui
#pyuic5 el.ui -x -o el_gui.py
from el_gui import Ui_MainWindow



class QMyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        
    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        self.drawText(event, qp)
        qp.end()
        
        
    def drawText(self, event, qp):
      
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setFont(QtGui.QFont('Decorative', 10))
        qp.drawText(event.rect(), QtCore.Qt.AlignCenter, "bébé")
                



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

