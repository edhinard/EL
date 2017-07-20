#! /usr/bin/env python3
# coding: utf-8

#designer -qt=4 el.ui
#pyuic5 el.ui -x -o el-gui.py


import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from el_gui import Ui_MainWindow



class QMyFrame(QtWidgets.QFrame):
#    def __init__(self):
#        super().__init__()
#        
#        self.initUI()
#        
#        
#    def initUI(self):      
#
#        self.text = u'\u041b\u0435\u0432 \u041d\u0438\u043a\u043e\u043b\u0430\
#\u0435\u0432\u0438\u0447 \u0422\u043e\u043b\u0441\u0442\u043e\u0439: \n\
#\u0410\u043d\u043d\u0430 \u041a\u0430\u0440\u0435\u043d\u0438\u043d\u0430'
#
#        #self.setGeometry(300, 300, 280, 170)
#        self.resize(250, 150)
#        self.center()
#        self.setWindowTitle('Draw text')
#        self.setWindowIcon(QIcon('web.png')) 
#        self.show()
#        
#    def center(self):
#        
#        qr = self.frameGeometry()
#        cp = QDesktopWidget().availableGeometry().center()
#        qr.moveCenter(cp)
#        self.move(qr.topLeft())
        
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

