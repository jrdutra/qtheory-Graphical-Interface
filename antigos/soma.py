# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'soma.ui'
#
# Created by: PyQt5 UI code generator 5.14.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(160, 130)
   
        self.txt1 = QtWidgets.QLineEdit(Dialog)
        self.txt1.setGeometry(QtCore.QRect(10, 10, 120, 30))
        self.txt1.setObjectName("txt1")

        self.txt2 = QtWidgets.QLineEdit(Dialog)
        self.txt2.setObjectName("txt2")
        self.txt2.setGeometry(QtCore.QRect(10, 45, 120, 30))

        self.btnPlus = QtWidgets.QPushButton(Dialog)
        self.btnPlus.setGeometry(QtCore.QRect(10, 90, 75, 25))
        self.btnPlus.setObjectName("btnPlus")

        self.lblResult = QtWidgets.QLabel(Dialog)
        self.lblResult.setGeometry(QtCore.QRect(90, 80, 61, 41))

        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(True)
        font.setWeight(75)

        self.lblResult.setFont(font)
        self.lblResult.setObjectName("lblResult")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnPlus.setText(_translate("Dialog", "+"))
        self.lblResult.setText(_translate("Dialog", "0"))
