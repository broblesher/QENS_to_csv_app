#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: app_QENStoCSV_Dlg.py
Author: Beatriz Robles Hernández
Date: 2025-03-10
Version: 1.0
Description: 
    This script runs an GUI app to read QENS data files recorded 
    in different facilities, organizes it as a matrix and export
    it as a csv file. Also computes susceptibility if required.

License: GLP
Contact: broblesher@gmail.com
Dependencies: os, sys, _io, pandas, FuncionesLeer, PyQt5, QENStoCSV_Dlg
"""
# Import statements
import os
import sys
import _io
import pandas as pd
import FuncionesLeer as fl

from PyQt5.QtWidgets import (
    QApplication, QDialog, QMainWindow, QMessageBox, QFileDialog
)
from PyQt5.QtCore import QDateTime, Qt
from PyQt5.QtGui import QColor
#from PyQt5.uic import loadUi

from QENStoCSV_Dlg import Ui_Dialog_QENStoCSV

class DLG(QDialog, Ui_Dialog_QENStoCSV):
    def __init__(self, parent = None):
        super().__init__(parent)
        self.setupUi(self)
        print('Initialized')
        self._instrument = ''
        self._rb_value = 'unchecked'
        self._iFileName = ''
        self._oFileName = ''
        self._defaultPath = os.path.expanduser('~')
        self._ifile_selected = False
        self._ofile_selected = False
        self._susceptivility_checked = False
        self._temperature = ''
        self._last_msg = ''
        self._current_date = ''
        #self._error: IOError # se puede asignar a algo que no haya nada?

        self._funcionesLeer = fl.FuncionesLeer()

    # Función que escribe en el display, cuando selecciono del browser, por ejemplo
    def set_iFile_DisplayText(self, text: str): 
        """Set the display's text."""
        self.lineEdit_iFile.setText(text)
        self.lineEdit_iFile.setFocus()

    # Función que escribe en el display, cuando selecciono del browser, por ejemplo
    def set_oFile_DisplayText(self, text: str): 
        """Set the display's text."""
        self.lineEdit_oFile.setText(text)
        self.lineEdit_oFile.setFocus()

    # Función que lee del display de input
    def display_iFile_Text(self) -> str: 
        """Get the display's text."""
        return self.lineEdit_iFile.text()

    # Función que lee del display de output
    def display_oFile_Text(self) -> str:
        """Get the display's text."""
        return self.lineEdit_oFile.text()
    
    # Función es la que genera el dlg del explorador de archivos para elegir el input
    def open_iFileDialog(self):
        ifile_dialog = QFileDialog(self)
        ifile_dialog.setWindowTitle('Open Input File')
        ifile_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self._iFileName = self.display_iFile_Text()
        if self._iFileName == '':
            ifile_dialog.setDirectory(self._defaultPath) 
        else:
            try:
                self._funcionesLeer.check_path(self._iFileName)
            except IOError as error:
                ifile_dialog.setDirectory(self._defaultPath) 
            else:
                ifile_dialog.setDirectory(self._iFileName)

        ifile_dialog.setNameFilter('Text (*.inx *.dat *.txt)')
        ifile_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        ifile_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if ifile_dialog.exec():
            self._iFileName = ifile_dialog.selectedFiles() # Así se guarda e nombre del archivo y la ruta
            self.set_iFile_DisplayText(self._iFileName[0])

    # Función que lee del display de temperatura
    def display_temp_Text(self) -> str: 
        """Get the display's text."""
        return self.lineEdit_Temp.text()

    # Función es la que genera el dlg del explorador de archivos para elegir el output
    def open_oFileDialog(self):
        ofile_dialog = QFileDialog(self)
        ofile_dialog.setWindowTitle("Set Output File Name")
        ofile_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self._oFileName = self.display_oFile_Text()
        if self._oFileName == '':
            ofile_dialog.setDirectory(self._defaultPath) # no consigo que me funcione con path relativo
            try:
                self._funcionesLeer.check_path(self._oFileName)
            except IOError as error:
                ofile_dialog.setDirectory(self._defaultPath) # no consigo que me funcione con path relativo
            else:
                ofile_dialog.setDirectory(self._oFileName)

        ofile_dialog.setNameFilter("Text (*.csv)")
        ofile_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if ofile_dialog.exec():
            self._oFileName = ofile_dialog.selectedFiles() # Así se guarda e nombre del archivo y la ruta
            self.set_oFile_DisplayText(self._oFileName[0])
            #self._last_path = _oFileName[0]
    
    # Función para comprobar los radio buttons
    def updateRadioSelection(self):
        # get the radio button the send the signal
        rb = self.sender()
        # check if the radio button is checked
        if rb.isChecked():
            self._rb_value = 'cheked'
            self._instrument = rb.text()
        return True
    
    # Función que guarda el valor del checkbox cuando lo pulso, y habilita/desabilita la temperatura
    def updateCheckBoxState(self):
        if self.checkBox_Susceptivility.isChecked() is True:
            self.label_Temp.setDisabled(False)
            self.lineEdit_Temp.setDisabled(False)
            self.label_K.setDisabled(False)
            self._susceptivility_checked = True
        if self.checkBox_Susceptivility.isChecked() is False:
            self.label_Temp.setDisabled(True)
            self.lineEdit_Temp.setDisabled(True)
            self.label_K.setDisabled(True)
            self._susceptivility_checked = False

    # Función que se ejecuta cuando pulso save
    def sortAndSave(self) -> bool:
        # Lo primero debería comprobar que los valores de los edit de los files existen.
        self._iFileName = self.display_iFile_Text()
        self._oFileName = self.display_oFile_Text()
        
        # Necesito comprobar que algún radio button está seleccionado
        if self._rb_value == 'unchecked':
            self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
            self._last_msg = self._current_date + ': Select instrument\n'
            self.textBrowser_log.setTextColor(QColor(255, 51, 0))
            self.textBrowser_log.insertPlainText(self._last_msg)
            return False

        try:
            self._funcionesLeer.check_path(self._iFileName)
        except IOError as error:
            self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
            self._last_msg = self._current_date + ': ' + str(error.strerror) + 'Enter a valid input path\n'
            self.textBrowser_log.setTextColor(QColor(255, 51, 0))
            self.textBrowser_log.insertPlainText(self._last_msg)
            return False
        else:
            # "Declaro" variables para guardar los datos
            qvalue: list[float]
            energy: list[list[float]]
            scatInt: list[list[float]]
            err: list[list[float]]

            if (self._instrument != 'LET'):
                iFile: _io.TextIOWrapper
                # LLamo a la función que abre el fichero con las medidas
                try:   
                    iFile = self._funcionesLeer.open_iFile(self._iFileName)
                except OSError as error:
                    self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                    #self._last_msg = self._current_date + ': Input file does not exist\n'
                    self._last_msg = self._current_date + ': ' + str(error.strerror) + '\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False
                else:
                    # Llamo a la función que me guarda los datos en listas
                    qvalue, energy, scatInt, err = self._funcionesLeer.read_from_ifile(iFile, self._instrument)
                    # Y cierro el archivo de datos
                    self._funcionesLeer.close_iFile(iFile)
            else:
                qvalue, energy, scatInt, err = self._funcionesLeer.leer_de_LET(self._iFileName)
                path: str
                path = os.path.dirname(self._iFileName)
                self._iFileName = path + self._funcionesLeer.fileNameDropLET(self._iFileName)

            # Defino el Data Frame para guardar S(Q,E)
            dfS: pd.DataFrame
            # Llamo a la función que me guarda los datos en DataFrame de Pandas
            dfS = self._funcionesLeer.data_to_pandas_df(self._iFileName, qvalue, energy, scatInt, err)
            
            # Por último, exporto S(Q,E) a  CSVs
            try:
                self._funcionesLeer.check_path(self._oFileName)
            except IOError as error:
                self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                self._last_msg = self._current_date + ': ' + str(error.strerror) + 'Enter a valid output path\n'
                self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                self.textBrowser_log.insertPlainText(self._last_msg)
                return False
            else:
                try:
                    self._funcionesLeer.save_data_to_csv(self._oFileName, dfS)
                except:
                    self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                    self._last_msg = self._current_date + ': Error exporting data to CSV!\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False
                else:
                    self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                    self._last_msg = self._current_date + ': Data succesfully exported to CSV!\n'
                    self.textBrowser_log.insertPlainText(self._last_msg)

            if self._susceptivility_checked == True:
                # Guardo el valor de la temperatura
                self._temperature = self.display_temp_Text()
                temp: float
                try:
                    temp = float(self._temperature)
                except ValueError:
                    self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                    self._last_msg = self._current_date + ': Enter a valid temperature\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False
                
                # Defino el DataFrame donde voy a guardar la susceptibilidad Chi
                dfChiSorted: pd.DataFrame
                # Llamo a la función que me calcula Chi a partir de E y S(Q,E) y me lo guarda en un DataFrame
                dfChiSorted = self._funcionesLeer.chi_from_S(temp, qvalue, dfS)
                # Por último, exporto Chi(Q,E) a  CSVs
                try:
                    self._funcionesLeer.check_path(self._oFileName)
                except IOError as error:
                    self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                    self._last_msg = self._current_date + ': ' + str(error.strerror) + 'Enter a valid output path\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False
                else:
                    try:
                        self._funcionesLeer.save_chi_data_to_csv(self._oFileName, dfChiSorted)# dfS,
                    except:
                        self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                        self._last_msg = self._current_date + ': Error exporting susceptivility data to CSV!\n'
                        self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                        self.textBrowser_log.insertPlainText(self._last_msg)
                        return False
                    else:
                        self._current_date = QDateTime.currentDateTime().toString('hh:mm:ss')
                        self._last_msg = self._current_date + ': Susceptivility data succesfully exported to CSV!\n'
                        self.textBrowser_log.insertPlainText(self._last_msg)
        return True


# Esta clase es para conectar las señales y los slots
class QENStoCSV:
    """QENStoCSV's controller class."""
    def __init__(self, view): 
        self._view = view # A view le voy a asignar la clase de la ventana
        self._connectSignalsAndSlots()

    def _connectSignalsAndSlots(self): # Esta función conecta los botones de la interface con las acciones del programa
        self._view.pushButton_iFile.clicked.connect(self._view.open_iFileDialog)
        self._view.pushButton_oFile.clicked.connect(self._view.open_oFileDialog)
        self._view.pushButton_Save.clicked.connect(self._view.sortAndSave)
        self._view.radioButton_IN5.toggled.connect(self._view.updateRadioSelection)
        self._view.radioButton_IN16B.toggled.connect(self._view.updateRadioSelection)
        self._view.radioButton_FOCUS.toggled.connect(self._view.updateRadioSelection)
        self._view.radioButton_LET.toggled.connect(self._view.updateRadioSelection)
        self._view.checkBox_Susceptivility.stateChanged.connect(self._view.updateCheckBoxState)



def main():
    app = QApplication(sys.argv)
    dlg = DLG()
    dlg.show()
    QENStoCSV(view = dlg)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()