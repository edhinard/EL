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

        self.visible_top = 100
        self.visible_bottom = -100
        self.visible_left = -100
        self.visible_right = 100

    def startPainting(self):
        self.qp = QtGui.QPainter()
        self.qp.begin(self)

        assert(self.visible_top>self.visible_bottom and self.visible_left<self.visible_right)
        width = self.visible_right-self.visible_left
        height = self.visible_top-self.visible_bottom
        scale = min(self.width()/width, self.height()/height)
        self.transf = QtGui.QTransform()
        self.transf.scale(scale,-scale)
        self.transf.translate(self.width()/2/scale, -self.height()/2/scale)
        
    def stopPainting(self):
        self.qp.end()

    def paintNode(self, x, y):
        pen = QtGui.QPen()
        pen.setWidthF(1.5)
        pen.setColor(QtGui.QColor(128, 64, 32, 100))
        self.qp.setBrush(QtGui.QColor(128, 64, 32, 100))
        self.qp.setPen(pen)

        x,y = self.transf.map(x,y)
        self.qp.drawEllipse(QtCore.QPointF(x,y), 10, 10)
#        path = QtGui.QPainterPath()
#        path.addEllipse(QtCore.QPointF(x,y), 10, 10)
#        self.qp.drawPath(self.transf.map(path))

    def paintVertex(self, x1, y1, x2, y2):
        pen = QtGui.QPen()
        pen.setWidthF(3)
        pen.setColor(QtGui.QColor(64, 64, 64, 100))
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setStyle(QtCore.Qt.DashDotDotLine)
        self.qp.setPen(pen)

        x1,y1 = self.transf.map(x1,y1)
        x2,y2 = self.transf.map(x2,y2)
        self.qp.drawLine(x1, y1, x2, y2)

    def paintEvent(self, event):
        self.startPainting()
        #self.drawText(event, "Bébé à bord.")
        self.paintNode(0,0)
        self.paintNode(20,70)
        self.paintNode(70,0)
        self.paintVertex(0,0, 20, 70)
        self.paintVertex(20, 70, 70, 0)
        self.stopPainting()
        
#    def drawText(self, event, text):     
#        self.qp.setPen(QtGui.QColor(168, 34, 3))
#        self.qp.setFont(QtGui.QFont('Decorative', 10))
#        self.qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text)
                
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

