#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""App to sort QENS data.

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
    QApplication, QDialog, QFileDialog)  # QMainWindow, QMessageBox,
from PyQt5.QtCore import QDateTime  # , Qt
from PyQt5.QtGui import QColor

from QENStoCSV_Dlg import Ui_Dialog_QENStoCSV


class DLG(QDialog, Ui_Dialog_QENStoCSV):
    """DLG window class.

    A class used to create the dialog window. Contains the methods
    to run the elements of the dlg.

    Attributes
    ----------
    _instrument: str
        to save the instrument in which the data was recorded
    _rb_value:
        to save the radiobutton state
    _iFileName: str
        to save the input file name and path
    _oFileName: str
        to save the output file name and path
    _defaultPath: str
        to save the default path when initializing the app
    _susceptivility_checked: bool
        to save the value of the susceptivility checkbox
    _temperature: str
        to save the (str) value of the temperature introduced
        in the lineEdit
    _last_msg: str
        to save the last message displayed in the log textBrowser
    _current_date: str
        to save the current date and time when displaying a msg
    _funcionesLeer: FuncionesLeer
        an instance to the class FuncionesLeer][QENS_to_csv_pkg.FuncionesLeer]
        to read and write from/to the input/output files

    Methods
    -------
    set_iFile_DisplayText(text)
        Sets the input display's text
    set_oFile_DisplayText(text)
        Sets the output display's text
    display_iFile_Text()
        Gets the input display's text
    display_oFile_Text()
        Gets the output display's text
    open_iFileDialog()
        Creates the browser dlg to select the input file
    open_oFileDialog()
        Creates the browser dlg to select the output file
    display_temp_Text()
        Gets the temperature display's text
    updateRadioSelection()
        Checks the radio buttons
    updateCheckBoxState()
        Saves the checkbox's value
    sortAndSave()
        Sorts the input data in a matrix form
        and saves it as csv
    """

    def __init__(self, parent=None):
        """Class constructor.

        Attributes
        ----------
        _intrument: str
            the name of the instrument in which the data was recorded
        _rb_value: str
            the value of the radio button to select the intrument
        _iFileName: str
            the name of the input data file
        _oFileName: str
            the name of the output data file
        _defaultPath: str
            the default path in the browser.
            It is set to "./User/Documents"
        _susceptivility_checked: bool
            the status of the check box that gives the option to save
            the susceptivility
        _temperature: str
            the string value of the temperature introduced in the dlg
        _last_msg: str
            the last message shown in the log section
        _current_date: str
            the date shown in the last message in the log section
        """
        super().__init__(parent)
        self.setupUi(self)
        print('Initialized')
        self._instrument = ''
        self._rb_value = 'unchecked'
        self._iFileName = ''
        self._oFileName = ''
        self._defaultPath = os.path.expanduser('~')
        # self._ifile_selected = False
        # self._ofile_selected = False
        self._susceptivility_checked = False
        self._temperature = ''
        self._last_msg = ''
        self._current_date = ''
        # self._error: IOError # se puede asignar a algo que no haya nada?

        self._funcionesLeer = fl.FuncionesLeer()

    def set_iFile_DisplayText(self, text: str):
        """Set the input display's text.

        Set the input display's text, when selecting something from
        the browser, for instance

        Parameters
        ----------
        text: str
            the text to be displayed
        """
        self.lineEdit_iFile.setText(text)
        self.lineEdit_iFile.setFocus()

    def set_oFile_DisplayText(self, text: str):
        """Set the input display's text.

        Set the output display's text, when selecting something from
        the browser, for instance

        Parameters
        ----------
        text: str
            the text to be displayed
        """
        self.lineEdit_oFile.setText(text)
        self.lineEdit_oFile.setFocus()

    def display_iFile_Text(self) -> str:
        """Get the input display's text.

        Returns
        -------
        lineEdit_iFile.text(): str
            the text in the display
        """
        return self.lineEdit_iFile.text()

    def display_oFile_Text(self) -> str:
        """Get the output display's text.

        Returns
        -------
        lineEdit_oFile.text(): str
            the text in the display
        """
        return self.lineEdit_oFile.text()

    def open_iFileDialog(self):
        """Create the browser dlg to select the input file."""
        ifile_dialog = QFileDialog(self)
        ifile_dialog.setWindowTitle('Open Input File')
        ifile_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptOpen)
        self._iFileName = self.display_iFile_Text()
        if self._iFileName == '':
            ifile_dialog.setDirectory(self._defaultPath)
        else:
            try:
                self._funcionesLeer.check_path(self._iFileName)
            except IOError:  # as error:
                ifile_dialog.setDirectory(self._defaultPath)
            else:
                ifile_dialog.setDirectory(self._iFileName)

        ifile_dialog.setNameFilter('Text (*.inx *.dat *.txt)')
        ifile_dialog.setFileMode(QFileDialog.FileMode.ExistingFile)
        ifile_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if ifile_dialog.exec():
            # Así se guarda el nombre del archivo y la ruta
            self._iFileName = ifile_dialog.selectedFiles()
            self.set_iFile_DisplayText(self._iFileName[0])

    def display_temp_Text(self) -> str:
        """Get the temperature display's text.

        Returns
        -------
        lineEdit_Temp.text(): str
            the text in the display

        """
        return self.lineEdit_Temp.text()

    def open_oFileDialog(self):
        """Create the browser dlg to select the output file."""
        ofile_dialog = QFileDialog(self)
        ofile_dialog.setWindowTitle("Set Output File Name")
        ofile_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
        self._oFileName = self.display_oFile_Text()
        if self._oFileName == '':
            ofile_dialog.setDirectory(self._defaultPath)
            try:
                self._funcionesLeer.check_path(self._oFileName)
            except IOError:  # as error:
                ofile_dialog.setDirectory(self._defaultPath)
            else:
                ofile_dialog.setDirectory(self._oFileName)

        ofile_dialog.setNameFilter("Text (*.csv)")
        ofile_dialog.setViewMode(QFileDialog.ViewMode.Detail)

        if ofile_dialog.exec():
            # Así se guarda e nombre del archivo y la ruta
            self._oFileName = ofile_dialog.selectedFiles()
            self.set_oFile_DisplayText(self._oFileName[0])

    def updateRadioSelection(self) -> bool:
        """Check the radio buttons."""
        # get the radio button the send the signal
        rb = self.sender()
        # check if the radio button is checked
        if rb.isChecked():
            self._rb_value = 'cheked'
            self._instrument = rb.text()
        return True

    def updateCheckBoxState(self):
        """Save the checkbox's value.

        Also enables/disables the temperature lineEdit.
        """
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
        """Sort input data and save as csv.

        Check if all the conditions meet to sort and save the data,
        and if so, proceeds.

        Other parameters
        ----------------
        _iFileName: str
            to save the input file name and path
        _oFileName: str
            to save the output file name and path
        _current_date: str
            to save the current date and time when displaying a msg
        _last_msg: str
            to save the last message displayed in the log textBrowser
        qvalue: list[float]
            to save the Q values
        energy: list[list[float]]
            to save the Energy array for each Q
        scatInt: list[list[float]]
            to save the scattered intensity for each Q
        err: list[list[float]]
            to save the measured error in the intensity for each Q
        iFile: _io.TextIOWrapper
            to save the opened input file
        path: str
            to save the path
        dfS: pandas.DataFrame
            to save the S(Q, E) in a matrix form
        dfChiSorted: pandas.DataFrame
            to save the Chi (Q, E) in a matrix from
        temp: float
            to save the numeric value of the temperature

        Raises
        ------
        OSError
            if the path or the file does not exist
        """
        # Lo primero debería comprobar que los valores de los edit de
        # los files existen.
        self._iFileName = self.display_iFile_Text()
        self._oFileName = self.display_oFile_Text()

        # Necesito comprobar que algún radio button está seleccionado
        if self._rb_value == 'unchecked':
            self._current_date = QDateTime.currentDateTime().\
                toString('hh:mm:ss')
            self._last_msg = self._current_date + ': Select instrument\n'
            self.textBrowser_log.setTextColor(QColor(255, 51, 0))
            self.textBrowser_log.insertPlainText(self._last_msg)
            return False

        try:
            self._funcionesLeer.check_path(self._iFileName)
        except IOError as error:
            self._current_date = QDateTime.currentDateTime().\
                toString('hh:mm:ss')
            self._last_msg = self._current_date + ': ' + \
                str(error.strerror) + 'Enter a valid input path\n'
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
                    self._current_date = QDateTime.currentDateTime().\
                        toString('hh:mm:ss')
                    self._last_msg = self._current_date + ': ' + \
                        str(error.strerror) + '\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False
                else:
                    # Llamo a la función que me guarda los datos en listas
                    qvalue, energy, scatInt, err = self._funcionesLeer.\
                        read_from_ifile(iFile, self._instrument)
                    # Y cierro el archivo de datos
                    self._funcionesLeer.close_iFile(iFile)
            else:
                qvalue, energy, scatInt, err = self._funcionesLeer.\
                    leer_de_LET(self._iFileName)
                # corto el nombre del archivo y lo junto con el path otra vez
                # para poder nombrar las columnas en los data frames
                path: str
                path = os.path.dirname(self._iFileName)
                self._iFileName = path + \
                    self._funcionesLeer.fileNameDropLET(self._iFileName)

            # Defino el Data Frame para guardar S(Q,E)
            dfS: pd.DataFrame
            # Llamo a la función que me guarda los datos en DataFrame de Pandas
            dfS = self._funcionesLeer.data_to_pandas_df(
                self._iFileName, qvalue, energy, scatInt, err)

            # Por último, exporto S(Q,E) a  CSVs
            try:
                self._funcionesLeer.check_path(self._oFileName)
            except IOError as error:
                self._current_date = QDateTime.currentDateTime().\
                    toString('hh:mm:ss')
                self._last_msg = self._current_date + ': ' + \
                    str(error.strerror) + 'Enter a valid output path\n'
                self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                self.textBrowser_log.insertPlainText(self._last_msg)
                return False
            else:
                try:
                    self._funcionesLeer.save_data_to_csv(self._oFileName, dfS)
                except IOError:
                    self._current_date = QDateTime.currentDateTime().\
                        toString('hh:mm:ss')
                    self._last_msg = self._current_date + \
                        ': Error exporting data to CSV!\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False
                else:
                    self._current_date = QDateTime.currentDateTime().\
                        toString('hh:mm:ss')
                    self._last_msg = self._current_date + \
                        ': Data succesfully exported to CSV!\n'
                    self.textBrowser_log.insertPlainText(self._last_msg)

            if self._susceptivility_checked is True:
                # Guardo el valor de la temperatura
                self._temperature = self.display_temp_Text()
                temp: float
                try:
                    temp = float(self._temperature)
                except ValueError:
                    self._current_date = QDateTime.currentDateTime().\
                        toString('hh:mm:ss')
                    self._last_msg = self._current_date + \
                        ': Enter a valid temperature\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False

                # Defino el DataFrame donde voy a guardar la susceptibilidad
                dfChiSorted: pd.DataFrame
                # Llamo a la función que me calcula Chi a partir de E y S(Q,E)
                # y me lo guarda en un DataFrame
                dfChiSorted = self._funcionesLeer.chi_from_S(temp, qvalue, dfS)
                # Por último, exporto Chi(Q,E) a  CSVs
                try:
                    self._funcionesLeer.check_path(self._oFileName)
                except IOError as error:
                    self._current_date = QDateTime.currentDateTime().\
                        toString('hh:mm:ss')
                    self._last_msg = self._current_date + ': ' + \
                        str(error.strerror) + 'Enter a valid output path\n'
                    self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                    self.textBrowser_log.insertPlainText(self._last_msg)
                    return False
                else:
                    try:
                        self._funcionesLeer.save_chi_data_to_csv(
                            self._oFileName, dfChiSorted)
                    except IOError:
                        self._current_date = QDateTime.currentDateTime().\
                            toString('hh:mm:ss')
                        self._last_msg = self._current_date + \
                            ': Error exporting susceptivility data to CSV!\n'
                        self.textBrowser_log.setTextColor(QColor(255, 51, 0))
                        self.textBrowser_log.insertPlainText(self._last_msg)
                        return False
                    else:
                        self._current_date = QDateTime.currentDateTime().\
                            toString('hh:mm:ss')
                        self._last_msg = self._current_date + \
                            ': Susceptivility data exported to CSV!\n'
                        self.textBrowser_log.insertPlainText(self._last_msg)
        return True


