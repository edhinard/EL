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

        self.pathwidth = self.findChild(QtWidgets.QSpinBox, 'pathwidth')
        self.alpha = self.findChild(QtWidgets.QSpinBox, 'alpha')
        self.plusgap = self.findChild(QtWidgets.QSpinBox, 'plusgap')
        self.equalgap = self.findChild(QtWidgets.QSpinBox, 'equalgap')
        self.peak = self.findChild(QtWidgets.QSpinBox, 'peak')

        self.jsonfilenames = [f.path for f in os.scandir('test') if f.name.endswith('.json') and f.is_file()]
        self.current = -1
        self.next()

    @QtCore.pyqtSlot(int, name='on_alpha_valueChanged')
    def updatealpha(self, alpha):
        self.el.params['alpha'] = alpha
        self.el.reset()
        self.elwidget.update()
    @QtCore.pyqtSlot(int, name='on_pathwidth_valueChanged')
    def updatepathwidth(self, pathwidth):
        self.el.params['pathwidth'] = pathwidth
        self.el.reset()
        self.elwidget.update()
    @QtCore.pyqtSlot(int, name='on_plusgap_valueChanged')
    def updateplusgap(self, plusgap):
        self.el.params['plusgap'] = plusgap
        self.el.reset()
        self.elwidget.update()
    @QtCore.pyqtSlot(int, name='on_equalgap_valueChanged')
    def updateequalgap(self, equalgap):
        self.el.params['equalgap'] = equalgap
        self.el.reset()
        self.elwidget.update()
    @QtCore.pyqtSlot(int, name='on_peak_valueChanged')
    def updatepeak(self, peak):
        self.el.params['peak'] = peak
        self.el.reset()
        self.elwidget.update()
        
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
        self.el = el.EL(**obj)
        self.pathwidth.setValue(self.el.params['pathwidth'])
        self.alpha.setValue(self.el.params['alpha'])
        self.plusgap.setValue(self.el.params['plusgap'])
        self.equalgap.setValue(self.el.params['equalgap'])
        self.peak.setValue(self.el.params['peak'])
        self.elwidget.setel(self.el)
        self.update()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
