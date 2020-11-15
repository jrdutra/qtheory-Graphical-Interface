#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 28 11:23:49 2020

@author: alang
"""

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog
import sys
import segyio
import matplotlib.pyplot as plt
import numpy as np
from wiggle.wiggle import wiggle
import cs

        
class Ui(QtWidgets.QMainWindow):

    
    def __init__(self, dado=[], percentualSubAmostragem=0.0, nt=0, nr=0, dadoObservado = [], adjointed = [], iava=[], Rop = None, dadoRecuperado = None):
        super(Ui, self).__init__() # Call the inherited classes __init__ method
        uic.loadUi('cs.ui', self) # Load the .ui file

        self.btnArquivo = self.findChild(QtWidgets.QPushButton, 'btnArquivo')
        self.btnArquivo.clicked.connect(self.btnArquivoPressed)
        
        self.btnProcessar = self.findChild(QtWidgets.QPushButton, 'btnProcessar')
        self.btnProcessar.clicked.connect(self.btnProccessarPressed)

        self.btnVisualizarDadoOriginal = self.findChild(QtWidgets.QPushButton, 'btnVisualizarDadoOriginal')
        self.btnVisualizarDadoOriginal.clicked.connect(self.btnVisualizarDadoOriginalPressed)

        self.btnVisualizarDadoObservado = self.findChild(QtWidgets.QPushButton, 'btnVisualizarDadoObservado')
        self.btnVisualizarDadoObservado.clicked.connect(self.btnVisualizarDadoObservadoPressed)

        self.btnInverterFft = self.findChild(QtWidgets.QPushButton, 'btnInverterFft')
        self.btnInverterFft.clicked.connect(self.btnInverterFftPressed)

        self.btnVisualizarDadoRecuperado = self.findChild(QtWidgets.QPushButton, 'btnVisualizarDadoRecuperado')
        self.btnVisualizarDadoRecuperado.clicked.connect(self.btnVisualizarDadoRecuperadoPressed)

        self.txtArquivo = self.findChild(QtWidgets.QLineEdit, 'txtArquivo')       

        self.txtPercentualSubAmostragem = self.findChild(QtWidgets.QLineEdit, 'txtPercentualSubAmostragem')       

        self.txtIava = self.findChild(QtWidgets.QLineEdit, 'TxtIava')       
        
        self.txtNt = self.findChild(QtWidgets.QLineEdit, 'TxtNt')       

        self.txtNr = self.findChild(QtWidgets.QLineEdit, 'TxtNr')               

        self.txtSaida = self.findChild(QtWidgets.QLineEdit, 'TxtSaida')       
        
        self.show() # Show the GUI
         
    def btnArquivoPressed(self):
        options = QFileDialog.Options()
        #options |= QFileDialog.FileType("*.segy")
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","Seg-Y (*.segy);; Seg-Y (*.sgy)", options=options)
        if fileName:
            self.txtArquivo.setText(fileName)
            sgy = segyio.open(self.txtArquivo.text(), ignore_geometry = True)
            Dx = np.array(sgy.trace)
            self.dado = Dx
            [self.nt,self.nr] = self.dado.shape
            self.txtNt.setText(str(self.nt))
            self.txtNr.setText(str(self.nr))
        
    def btnVisualizarArquivoPressed(self):
        self.plot_segy(self.txtArquivo.text())
        
    def btnProccessarPressed(self):
        self.percentualSubAmostragem = float(self.txtPercentualSubAmostragem.text())
        [self.iava, self.nt, self.nr, self.dadoObservado, self.adjoint, self.Rop] = cs.getDadoObservado(self.dado, self.percentualSubAmostragem)
        self.txtIava.setText(str(self.iava.size))

    def btnVisualizarDadoOriginalPressed(self):
        #self.plotar(self.dado,'Dado Original','X','Y')
        self.plotar2(self.dado, self.nt, self.nr)

    def btnVisualizarDadoObservadoPressed(self):
        #self.plotar(self.dadoObservado,'Dado Observado','X','Y')
        self.plotar2(self.dadoObservado, self.nt, self.nr)

    
    def btnInverterFftPressed(self):
        self.dadoRecuperado = cs.inverterComFFT(self.dadoObservado, self.Rop, self.nt, self.nr)
    
    def btnVisualizarDadoRecuperadoPressed(self):
        #self.plotar(self.dadoRecuperado,'Dado Recuperado','X','Y')
        self.plotar2(self.dadoRecuperado, self.nt, self.nr)
        
    def plot_segy(self, file):
        with segyio.open(file, ignore_geometry=True) as f:
            # Get basic attributes
            n_traces = f.tracecount
            twt = f.samples
            data = f.trace.raw[:]
    
        # Plot
        plt.style.use('ggplot')  # Use ggplot styles for all plotting
        vm = np.percentile(data, 99)
        fig = plt.figure(figsize=(18, 8))
        ax = fig.add_subplot(1, 1, 1)
        extent = [1, n_traces, twt[-1], twt[0]]  # define extent
        ax.imshow(data.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto', extent=extent)
        ax.set_xlabel('CDP number')
        ax.set_ylabel('TWT [ms]')
        ax.set_title(f'{file}')
        ax.grid(False)   
    
    def plotar(self, dados, titulo, tituloeixox, tituloeixoy, climmin=100, climmax=100):
        plt.figure()
        plt.imshow(dados, cmap='gray_r', interpolation='nearest', aspect='auto')
        plt.colorbar()
        #plt.clim(climmin,climmax)
        plt.title(titulo)
        plt.xlabel(tituloeixox)
        plt.ylabel(tituloeixoy)
        plt.tight_layout()
        plt.grid(False)

    def plotar2(self, data, nt, nr):
        a=0
        twt=[]
        for i in range(0,160000):
            twt.append(a)
            a=a+4
        plt.style.use('ggplot')  # Use ggplot styles for all plotting
        vm = np.percentile(data, 99)
        fig = plt.figure(figsize=(18, 8))
        ax = fig.add_subplot(1, 1, 1)
        extent = [1, nr, twt[-1], twt[0]]  # define extent
        ax.imshow(data.T, cmap="RdBu", vmin=-vm, vmax=vm, aspect='auto', extent=extent)
        ax.set_xlabel('CDP number')
        ax.set_ylabel('TWT [ms]')
        #ax.set_title(f'{file}')
        ax.grid(False)        
        
    def gerarWiggle(self, dados, titulo, tituloeixox, tituloeixoy):
        plt.figure()
        plt.title(titulo)
        plt.xlabel(tituloeixox)
        plt.ylabel(tituloeixoy)
        wiggle(dados)

np.random.seed(43273289)        
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
sys.exit(app.exec_()) # Start the application

