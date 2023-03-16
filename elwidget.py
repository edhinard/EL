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
        self.scale = min(self.width()/width, self.height()/height)
        self.transf = QtGui.QTransform()
        self.transf.scale(self.scale,-self.scale)
        self.transf.translate(self.width()/2/self.scale - (left+right)/2,
                              -self.height()/2/self.scale - (top+bottom)/2)
        
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
        
    def paintEvent(self, event):
        if not self.el:
            return
        self.startPainting()

        for node in self.el.nodes:
            self.paintNode(node)
        for vertex in self.el.vertices:
            self.paintVertex(vertex)

        for path in self.el.paths:
            color = QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
            for m1,c1,c2,m2 in path[3::4]:
                self.paintArc(m1,c1,c2,m2,(1+self.el.params['pathwidth'])*self.scale,QtCore.Qt.blue)
                self.paintArc(m1,c1,c2,m2,(0+self.el.params['pathwidth'])*self.scale,color)

            for m1,c1,c2,m2 in path[::4]:
                self.paintArc(m1,c1,c2,m2,(1+self.el.params['pathwidth'])*self.scale,QtCore.Qt.red)
                self.paintArc(m1,c1,c2,m2,(0+self.el.params['pathwidth'])*self.scale,color)

            for m1,c1,c2,m2 in path[1::4]:
                self.paintArc(m1,c1,c2,m2,(1+self.el.params['pathwidth'])*self.scale,QtCore.Qt.yellow)

            for m1,c1,c2,m2 in path[2::4]:
                self.paintArc(m1,c1,c2,m2,(1+self.el.params['pathwidth'])*self.scale,QtCore.Qt.black)


            for m1,c1,c2,m2 in path[1::4]:
                self.paintArc(m1,c1,c2,m2,(0+self.el.params['pathwidth'])*self.scale,color)

            for m1,c1,c2,m2 in path[2::4]:
                self.paintArc(m1,c1,c2,m2,(0+self.el.params['pathwidth'])*self.scale,color)

                
#        for path in self.el.paths:
#            for m1,c1,c2,m2 in path:
#                color = QtGui.QColor(random.randint(0,255), random.randint(0,255), random.randint(0,255))
#                self.paintArc(m1,c1,c2,m2,20,QtCore.Qt.white)
#                self.paintArc(*self.offset(m1,c1,c2,m2,10),3,color)
#                self.paintArc(*self.offset(m1,c1,c2,m2,-10),3,color)


        self.stopPainting()

    def offset(self, P0, P1, P2, P3, e):
        s0 = P1 - P0
        s3 = P3 - P2

        # P = a.t^3 + b.t^2 + c.t + P0
        a =  3*s0 + 3*s3 - 2*(P3-P0)
        b = -6*s0 - 3*s3 + 3*(P3-P0)
        c =  3*s0
        Pc = a/8 + b/4 + c/2 + P0
        dP = 3/4*a + b + c

        n0 = s0.rotatepi2().unit()
        n3 = s3.rotatepi2().unit()
        nc = dP.rotatepi2().unit()
        Q0 = P0 + e*n0
        Q3 = P3 + e*n3
        Rc = Pc + e*nc

        # Q = A.t^3 + B.t^2 + C.t + Q0
        A =  3*s0 + 3*s3 - 2*(Q3-Q0)
        B = -6*s0 - 3*s3 + 3*(Q3-Q0)
        C =  3*s0
        Qc = A/8 + B/4 + C/2 + Q0
        dQ = 3/4*A + B + C


        a11 = s0.x;                  a12 = -s3.x;                  a13 = 8/3*dP.x
        a21 = s0.y;                  a22 = -s3.y;                  a23 = 8/3*dP.y
        a31 = s0.x*nc.x + s0.y*nc.y; a32 =  s3.x*nc.x + s3.y*nc.y; a33 = 4*((s0.x-s3.x)*nc.x + (s0.y-s3.y)*nc.y)
        y1 = 8/3*(Rc.x - Qc.x)
        y2 = 8/3*(Rc.y - Qc.y)
        y3 = 4/3*(dQ.x*nc.x + dQ.y*nc.y)

        A11 =  a22*a33 - a23*a32
        A21 = -a12*a33 + a13*a32
        A31 =  a12*a23 - a13*a22
        A12 = -a21*a33 + a23*a31
        A22 =  a11*a33 - a13*a31
        A32 = -a11*a23 + a13*a21
        A13 =  a21*a32 - a22*a31
        A23 = -a11*a32 + a12*a31
        A33 =  a11*a22 - a12*a21

        
        De0 = a11*A11 + a21*A21 + a31*A31
        De1 =  y1*A11 +  y2*A21 +  y3*A31
        De2 =  y1*A12 +  y2*A22 +  y3*A32
        De3 =  y1*A13 +  y2*A23 +  y3*A33
        if abs(De0) > 1:
            flag = 3
        else:
            flag = 0
            if abs(De1) < 0.9*abs(De0):
                flag == 1
            if abs(De2) < 0.9*abs(De0):
                flag == 1
            if abs(De3) < 0.45*abs(De0):
                flag == 1
        if flag == 3:
            dk0 = De1/De0
            dk3 = De2/De0
            dt  = De3/De0
        else:
            a13 = 0; a23=0; a31=0; a32=0; a33=1; y3=0
            De0 = a11*a22 - a12*a21
            De1 =  y1*a22 -  y2*a12
            De2 = a11*y2  -  y1*a21
            De3 = 0
            if abs(De0) > 1:
                flag = 2
            else:
                flag = 0
                if abs(De1) < 0.9*abs(De0):
                    flag += 1
                if abs(De2) < 0.9*abs(De0):
                    flag += 1
            if flag == 2:
                dk0 = De1/De0
                dk3 = De2/De0
                dt  = 0
            else:
                dk0 = 0
                dk3 = 0
                dt = 0

        k0 = 1+dk0
        k3 = 1+dk3
        t  = 0.5+dt

        R0 = Q0
        R1 = Q0 + k0*s0
        R2 = Q3 - k3*s3
        R3 = Q3
        
        return R0,R1,R2,R3

        
        
#    def drawText(self, event, text):     
#        self.qp.setPen(QtGui.QColor(168, 34, 3))
#        self.qp.setFont(QtGui.QFont('Decorative', 10))
#        self.qp.drawText(event.rect(), QtCore.Qt.AlignCenter, text)
