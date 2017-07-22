#! /usr/bin/env python3
# coding: utf-8

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
#designer -qt=4 mainel.ui
#pyuic5 mainel.ui -x -o mainel_gui.py
from mainel_gui import Ui_MainWindow

import el

class QMyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.visible_top = 200
        self.visible_bottom = -5
        self.visible_left = -100
        self.visible_right = 160

    def startPainting(self):
        self.qp = QtGui.QPainter()
        self.qp.begin(self)

        assert(self.visible_top>self.visible_bottom and self.visible_left<self.visible_right)
        width = self.visible_right-self.visible_left
        height = self.visible_top-self.visible_bottom
        scale = min(self.width()/width, self.height()/height)
        self.transf = QtGui.QTransform()
        self.transf.scale(scale,-scale)
        self.transf.translate(self.width()/2/scale - (self.visible_left+self.visible_right)/2,
                              -self.height()/2/scale - (self.visible_top+self.visible_bottom)/2)
        
    def stopPainting(self):
        self.qp.end()

    def paintNode(self, node):
        pen = QtGui.QPen()
        pen.setWidthF(1.5)
        pen.setColor(QtGui.QColor(128, 64, 32, 100))
        self.qp.setBrush(QtGui.QColor(128, 64, 32, 100))
        self.qp.setPen(pen)

        x,y = self.transf.map(node.x, node.y)
        self.qp.drawEllipse(QtCore.QPointF(x,y), 10, 10)
#        path = QtGui.QPainterPath()
#        path.addEllipse(QtCore.QPointF(x,y), 10, 10)
#        self.qp.drawPath(self.transf.map(path))

    def paintVertex(self, vertex):
        pen = QtGui.QPen()
        pen.setWidthF(3)
        pen.setColor(QtGui.QColor(64, 64, 64, 100))
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setStyle(QtCore.Qt.DashDotDotLine)
        self.qp.setPen(pen)

        x1,y1 = self.transf.map(vertex.node1.x, vertex.node1.y)
        x2,y2 = self.transf.map(vertex.node2.x, vertex.node2.y)
        self.qp.drawLine(x1, y1, x2, y2)


    def paintEvent(self, event):
        global myel

        self.startPainting()

        for node in myel.nodes:
            self.paintNode(node)
        for vertex in myel.vertices:
            self.paintVertex(vertex)
        self.stopPainting()
        
#    def drawText(self, event, text):     
#        self.qp.setPen(QtGui.QColor(168, 34, 3))
#        self.qp.setFont(QtGui.QFont('Decorative', 10))
#        self.qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text)
                
nodes = [
    (-50,0),
    (50,0),
    (0,86),
    (0,186)
]
vertices = [
    (0,1),
    (1,2),
    (2,0),
    (2,3)
]    
nodes = [el.Node(*node) for node in nodes]
vertices = [el.Vertex(nodes[n1], nodes[n2]) for n1,n2 in vertices]
myel = el.EL(nodes, vertices)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
