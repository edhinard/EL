#! /usr/bin/env python3
# coding: utf-8

from PyQt5 import QtCore, QtGui, QtWidgets
import random

class QMyWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.el = None

    def setel(self, el):
        self.el = el

    def startPainting(self):
        self.qp = QtGui.QPainter()
        self.qp.begin(self)
        self.qp.setRenderHint(QtGui.QPainter.Antialiasing)

        left, right, top, bottom = self.el.bounds
        
        width = right-left
        height = top-bottom
        scale = min(self.width()/width, self.height()/height)
        self.transf = QtGui.QTransform()
        self.transf.scale(scale,-scale)
        self.transf.translate(self.width()/2/scale - (left+right)/2,
                              -self.height()/2/scale - (top+bottom)/2)
        
    def stopPainting(self):
        self.qp.end()

    def paintNode(self, node):
        pen = QtGui.QPen()
        pen.setWidthF(1.5)
        pen.setColor(QtGui.QColor(128, 64, 32, 100))
        self.qp.setBrush(QtGui.QColor(128, 64, 32, 100))
        self.qp.setPen(pen)

        x,y = self.transf.map(node.pos.x, node.pos.y)
        self.qp.drawEllipse(QtCore.QPointF(x,y), 10, 10)

    def paintVertex(self, vertex):
        pen = QtGui.QPen()
        pen.setWidthF(3)
        pen.setColor(QtGui.QColor(64, 64, 64, 100))
        pen.setCapStyle(QtCore.Qt.RoundCap)
        pen.setStyle(QtCore.Qt.DashDotDotLine)
        self.qp.setPen(pen)

        x1,y1 = self.transf.map(vertex.node1.pos.x, vertex.node1.pos.y)
        x2,y2 = self.transf.map(vertex.node2.pos.x, vertex.node2.pos.y)
        self.qp.drawLine(x1, y1, x2, y2)

    def paintArc(self, m1,c1,c2,m2, width, color):
        pen = QtGui.QPen()
        pen.setWidthF(width)
        pen.setColor(color)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        self.qp.setPen(pen)
        self.qp.setBrush(QtCore.Qt.NoBrush)

        path = QtGui.QPainterPath(QtCore.QPointF(m1.x,m1.y))
        path.cubicTo(c1.x, c1.y, c2.x, c2.y, m2.x, m2.y)
        self.qp.drawPath(self.transf.map(path))
        
    def paintArc2(self, m1,c1,c2,m2):
        pen = QtGui.QPen()
        pen.setWidthF(1)
        pen.setColor(QtCore.Qt.black)
        pen.setCapStyle(QtCore.Qt.FlatCap)
        self.qp.setPen(pen)
        #self.qp.setBrush(QtCore.Qt.white)
        self.qp.setBrush(QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255)))

        path = QtGui.QPainterPath(QtCore.QPointF(m1.x,m1.y))
        path.cubicTo(c1.x, c1.y, c2.x, c2.y, m2.x, m2.y)

        ps = QtGui.QPainterPathStroker(pen)
        ps.setWidth(self.el.params.get('pathwidth',20))
        path = ps.createStroke(path)

        self.qp.drawPath(self.transf.map(path))
        

    def paintEvent(self, event):
        if not self.el:
            return
        self.startPainting()

        for node in self.el.nodes:
            self.paintNode(node)
        for vertex in self.el.vertices:
            self.paintVertex(vertex)

#        for m1,c1,c2,m2 in self.el.paths:
#            self.paintArc(m1,c1,c2,m2, 19.5, QtCore.Qt.black)
#        for m1,c1,c2,m2 in self.el.paths:
#            self.paintArc(m1,c1,c2,m2, 19, QtCore.Qt.white)
        for m1,c1,c2,m2 in self.el.paths:
            self.paintArc2(m1,c1,c2,m2)
            
        self.stopPainting()
        
#    def drawText(self, event, text):     
#        self.qp.setPen(QtGui.QColor(168, 34, 3))
#        self.qp.setFont(QtGui.QFont('Decorative', 10))
#        self.qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text)