# Esta clase es para conectar las señales y los slots
class QENStoCSV:
    """QENStoCSV's controller class.

    Conects the signals with the actions.

    Attributes
    ----------
    view: DLG
        is the class of dlg window to acces the elements
        sendig out the signals.

    Methods
    -------
    _connectSignalsAndSlots()
        Connects signals and slots
    """

    def __init__(self, view):
        """Class constructor."""
        self._view = view  # A view le voy a asignar la clase de la ventana
        self._connectSignalsAndSlots()

    # Esta función conecta los botones de la interface con las acciones del
    # programa
    def _connectSignalsAndSlots(self):
        self._view.pushButton_iFile.clicked.connect(
            self._view.open_iFileDialog)
        self._view.pushButton_oFile.clicked.connect(
            self._view.open_oFileDialog)
        self._view.pushButton_Save.clicked.connect(self._view.sortAndSave)
        self._view.radioButton_IN5.toggled.connect(
            self._view.updateRadioSelection)
        self._view.radioButton_IN16B.toggled.connect(
            self._view.updateRadioSelection)
        self._view.radioButton_FOCUS.toggled.connect(
            self._view.updateRadioSelection)
        self._view.radioButton_LET.toggled.connect(
            self._view.updateRadioSelection)
        self._view.checkBox_Susceptivility.stateChanged.connect(
            self._view.updateCheckBoxState)


def main():
    """Run the App."""
    app = QApplication(sys.argv)
    dlg = DLG()
    dlg.show()
    QENStoCSV(view=dlg)
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
