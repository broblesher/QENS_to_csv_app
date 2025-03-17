#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""FuncionesLeer class.

Filename: FuncionesLeer.py  
Author: Beatriz Robles Hernández  
Date: 2025-03-10  
Version: 1.0  
Description:
    This module contains a class with the functions
    necesary to read from data files, save data in
    pandas data frames, and write data to csv files.

License: GLP  
Contact: broblesher@gmail.com  
Dependencies: os, _io, pandas, matplotlip.pyplot, numpy, numpy.typing
"""
# Import statements
import os
import _io
import pandas as pd
import numpy as np


class FuncionesLeer:
    """FuncionesLeer class.

    A class used to colect the methos to read QENS data from text file,
    transform the data into a matrix, and write it to a csv file.

    Methods
    -------
    fileNameDropLET(iFileName)
        Trims the filenames of the LET input file
    check_path(path)
        Checks if the path exist
    open_iFile(fileName)
        Opens the data file
    close_iFile(iFile)
        Closes the data file
    leer_de_IN5(iFile:, qvalue,energy, scatInt, err)
        Parses the IN5 data files
    leer_de_IN16B(iFile:, qvalue,energy, scatInt, err)
        Parses the IN16B data files
    leer_de_FOCUS(iFile:, qvalue,energy, scatInt, err)
        Parses the FOCUS data files
    leer_de_LET(iFileName)
        Parses the LET data files
    read_from_ifile(iFile, instrument)
        Reads from input files and saves the data in lists
    data_to_pandas_df(fileName, qvalue, energy, scatInt, err)
        Saves S(Q, E) data in a pandas DataFrame.
    chi_from_S(temp, qvalue, dfS)
        Calculates Chi(Q, E) from S(Q, E) at a given T
    save_data_to_csv(oFileName, dfS)
        Saves the data in the S(Q, E) pandas.DataFrame to a csv file.
    save_chi_data_to_csv(oFileName, dfchiSorted)
        Saves the data in the Chi(Q, E) pandas.DataFrame to a csv file.
    """

    def __init__(self):
        """Class constructor."""
        print('FuncionesLeer constructor')

    def fileNameDropLET(self, iFileName: str) -> str:
        """Trim LET files names.

        Trims the filenames of the LET input file to find all the
        files begining with the same characters, belonging to the
        same measurement.

        Parameters
        ----------
        iFileName:
            the filename, icluding the path

        Returns
        -------
        fileName: str
            the filename, excluding the path

        Other parameters
        ---------
        firstParethesisPos: int
            the position in fileName of the first parenthesis
        charDrop: int
            the number of characters (at the endo of the filename)
            to delete
        """
        fileName: str
        fileName = os.path.basename(iFileName)  # quita la ruta (path)
        firstParethesisPos: int
        # busco la primera aparición de el paréntesis
        firstParethesisPos = fileName.index('(')
        charDrop: int
        # calculo el número de caracteres que quiero eliminar
        charDrop = len(fileName) - firstParethesisPos
        fileName = fileName[:-charDrop]
        return fileName

    def check_path(self, path: str) -> bool:
        """Check if the path exist.

        Parameters
        ----------
        path: str
            the input path

        Raises
        ------
        IOError
        """
        if not os.path.exists(os.path.dirname(path)):
            raise IOError(2, 'Path does not exist. ')
        else:
            return True

    def open_iFile(self, fileName: str) -> _io.TextIOWrapper:
        """Open the data file.

        Parameters
        ----------
        fileName: str
            the data file to be open, with path included

        Returns
        -------
        iFile: _io.TextIOWrapper
            the object to which the open file is assigned

        Raises
        ------
        err: IOError
            the IOError to save the error
        """
        # msg: str
        iFile: _io.TextIOWrapper
        try:
            iFile = open(fileName, "r")  # abro el input file
        except IOError:  # as err:
            # msg = str(err.strerror)
            raise OSError(2, 'Input file does not exist. ')
            # return msg
        else:
            return iFile

    def close_iFile(self, iFile: _io.TextIOWrapper) -> bool:
        """Close the data file.

        Parameters
        ----------
        iFile: _io.TextIOWrapper
            the input object of the opened data file
        """
        iFile.close()  # Cuando acabo de leer el fichero, lo cierro
        if iFile.closed is False:
            print("Error closing file!")
            return False
        else:
            print("File closed!")
            return True

    def leer_de_IN5(self, iFile: _io.TextIOWrapper, qvalue: list[float],
                    energy: list[list[float]], scatInt: list[list[float]],
                    err: list[list[float]]) -> tuple:
        """Parse the IN5 data files.

        Parameters
        ----------
        iFile: _io.TextIOWrapper
            the objecto with the input file open
        qvalue: list[float]
            the array with the Q values
        energy: list[list[float]]
            the array with the arays of measured energies,
            for earch Q
        scatInt: list[list[float]]
            the array with the arays of measured intensities,
            for earch Q
        err: list[list[float]]
            the array with the arays of measured errors,
            for earch Q

        Returns
        -------
        A tuple with the values:
        qvalue: list[float]
        energy: list[list[float]]
        scatInt: list[list[float]]
        err: list[list[float]]

        Other parameters
        ----------------
        line: str
            to read de file line by line
        elements: list[str]
            to save all the elements of a line in a list
        numq: int
            to Q iterator (contador de Q, para cambiar de Q)
        """
        line: str
        elements: list[str]
        numq: int
        numq = 0  # Pongo el contador de Q a cero

        for line in iFile.readlines():
            elements = line.split()  # Divido la línea en elementos
            if (len(elements) != 0):  # la línea leída no está vacía
                # Para IN5, si son 6, el primer elemento es la Q
                if (len(elements) == 6):
                    # añado la Q a la lista correspondiente
                    qvalue.append(float(elements[0]))
                    # añado una lista vacía a E, S(Q,E) y err
                    energy.append([])
                    scatInt.append([])
                    err.append([])
                    numq = numq + 1  # Sumo uno al contador de Q
                # Si tengo 3 elementos en la línea, son E, S(Q, E) y err
                if (len(elements) == 3):
                    # hay una linea chunga que no sé que es y empieza por 0
                    # la descarto
                    if (float(elements[0]) != 0):
                        # Añado los valores a las listas correspondientes
                        energy[numq-1].append(float(elements[0]))
                        scatInt[numq-1].append(float(elements[1]))
                        err[numq-1].append(float(elements[2]))
        return qvalue, energy, scatInt, err

    def leer_de_IN16B(self, iFile: _io.TextIOWrapper, qvalue: list[float],
                      energy: list[list[float]], scatInt: list[list[float]],
                      err: list[list[float]]) -> tuple:
        """Parse the IN16B data files.

        Parameters
        ----------
        iFile: _io.TextIOWrapper
            the object with the input file open
        qvalue: list[float]
            the array with the Q values
        energy: list[list[float]]
            the array with the arays of measured energies,
            for earch Q
        scatInt: list[list[float]]
            the array with the arays of measured intensities,
            for earch Q
        err: list[list[float]]
            the array with the arays of measured errors,
            for earch Q

        Returns
        -------
        A tuple with the values:
        qvalue: list[float]
        energy: list[list[float]]
        scatInt: list[list[float]]
        err: list[list[float]]

        Other parameters
        ----------------
        line: str
            to read de file line by line
        elements: list[str]
            to save all the elements of a line in a list
        numq: int
            to Q iterator (contador de Q, para cambiar de Q)
        """
        line: str
        elements: list[str]
        numq: int
        numq = 0  # Pongo el contador de Q a cero

        for line in iFile.readlines():
            elements = line.split()  # Divido la línea en elementos
            if (len(elements) != 0):  # la línea leída no está vacía
                # Para IN16B, busco la Q
                if (elements[0] == "#" and elements[1] == "q(Angstrom^-1)"):
                    # añado la Q a la lista correspondiente
                    qvalue.append(float(elements[3]))
                    # añado una lista vacía a E, S(Q,E) y err
                    energy.append([])
                    scatInt.append([])
                    err.append([])
                    numq = numq + 1  # Sumo uno al contador de Q
                # Si hay elementos y no empiezan por #, son los datos
                if (elements[0] != "#"):
                    # Añado los valores a la lista correspondiente
                    energy[numq-1].append(float(elements[0]))
                    scatInt[numq-1].append(float(elements[1]))
                    err[numq-1].append(float(elements[2]))
        return qvalue, energy, scatInt, err

    def leer_de_LET(self, iFileName: str) -> tuple:
        """Parse the LET data files.

        Parameters
        ----------
        iFileName: str
            the input filename, with path

        Returns
        -------
        A tuple with the values:
        qvalue: list[float]
        energy: list[list[float]]
        scatInt: list[list[float]]
        err: list[list[float]]

        Other parameters
        ----------------
        qvalue: list[float]
            the array with the Q values
        energy: list[list[float]]
            the array with the arays of measured energies,
            for earch Q
        scatInt: list[list[float]]
            the array with the arays of measured intensities,
            for earch Q
        err: list[list[float]]
            the array with the arays of measured errors,
            for earch Q
        line: str
            to read de file line by line
        elements: list[str]
            to save all the elements of a line in a list
        qlist: list[str]
            to save the string of the line where the Q interval is
        qmin: float
            the minimum Q in the Q interval
        qmax: float
            the maximum Q in the Q interval
        qcurr: float
            the Q of the currently reading input file
        numq: int
            to Q iterator (contador de Q, para cambiar de Q)
        filenames: list[str]
            list with al the files in the folder
        dirs: list[str]
            list with the subdirectories in the folder
        root: str
            # me imagino que el path?
        f: str
        files: list[str]
            the array where I save the file names that I want to read from
        path: str
            the path where the files are
        iFile: _io.TextIOWrapper
            the object with the input file open
        """
        qvalue: list[float]
        energy: list[list[float]]
        scatInt: list[list[float]]
        err: list[list[float]]
        qvalue = []
        energy = []
        scatInt = []
        err = []

        line: str
        elements: list[str]
        qlist: list[str]
        qmin: float  # la Q minima del intervalo
        qmax: float  # la Q maxima del intervalo
        qcurr: float  # la Q corespondiente al fichero q está leyendo
        numq: int  # es el contador que voy a usar para cambiar de Q
        numq = 0  # Pongo el contador de Q a cero
        # Lo primero que tengo que hacer es buscar los ficheros que me
        # interesan en la carpeta
        filenames: list[str]  # la lista de todos los archivos en la carpeta
        dirs: list[str]  # la lista de subdirectorios en la carpeta
        root: str  # me imagino que el path?
        f: str
        files: list[str]
        files = []
        path: str
        path = os.path.dirname(iFileName)
        fileName = self.fileNameDropLET(iFileName)
        for (root, dirs, filenames) in os.walk(path):
            for f in filenames:
                if fileName in f and '.txt' in f:
                    files.append(f)

        iFile: _io.TextIOWrapper
        for f in files:
            try:
                iFile = self.open_iFile(path + '/' + f)
            except IOError:  # as error:
                pass
                # pongo algo más? qué quiero que haga si no consigue
                # abrir un fichero?
            else:
                for line in iFile.readlines():
                    elements = line.split()  # Divido la línea en elementos
                    if (len(elements) != 0):  # Si la línea leída no está vacía
                        # Para LET la Q está en la línea que empieza así:
                        if (elements[1] == "Integration"):
                            qlist = elements[3].split(",")
                            qmin = float(qlist[1])
                            qmax = float(qlist[2])
                            qcurr = qmin + (qmax - qmin) / 2
                            # añado la Q a la lista correspondiente
                            qvalue.append(qcurr)
                            # añado una lista vacía a E, S(Q,E) y err
                            energy.append([])
                            scatInt.append([])
                            err.append([])
                            numq = numq + 1  # Sumo uno al contador de Q
                        # Si hay elementos y no empiezan por #, son los datos
                        if (elements[0] != "#"):
                            # Añado los valores a la lista correspondiente
                            energy[numq-1].append(float(elements[0]))
                            scatInt[numq-1].append(float(elements[1]))
                            err[numq-1].append(float(elements[2]))
                self.close_iFile(iFile)
        return qvalue, energy, scatInt, err

    def leer_de_FOCUS(self, iFile: _io.TextIOWrapper, qvalue: list[float],
                      energy: list[list[float]], scatInt: list[list[float]],
                      err: list[list[float]]) -> tuple:
        """Parse the FOCUS data files.

        Parameters
        ----------
        iFile: _io.TextIOWrapper
            the object with the input file open
        qvalue: list[float]
            the array with the Q values
        energy: list[list[float]]
            the array with the arays of measured energies,
            for earch Q
        scatInt: list[list[float]]
            the array with the arays of measured intensities,
            for earch Q
        err: list[list[float]]
            the array with the arays of measured errors,
            for earch Q

        Returns
        -------
        A tuple with the values:
        qvalue: list[float]
        energy: list[list[float]]
        scatInt: list[list[float]]
        err: list[list[float]]

        Other parameters
        ----------------
        line: str
            to read de file line by line
        elements: list[str]
            to save all the elements of a line in a list
        numq: int
            to Q iterator (contador de Q, para cambiar de Q)
        """
        line: str
        elements: list[str]
        numq: int
        numq = 0  # Pongo el contador de Q a cero

        for line in iFile.readlines():
            elements = line.split()  # Divido la línea en elementos
            if (len(elements) != 0):  # La línea leída no está vacía
                # Para FOCUS la Q está en la línea que empieza así
                if (elements[0] == "#Group" and elements[1] == "Value:"):
                    # añado la Q a la lista correspondiente
                    qvalue.append(float(elements[2]))
                    # añado una lista vacía a E, S(Q,E) y err
                    energy.append([])
                    scatInt.append([])
                    err.append([])
                    numq = numq + 1  # Sumo uno al contador de Q
                # Si hay elementos y no empiezan por #, son los datos
                if (elements[0][0] != "#"):
                    # Añado los valores a la lista correspondiente
                    energy[numq-1].append(float(elements[0]))
                    scatInt[numq-1].append(float(elements[1]))
                    err[numq-1].append(float(elements[2]))
        return qvalue, energy, scatInt, err

    def read_from_ifile(self, iFile: _io.TextIOWrapper,
                        instrument: str) -> tuple:
        """Read from input files and saves the data in lists.

        Calls a diferent parsing function depending on the input
        instrument. **This fuction does not work with LET data.**

        Parameters
        ----------
        iFile: _io.TextIOWrapper
            object with the open input file
        instrument: str
            name of the instrument where the data was recorded

        Returns
        -------
        A tuple with the values:
        qvalue: list[float]
        energy: list[list[float]]
        scatInt: list[list[float]]
        err: list[list[float]]

        Other parameters
        ----------------
        qvalue: list[float]
            the array with the Q values
        energy: list[list[float]]
            the array with the arays of measured energies,
            for earch Q
        scatInt: list[list[float]]
            the array with the arays of measured intensities,
            for earch Q
        err: list[list[float]]
            the array with the arays of measured errors,
            for earch Q

        See Also
        --------
        leer_de_IN5
        leer_de_IN16B
        leer_de_FOCUS
        """
        qvalue: list[float]  # Para guardar los valores de Q
        energy: list[list[float]]  # Para guardar la energía dispersada
        scatInt: list[list[float]]  # Para guardar S(Q,E)
        err: list[list[float]]  # Para guardar el error experimental en S(Q,E)

        # Inicializo las variables a listas vacías
        qvalue = []
        energy = []
        scatInt = []
        err = []

        match instrument:
            case "IN5":
                qvalue, energy, scatInt, err = self.leer_de_IN5(
                    iFile, qvalue, energy, scatInt, err)
            case "IN16B":
                qvalue, energy, scatInt, err = self.leer_de_IN16B(
                    iFile, qvalue, energy, scatInt, err)
            case "FOCUS":
                qvalue, energy, scatInt, err = self.leer_de_FOCUS(
                    iFile, qvalue, energy, scatInt, err)

        return qvalue, energy, scatInt, err

    def data_to_pandas_df(self, fileName: str, qvalue: list[float],
                          energy: list[list[float]],
                          scatInt: list[list[float]],
                          err: list[list[float]]) -> pd.DataFrame:
        """Save S(Q, E) data in a pandas DataFrame.

        Parameters
        ----------
        fileName: str
            the name to the input file, to asing it to the
            intensity column
        qvalue: list[float]
            the array with the Q values
        energy: list[list[float]]
            the array with the array of energies for each Q
        scatInt: list[list[float]]
            the array with the arrays of intensities for each Q
        err: list[list[float]])
            the array with the arrays of errors in the intensity,
            for each Q

        Returns
        -------
        dfS: pd.DataFrame
            DataFrame to save S(Q, E)

        Other parameters
        ----------------
        energyS: pd.Series
            a series to save the energy array for a Q, to concatenate
            to dfS
        scatIntS: pd.Series
            a series to save the scattered intensity array for a Q,
            to concatenate to dfS
        errS: pd.Series
            a series to save the measured error array for a Q, to
            concatenate to dfS
        i: int
            iterator
        q: float
            iterator, to go over qvalue
        scatIntLabel: str
            to write the intensity column label
        qstr: str
            to write the intensity column label

        See Also
        --------
        pandas.DataFrame.concat
        pandas.Series.replace
        """
        dfS: pd.DataFrame
        dfS = pd.DataFrame()
        # declaro estas series porque para que las columnas tengan el
        # mismo nombre tengo que usar concat
        energyS: pd.Series
        scatIntS: pd.Series
        errS: pd.Series

        i: int
        q: float
        scatIntLabel: str
        qstr: str

        for i, q in enumerate(qvalue):
            energyS = pd.Series(energy[i], name="E (meV)")
            # redondeo el valor de Q a 2 decimales
            qstr = "_" + str(round(qvalue[i], 2)) + "A-1"
            scatIntLabel = os.path.basename(fileName)[:-4] + qstr
            scatIntS = pd.Series(scatInt[i], name=scatIntLabel)
            errS = pd.Series(err[i], name="err")
            # En IN5 a veces hay valores del error < 0. Los convierto a 0
            errS = errS.replace(-1, 0)
            dfS = pd.concat([dfS, energyS, scatIntS, errS], axis=1, names=[
                            energyS.name, scatIntS.name, errS.name])

        return dfS

    def chi_from_S(self, temp: float, qvalue: list[float],
                   dfS: pd.DataFrame) -> pd.DataFrame:
        """Calculate the susceptibility.

        Calculate the corresponding susceptibility of a given
        scattered intensity S(Q, E) pandas.DataFrame. For each
        Q value it saves E+, Chi+, E-, Chi-

        Parameters
        ----------
        temp: float
            the temperature at which the data was recorded
        qvalue: list[float]
            the array with the Q values
        dfS: pd.DataFrame
            the pandas.DataFrame with S(Q, E)

        Returns
        -------
        dfchiSorted: pandas.DataFrame

        Other parameters
        ----------------
        energyM: pd.Series
            to save the energies E < 0
        energyP: pd.Series
            to save the energies E > 0
        chiSM: pd.Series
            to save the calculated susceptibilities for E<0
        chiSP: pd.Series
            to save the calculated susceptibilities for E>0
        kb: float  # Boltzmann constant: 8.617333262 x 10-5 eV K-1
        factSusS: pd.Series
            to save the factor
        dfchiM: pd.DataFrame
            to save (E, Chi) for E<0, because once taken the absolute
            value, they need to be sorted in ascending order
        dfchiSorted: pd.DataFrame
            to save the susceptivilities
        """
        # Quiero probar a guardar la susceptibilidad en E+ Chi+ E- Chi-,
        # para cada Q.
        energyM: pd.Series
        energyP: pd.Series
        chiSM: pd.Series
        chiSP: pd.Series
        kb: float
        kb = 8.6173332e-5  # eV K-1
        factSusS: pd.Series
        dfchiM: pd.DataFrame
        dfchiSorted: pd.DataFrame
        dfchiSorted = pd.DataFrame()

        for i, q in enumerate(qvalue):
            # Guardo las E<0 para una Q
            energyM = dfS[dfS.iloc[:, 3 * i] < 0].iloc[:, 3 * i]
            energyM.name = 'E- (meV)'
            factSusS = pd.Series(np.pi * (np.exp(
                energyM.abs()/kb/1000/temp) - 1))
            chiSM = factSusS*dfS[dfS.iloc[:, 3 * i] < 0].iloc[:, 3 * i + 1]
            chiSM.name = dfS.iloc[:, 3 * i + 1].name
            energyM = energyM.abs()
            dfchiM = pd.concat([energyM, chiSM], axis=1)
            dfchiM.sort_values('E- (meV)', ascending=True, inplace=True)
            # dfchiM.sort_values(energyM.name, ascending=True, inplace=True)
            dfchiM.reset_index(drop=True, inplace=True)

            # Guardo las E>0 para una Q
            energyP = dfS[dfS.iloc[:, 3 * i] > 0].iloc[:, 3 * i]
            energyP.name = 'E+ (meV)'
            factSusS = pd.Series(np.pi * (1 - np.exp(-energyP/kb/1000/temp)))
            chiSP = factSusS * dfS[dfS.iloc[:, 3 * i] > 0].iloc[:, 3 * i + 1]
            chiSP.name = dfS.iloc[:, 3 * i + 1].name
            dfchiP = pd.concat([energyP, chiSP], axis=1)
            dfchiP.reset_index(drop=True, inplace=True)

            dfchiSorted = pd.concat([dfchiSorted, dfchiM, dfchiP], axis=1)
            # Borro los data frames antes de que cambie de Q
            del dfchiM, dfchiP

        return dfchiSorted

    def save_data_to_csv(self, oFileName: str, dfS: pd.DataFrame) -> bool:
        """Export S(Q, E) pandas.DataFrame to csv.

        Saves the data in the scattered intensity S(Q, E)
        pandas.DataFrame to a csv file. When exporting the
        DataFrame, I remove ALL the rows only ifthere are NAN
        values in ALL the I and err columns (for all the Q values).

        Parameters
        ----------
        oFileName: str

        dfS: pd.DataFrame
            the data to be exported to a csv

        Other parameters
        ----------------
        thresholdVal: int
            Require that many non-NA values to keep the rows
            >Keep only the rows with at least 'thres' non-NA values.
        """
        thresholdVal: int
        # Todas las E son no-NAN. Si hay una columna más con no-NAN, NO
        # se hace drop.
        thresholdVal = int(len(dfS.columns)/3+1)
        dfS.dropna(axis=0, thresh=thresholdVal, inplace=True)
        dfS.to_csv(oFileName, sep='\t', index=False)

        return True

    def save_chi_data_to_csv(self, oFileName: str,
                             dfchiSorted: pd.DataFrame) -> bool:
        """Export Chi(Q, E) pandas.DataFrame to csv.

        Saves the susceptivility data in the Chi(Q, E) pandas.DataFrame
        to a csv file.When exporting the DataFrame, I remove ALL the rows
        only if there are NAN values in ALL the I and err columns (for
        all the Q values).

        Parameters
        ----------
        oFileName: str

        dfchiSorted: pd.DataFrame
            the data to be exported to a csv

        Other parameters
        ----------------
        thresholdVal: int
            Require that many non-NA values to keep the rows
            >Keep only the rows with at least 'thres' non-NA values.
        """
        thresholdVal: int
        # En este caso, como la E no es simetrica respecto a cero,
        # seguro que solo tengo valores no-NAN para todos las filas
        # de las columnas E-. Hay un rango de filas para las que no
        # tengo valores de E+, y por lo tanto son NAN.
        # Si hay una columna más con no-NAN, no se hace drop
        thresholdVal = int(len(dfchiSorted.columns)/4+1)
        dfchiSorted.dropna(thresh=thresholdVal, inplace=True)
        dfchiSorted.to_csv(oFileName.replace('.csv', '_Chi.csv'), sep='\t',
                           index=False)

        return True
