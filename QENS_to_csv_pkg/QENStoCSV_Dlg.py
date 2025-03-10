#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/OrdenDlg.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.
"""
Filename: QENStoCSV_Dlg.py
Author: Beatriz Robles Hernández
Date: 2025-03-10
Version: 1.0
Description: 
    This script creates the class of the GUI that uses 
    the app_QENStoCSV_Dlg application.

License: GLP
Contact: broblesher@gmail.com
Dependencies: os, PyQt5
"""
# Import statements
import os
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_QENStoCSV(object):
    def setupUi(self, Dialog_QENStoCSV):
        Dialog_QENStoCSV.setObjectName("Dialog_QENStoCSV")
        Dialog_QENStoCSV.resize(437, 447)
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(Dialog_QENStoCSV)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout()
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.label_input = QtWidgets.QLabel(Dialog_QENStoCSV)
        self.label_input.setObjectName("label_input")
        self.verticalLayout_3.addWidget(self.label_input)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.lineEdit_iFile = QtWidgets.QLineEdit(Dialog_QENStoCSV)
        self.lineEdit_iFile.setObjectName("lineEdit_iFile")
        self.horizontalLayout.addWidget(self.lineEdit_iFile)
        self.pushButton_iFile = QtWidgets.QPushButton(Dialog_QENStoCSV)
        self.pushButton_iFile.setObjectName("pushButton_iFile")
        self.horizontalLayout.addWidget(self.pushButton_iFile)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.verticalLayout_5.addLayout(self.verticalLayout_3)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_intrument = QtWidgets.QLabel(Dialog_QENStoCSV)
        self.label_intrument.setObjectName("label_intrument")
        self.verticalLayout_2.addWidget(self.label_intrument)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.radioButton_IN5 = QtWidgets.QRadioButton(Dialog_QENStoCSV)
        self.radioButton_IN5.setChecked(False)
        self.radioButton_IN5.setObjectName("radioButton_IN5")
        self.horizontalLayout_4.addWidget(self.radioButton_IN5)
        self.radioButton_IN16B = QtWidgets.QRadioButton(Dialog_QENStoCSV)
        self.radioButton_IN16B.setChecked(False)
        self.radioButton_IN16B.setObjectName("radioButton_IN16B")
        self.horizontalLayout_4.addWidget(self.radioButton_IN16B)
        self.radioButton_FOCUS = QtWidgets.QRadioButton(Dialog_QENStoCSV)
        self.radioButton_FOCUS.setChecked(False)
        self.radioButton_FOCUS.setObjectName("radioButton_FOCUS")
        self.horizontalLayout_4.addWidget(self.radioButton_FOCUS)
        self.radioButton_LET = QtWidgets.QRadioButton(Dialog_QENStoCSV)
        self.radioButton_LET.setChecked(False)
        self.radioButton_LET.setObjectName("radioButton_LET")
        self.horizontalLayout_4.addWidget(self.radioButton_LET)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.verticalLayout_5.addLayout(self.verticalLayout_2)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_output = QtWidgets.QLabel(Dialog_QENStoCSV)
        self.label_output.setObjectName("label_output")
        self.verticalLayout.addWidget(self.label_output)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.lineEdit_oFile = QtWidgets.QLineEdit(Dialog_QENStoCSV)
        self.lineEdit_oFile.setObjectName("lineEdit_oFile")
        self.horizontalLayout_2.addWidget(self.lineEdit_oFile)
        self.pushButton_oFile = QtWidgets.QPushButton(Dialog_QENStoCSV)
        self.pushButton_oFile.setObjectName("pushButton_oFile")
        self.horizontalLayout_2.addWidget(self.pushButton_oFile)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.checkBox_Susceptivility = QtWidgets.QCheckBox(Dialog_QENStoCSV)
        self.checkBox_Susceptivility.setObjectName("checkBox_Susceptivility")
        self.horizontalLayout_5.addWidget(self.checkBox_Susceptivility)
        spacerItem3 = QtWidgets.QSpacerItem(138, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem3)
        self.label_Temp = QtWidgets.QLabel(Dialog_QENStoCSV)
        self.label_Temp.setObjectName("label_Temp")
        self.horizontalLayout_5.addWidget(self.label_Temp)
        self.lineEdit_Temp = QtWidgets.QLineEdit(Dialog_QENStoCSV)
        self.lineEdit_Temp.setObjectName("lineEdit_Temp")
        self.horizontalLayout_5.addWidget(self.lineEdit_Temp)
        self.label_K = QtWidgets.QLabel(Dialog_QENStoCSV)
        self.label_K.setObjectName("label_K")
        self.horizontalLayout_5.addWidget(self.label_K)
        self.verticalLayout_5.addLayout(self.horizontalLayout_5)
        spacerItem4 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem4)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.pushButton_Save = QtWidgets.QPushButton(Dialog_QENStoCSV)
        self.pushButton_Save.setObjectName("pushButton_Save")
        self.horizontalLayout_3.addWidget(self.pushButton_Save)
        self.pushButton_Exit = QtWidgets.QPushButton(Dialog_QENStoCSV)
        self.pushButton_Exit.setObjectName("pushButton_Exit")
        self.horizontalLayout_3.addWidget(self.pushButton_Exit)
        self.verticalLayout_4.addLayout(self.horizontalLayout_3)
        self.line = QtWidgets.QFrame(Dialog_QENStoCSV)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout_4.addWidget(self.line)
        self.label_log = QtWidgets.QLabel(Dialog_QENStoCSV)
        self.label_log.setObjectName("label_log")
        self.verticalLayout_4.addWidget(self.label_log)
        self.textBrowser_log = QtWidgets.QTextBrowser(Dialog_QENStoCSV)
        self.textBrowser_log.setMaximumSize(QtCore.QSize(16777215, 50))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.textBrowser_log.setFont(font)
        self.textBrowser_log.setObjectName("textBrowser_log")
        self.verticalLayout_4.addWidget(self.textBrowser_log)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_6.addLayout(self.verticalLayout_5)

        self.retranslateUi(Dialog_QENStoCSV)
        self.pushButton_Exit.clicked.connect(Dialog_QENStoCSV.reject) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(Dialog_QENStoCSV)

    def retranslateUi(self, Dialog_QENStoCSV):
        _translate = QtCore.QCoreApplication.translate
        Dialog_QENStoCSV.setWindowTitle(_translate("Dialog_QENStoCSV", "QENS to CSV"))
        self.label_input.setText(_translate("Dialog_QENStoCSV", "Input path and file name:"))
        self.lineEdit_iFile.setText(_translate("Dialog_QENStoCSV", os.path.expanduser('~')))
        self.pushButton_iFile.setText(_translate("Dialog_QENStoCSV", "Browse"))
        self.label_intrument.setText(_translate("Dialog_QENStoCSV", "Instrument:"))
        self.radioButton_IN5.setText(_translate("Dialog_QENStoCSV", "IN5"))
        self.radioButton_IN16B.setText(_translate("Dialog_QENStoCSV", "IN16B"))
        self.radioButton_FOCUS.setText(_translate("Dialog_QENStoCSV", "FOCUS"))
        self.radioButton_LET.setText(_translate("Dialog_QENStoCSV", "LET"))
        self.label_output.setText(_translate("Dialog_QENStoCSV", "Output path and file name:"))
        self.lineEdit_oFile.setText(_translate("Dialog_QENStoCSV", os.path.expanduser('~')))
        self.pushButton_oFile.setText(_translate("Dialog_QENStoCSV", "Browse"))
        self.checkBox_Susceptivility.setText(_translate("Dialog_QENStoCSV", "Save susceptivility too"))
        self.label_Temp.setText(_translate("Dialog_QENStoCSV", "T = "))
        self.label_Temp.setDisabled(True)
        self.label_K.setText(_translate("Dialog_QENStoCSV", "K"))
        self.label_K.setDisabled(True)
        self.lineEdit_Temp.setDisabled(True)
        self.pushButton_Save.setText(_translate("Dialog_QENStoCSV", "Save as CSV"))
        self.pushButton_Exit.setText(_translate("Dialog_QENStoCSV", "Exit"))
        self.label_log.setText(_translate("Dialog_QENStoCSV", "Log:"))
