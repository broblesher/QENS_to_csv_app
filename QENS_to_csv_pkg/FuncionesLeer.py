#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Filename: app_QENStoCSV_Dlg.py
Author: Beatriz Robles Hernández
Date: 2025-03-10
Version: 1.0
Description: 
    This script contains a class with the functions
    necesary to read from data files, save data in 
    pandas data frames, and write data to csv files

License: GLP
Contact: broblesher@gmail.com
Dependencies: os, _io, pandas, matplotlip.pyplot, numpy, numpy.typing
"""
# Import statements
import os
import _io
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from numpy.typing import NDArray

class FuncionesLeer:

    def __init__(self):
        print('FuncionesLeer constructor')
        
    # función para cortar lo nombres de LET
    def fileNameDropLET(self, iFileName) -> str:
        fileName: str
        fileName = os.path.basename(iFileName) # Tengo que cortarlo para buscar los archivos que cominezan igual
        firstParethesisPos: int
        firstParethesisPos= fileName.index('(')  #·busco la primera aparición de el paréntesis
        charDrop: int
        charDrop = len(fileName)-firstParethesisPos # calculo el número de caracteres que quiero eliminar
        fileName = fileName[:-charDrop]
        return fileName


    # Función para comprobar si el path existe
    def check_path(self, path: str) -> bool:
        if not os.path.exists(os.path.dirname(path)):
            raise IOError(2,'Path does not exist. ')
        else:
            return True

    # Función para abrir el archivo de datos
    def open_iFile(self, fileName: str) -> _io.TextIOWrapper:
        # Abro el fichero de datos
        #msg: str
        iFile: _io.TextIOWrapper 
        try:
            iFile = open(fileName, "r") # abro el input file
        except IOError as err:
            #msg = str(err.strerror)
            raise OSError(2,'Input file does not exist. ')
            #return msg, False
        else:
            return iFile

    # Función para cerrar el archivo de datos
    def close_iFile(self, iFile: _io.TextIOWrapper) -> bool:
        iFile.close() # Cuando acabo de leer el fichero, lo cierro
        if iFile.closed == False:
            print("Error closing file!")
            return False
        else:
            print("File closed!")
            return True

    def leer_de_IN5(self, iFile: _io.TextIOWrapper, qvalue: list[float], energy: list[list[float]], scatInt: list[list[float]], err: list[list[float]]) -> tuple:
        line: str # Para leer el fichero línea a línea
        elements: list[str] # Para guardar los elemento de una línea en una lista
        numq: int # es el contador que voy a usar para cambiar de Q 
        numq = 0 # Pongo el contador de Q a cero

        for line in iFile.readlines():
            elements = line.split() # Divido la línea en elementos
            if (len(elements) != 0): # Cuento cuantos elementos (columnas) hay en la línea
                if (len(elements) == 6): # Para IN5, si son 6, el primer elemento es la Q
                    qvalue.append(float(elements[0])) # añado la Q a la lista correspondiente
                    energy.append([]) # añado una lista vacía a E, S(Q,E) y err
                    scatInt.append([]) 
                    err.append([])
                    numq = numq + 1 # Sumo uno al contador de Q
                if (len(elements) == 3): # Si tengo 3 elementos en la línea, son E, S(Q, E) y err
                    if (float(elements[0]) != 0): # hay una linea chunga que no sé que es y empieza por 0
                        energy[numq-1].append(float(elements[0])) # Añado los valores a la lista correspondiente
                        scatInt[numq-1].append(float(elements[1]))
                        err[numq-1].append(float(elements[2]))
        return qvalue, energy, scatInt, err

    def leer_de_IN16B(self, iFile: _io.TextIOWrapper, qvalue: list[float], energy: list[list[float]], scatInt: list[list[float]], err: list[list[float]]) -> tuple:
        line: str # Para leer el fichero línea a línea
        elements: list[str] # Para guardar los elemento de una línea en una lista
        numq: int # es el contador que voy a usar para cambiar de Q 
        numq = 0 # Pongo el contador de Q a cero

        for line in iFile.readlines():
            elements = line.split() # Divido la línea en elementos
            if (len(elements) != 0): # Cuento cuantos elementos (columnas) hay en la línea
                if (elements[0]=="#" and elements[1] == "q(Angstrom^-1)"): # Para IN16B, busco la Q
                    qvalue.append(float(elements[3])) # añado la Q a la lista correspondiente
                    energy.append([]) # añado una lista vacía a E, S(Q,E) y err
                    scatInt.append([]) 
                    err.append([])
                    numq = numq + 1 # Sumo uno al contador de Q
                if (elements[0] != "#"): # Si hay elementos y no empiezan por #, son los datos
                    energy[numq-1].append(float(elements[0])) # Añado los valores a la lista correspondiente
                    scatInt[numq-1].append(float(elements[1]))
                    err[numq-1].append(float(elements[2]))
        return qvalue, energy, scatInt, err

    def leer_de_LET(self, iFileName: str) -> tuple:
        qvalue: list[float]
        energy: list[list[float]]
        scatInt: list[list[float]]
        err: list[list[float]]
        qvalue = []
        energy = []
        scatInt = []
        err = []

        line: str # Para leer el fichero línea a línea
        elements: list[str] # Para guardar los elemento de una línea en una lista
        qlist: list[str] # Para guardar el string de la linea donde está el intervalo de Q
        qmin: float # la Q minima del intervalo
        qmax: float # la Q maxima del intervalo
        qcurr: float # la Q corespondiente al fichero q está leyendo
        numq: int # es el contador que voy a usar para cambiar de Q 
        numq = 0 # Pongo el contador de Q a cero
        # Lo primero que tengo que hacer es buscar los ficheros que me interesan en la carpeta
        filenames: list[str] # la lista de todos los archivos en la carpeta
        dirs: list[str] # la lista de subdirectorios en la carpeta
        root: str # me imagino que el path?
        f: str
        files: list[str] # Donde guardo los nombres de los archivos que a mi me interesan
        files = []
        path: str
        path = os.path.dirname(iFileName)
        fileName = self.fileNameDropLET(iFileName)
        for (root, dirs, filenames) in os.walk(path):
            for f in filenames:
                if fileName in f and '.txt' in f:
                    files.append(f)

        iFile: _io.TextIOWrapper
        #msg: str
        for f in files:
            try:
                iFile = self.open_iFile(path + '/' + f)
            except IOError as error:
                pass #pongo algo más? qué quiero que haga si no consigue abrir un fichero?
            else:
                for line in iFile.readlines():
                    elements = line.split() # Divido la línea en elementos
                    if (len(elements) != 0): # Cuento cuantos elementos (columnas) hay en la línea
                        if (elements[1]=="Integration"): # Para LET la Q está en la línea que empieza así (# Integration axis:)
                            qlist = elements[3].split(",")
                            qmin = float(qlist[1])
                            qmax = float(qlist[2])
                            qcurr = qmin + (qmax - qmin) /2
                            qvalue.append(qcurr)# añado la Q a la lista correspondiente
                            energy.append([]) # añado una lista vacía a E, S(Q,E) y err
                            scatInt.append([]) 
                            err.append([])
                            numq = numq + 1 # Sumo uno al contador de Q
                        if (elements[0] != "#"): # Si hay elementos y no empiezan por #, son los datos
                            energy[numq-1].append(float(elements[0])) # Añado los valores a la lista correspondiente
                            scatInt[numq-1].append(float(elements[1]))
                            err[numq-1].append(float(elements[2]))
                self.close_iFile(iFile)
        return qvalue, energy, scatInt, err

    def leer_de_FOCUS(self, iFile: _io.TextIOWrapper, qvalue: list[float], energy: list[list[float]], scatInt: list[list[float]], err: list[list[float]]) -> tuple:
        line: str # Para leer el fichero línea a línea
        elements: list[str] # Para guardar los elemento de una línea en una lista
        numq: int # es el contador que voy a usar para cambiar de Q 
        numq = 0 # Pongo el contador de Q a cero

        for line in iFile.readlines():
            elements = line.split() # Divido la línea en elementos
            if (len(elements) != 0): # Cuento cuantos elementos (columnas) hay en la línea
                if (elements[0]=="#Group" and elements[1]=="Value:"): # Para FOCUS la Q está en la línea que empieza así
                    qvalue.append(float(elements[2])) # añado la Q a la lista correspondiente
                    energy.append([]) # añado una lista vacía a E, S(Q,E) y err
                    scatInt.append([]) 
                    err.append([])
                    numq = numq + 1 # Sumo uno al contador de Q
                if (elements[0][0] != "#"): # Si hay elementos y no empiezan por #, son los datos
                    energy[numq-1].append(float(elements[0])) # Añado los valores a la lista correspondiente
                    scatInt[numq-1].append(float(elements[1]))
                    err[numq-1].append(float(elements[2]))
        return qvalue, energy, scatInt, err

    # Función para leer del archivo de datos y guardarlos en listas
    # Uso esta función para leer de todos los tipos de archivo (excepto LET): como variable de entrada tiene el instrumento y dentro tiene que tener un match case
    def read_from_ifile(self, iFile: _io.TextIOWrapper, instrument: str) -> tuple:

        qvalue: list[float] # Para guardar los valores de Q
        energy: list[list[float]] # Para guardar la energía dispersada
        scatInt: list[list[float]] # Para guardar S(Q,E)
        err: list[list[float]] # Para guardar el error experimental en S(Q,E)

        # Inicializo las variables a listas vacías
        qvalue = []
        energy = []
        scatInt = []
        err = []

        match instrument:
            case "IN5":
                qvalue, energy, scatInt, err = self.leer_de_IN5(iFile, qvalue, energy, scatInt, err)
            case "IN16B":
                qvalue, energy, scatInt, err = self.leer_de_IN16B(iFile, qvalue, energy, scatInt, err)
            case "FOCUS":
                qvalue, energy, scatInt, err = self.leer_de_FOCUS(iFile, qvalue, energy, scatInt, err)

        return qvalue, energy, scatInt, err

    # Función para guardar los datos de S(Q,E) en un DataFrame de Pandas
    def data_to_pandas_df(self, fileName: str, qvalue: list[float], energy: list[list[float]], scatInt: list[list[float]], err: list[list[float]]) -> pd.DataFrame:

        dfS: pd.DataFrame # Data frame para guardar S(Q,E)
        dfS = pd.DataFrame() 
        energyS: pd.Series # declaro estas series porque para que las columnas tengan el mismo nombre tengo que usar concat
        scatIntS: pd.Series
        errS: pd.Series

        i: int # El contador para iterar
        q: float # Para recorrer qvalue
        scatIntLabel: str # Para escribir el nombre de las columnas
        qstr:str

        for i, q in enumerate(qvalue):
            energyS = pd.Series(energy[i], name = "E (meV)")
            qstr = "_" + str(qvalue[i]) + "A-1"
            scatIntLabel = os.path.basename(fileName)[:-4] + qstr
            scatIntS = pd.Series(scatInt[i], name = scatIntLabel)
            errS = pd.Series(err[i], name = "err")
            errS = errS.replace(-1, 0) # En IN5 a veces hay valores negativos del error. Los comvierto a ceros
            dfS = pd.concat([dfS, energyS, scatIntS, errS], axis = 1, names = [energyS.name, scatIntS.name, errS.name])

        return dfS

    # Hago una función para calcular la susceptibilidad a partir de el DataFrame de S(Q,E)
    def chi_from_S(self, temp: float, qvalue: list[float], dfS: pd.DataFrame)-> pd.DataFrame:
        # Quiero probar a guardar la susceptibilidad en E+ Chi+ E- Chi-, para cada Q.
        energyM: pd.Series # Creo unas series para meter las energías negativas
        energyP: pd.Series # y positivas
        chiSM: pd.Series # Creo unas series para guardar las susceptibilidades calculadas para E<0
        chiSP: pd.Series # y E>0
        kb: float # 8.617333262 × 10-5 eV K-1
        kb = 8.6173332e-5
        factSusS: pd.Series # Creo una serie con el factor por el que hay que multiplicar
        dfchiM: pd.DataFrame # En este data frame guardo los pares E Chi para E<0
        dfchiSorted: pd.DataFrame # En este data frame guardo las susceptivilidades
        dfchiSorted = pd.DataFrame()

        for i, q in enumerate(qvalue):
            energyM = dfS[dfS.iloc[:,3*i]<0].iloc[:,3*i] # Guardo las E<0 para una Q
            energyM.name = 'E- (meV)'
            factSusS = np.pi*(np.exp(energyM.abs()/kb/1000/temp) - 1)
            chiSM = factSusS*dfS[dfS.iloc[:,3*i]<0].iloc[:,3*i+1]
            chiSM.name = dfS.iloc[:,3*i+1].name
            energyM = energyM.abs()
            dfchiM = pd.concat([energyM, chiSM], axis = 1)
            dfchiM.sort_values(energyM.name, ascending = True, inplace = True)
            dfchiM.reset_index(drop = True, inplace = True)

            energyP = dfS[dfS.iloc[:, 3*i]>0].iloc[:, 3*i] # Guardo las E>0 para una Q
            energyP.name = 'E+ (meV)'
            factSusS = np.pi*(1 - np.exp(-energyP/kb/1000/temp))
            chiSP = factSusS*dfS[dfS.iloc[:, 3*i]>0].iloc[:, 3*i+1]
            chiSP.name =  dfS.iloc[:,3*i+1].name
            dfchiP = pd.concat([energyP, chiSP], axis = 1)
            dfchiP.reset_index(drop = True, inplace = True)

            dfchiSorted = pd.concat([dfchiSorted ,dfchiM, dfchiP], axis = 1)
            del dfchiM, dfchiP # Borro los data frames antes de que cambie de Q

        return dfchiSorted

    # Hago una función para guardar los datos en CSV
    def save_data_to_csv(self, oFileName: str, dfS: pd.DataFrame) -> bool:
        thresholdVal: int
        # Cuando guardo, quito todas las filas con NAN solamente si en todas las columnas hay NANs
        # thres es el número mínimo de no-NAN para que no se haga drop: Keep only the rows with at least 'Thres' non-NA values.
        thresholdVal = int(len(dfS.columns)/3+1) # Todas las E son no-NAN. Si hay una columna más con no-NAN, no se hace drop.
        dfS.dropna(axis = 0, thresh = thresholdVal, inplace=True)
        dfS.to_csv(oFileName, sep = '\t', index = False)
        #print("Data succesfully exported to CSV!")
        #print(oFileName)

        return True
    
    def save_chi_data_to_csv(self, oFileName: str, dfchiSorted: pd.DataFrame) -> bool: #dfS: pd.DataFrame, 
        thresholdVal: int
        # Cuando guardo, quito todas las filas con NAN solamente si en todas las columnas hay NANs
        # thres es el número mínimo de no-NAN para que no se haga drop: Keep only the rows with at least 'Thres' non-NA values.
        thresholdVal = int(len(dfchiSorted.columns)/4+1) # En este caso, como la E no es simetrica respecto a cero, solo tengo no-NAN para las columnas E-. Si hay una columna más con no-NAN, no se hace drop
        dfchiSorted.dropna(thresh = thresholdVal, inplace=True)
        dfchiSorted.to_csv(oFileName.replace('.csv','_Chi.csv'), sep = '\t', index = False)
        #print("Data succesfully exported to CSV!")
        #print(oFileName)

        return True
