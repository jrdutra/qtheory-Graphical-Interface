#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 07 11:23:49 2020

@author: jrdutra
"""

from PyQt5 import QtWidgets, uic, QtCore
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QPixmap, QImage
import sys
import numpy as np
import pandas as pd
from pandasmodel import PandasModel
import matplotlib.pyplot as plt
import pyqtgraph as pg
from pyqtgraph import mkPen

from qtheory import stats
from qtheory import multiserver


class Ui(QtWidgets.QMainWindow):
    
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('gui.ui', self)

        #Construcao grafica
        pg.setConfigOption('background', 'w')
        pg.setConfigOption('foreground', 'k')
        
        #----------------------------------
        #Construção do grafico de chegadas
        #----------------------------------
        self.pw = pg.PlotWidget()
        self.pw.addLegend()
        self.pen1 = mkPen(width=2, color='b')
        self.plotChegadasReal = self.pw.plot([], [], pen=self.pen1, name='Real')
        self.pen2 = mkPen(width=2, color='r')
        self.plotChegadasTeorica = self.pw.plot([], [], pen=self.pen2, name='Teórica')
        self.plt = self.pw.getPlotItem()
        self.plt.hideButtons()
        self.plt.setLabels(left='Frequência Relativa (Ocurr/min)', bottom="Ocorrências (Ocurr)")
        #Atribuicao em tela do Grafico de Chegadas
        self.horizontalLayout = self.findChild(QtWidgets.QHBoxLayout, 'horizontalLayout')
        self.horizontalLayout.addWidget(self.pw)

        #----------------------------------
        #Construção do grafico de Partidas
        #----------------------------------
        self.pw2 = pg.PlotWidget()
        self.pw2.addLegend()
        self.pen3 = mkPen(width=2, color=(0, 0, 0))
        self.plotPartidasReal = self.pw2.plot([], [], pen=self.pen3, name='Real')
        self.pen4 = mkPen(width=2, color=(0, 255, 0))
        self.plotPartidasTeorica = self.pw2.plot([], [], pen=self.pen4, name='Teórica')
        self.plt2 = self.pw2.getPlotItem()
        self.plt2.hideButtons()
        self.plt2.setLabels(left='Frequência Relativa (Ocurr/min)', bottom="Ocorrências (Ocurr)")
        #Atribuicao em tela do Grafico de Partidas
        self.horizontalLayout2 = self.findChild(QtWidgets.QHBoxLayout, 'horizontalLayout2')
        self.horizontalLayout2.addWidget(self.pw2)

        #-----------------
        #ITENS DA CHEGADA
        #-----------------
        self.btnChegadas = self.findChild(QtWidgets.QPushButton, 'btnChegadas')
        self.btnChegadas.clicked.connect(self.btnChegadasPressed)

        self.txtArquivoChegadas = self.findChild(QtWidgets.QLineEdit, 'txtArquivoChegadas')
        self.txtArquivoChegadas.setText("/home/jrdutra/JOAO/TCC/QT/chegadas.csv")

        self.txtPontosChegadas = self.findChild(QtWidgets.QLineEdit, 'txtPontosChegadas')
        self.txtPontosChegadas.setText("0;130;220;385;501")

        #Tabela chegadas
        self.tbChegadas = self.findChild(QtWidgets.QTableView, 'tbChegadas')
        
        #combobox modelos chegadas
        self.cbModelos = self.findChild(QtWidgets.QComboBox, 'cbModelos')
        self.cbModelos.addItem("poisson")
        self.cbModelos.addItem("exponential")
        self.cbModelos.addItem("exponentialnorm")

        #combobox colunas arquivo chegadas
        self.cbColunasChegadas = self.findChild(QtWidgets.QComboBox, 'cbColunasChegadas')

        #Botao Executar chegadas
        self.btnExecChegadas = self.findChild(QtWidgets.QPushButton, 'btnExecChegadas')
        self.btnExecChegadas.clicked.connect(self.btnExecChegadasPressed)

        #-----------------
        #ITENS DA PARTIDA
        #-----------------
        self.btnPartidas = self.findChild(QtWidgets.QPushButton, 'btnPartidas')
        self.btnPartidas.clicked.connect(self.btnPartidasPressed)

        self.txtArquivoPartidas = self.findChild(QtWidgets.QLineEdit, 'txtArquivoPartidas')
        self.txtArquivoPartidas.setText("/home/jrdutra/JOAO/TCC/QT/partidas.csv")

        self.txtPontosPartidas = self.findChild(QtWidgets.QLineEdit, 'txtPontosPartidas')
        self.txtPontosPartidas.setText("0;121;207;255;461")

        #combobox colunas arquivo chegadas
        self.cbColunasPartidas = self.findChild(QtWidgets.QComboBox, 'cbColunasPartidas')

        #Tabela chegadas
        self.tbPartidas = self.findChild(QtWidgets.QTableView, 'tbPartidas')

        #combobox modelos Partidas
        self.cbModelosP = self.findChild(QtWidgets.QComboBox, 'cbModelosP')
        self.cbModelosP.addItem("poisson")
        self.cbModelosP.addItem("exponential")
        self.cbModelosP.addItem("exponentialnorm")

        #Botao Executar Partidas
        self.btnExecPartidas = self.findChild(QtWidgets.QPushButton, 'btnExecPartidas')
        self.btnExecPartidas.clicked.connect(self.btnExecPartidasPressed)

        #botao executa parametros
        self.btnExecParametros = self.findChild(QtWidgets.QPushButton, 'btnExecParametros')
        self.btnExecParametros.clicked.connect(self.btnExecParametrosPressed)

        #n maximo
        self.spNMax = self.findChild(QtWidgets.QSpinBox, 'spNMax')

        #n servidores
        self.spNServidores = self.findChild(QtWidgets.QSpinBox, 'spNServidores')
        self.spNServidores.setMinimum(2)

        #tree
        self.arvore = self.findChild(QtWidgets.QTreeWidget, 'arvore')
        self.arvore.setHeaderLabels(['Parâmetro', 'Valor'])
        self.arvore.setAlternatingRowColors(True)

        self.show() # Show the GUI

    def btnExecParametrosPressed(self):
        try:
            self.arvore.clear()

            h = QtWidgets.QTreeWidgetItem(['Probabilidades', ''])

            c = self.spNServidores.value()

            arrival_times = self.getArrivalTimes()

            pontos = self.txtPontosChegadas.text()
            index_period_beginning_arrival = list(map(int, pontos.split(";")))

            leave_times = self.getLeaveTimes()

            pontos = self.txtPontosPartidas.text()
            index_period_beginning_leave = list(map(int, pontos.split(";")))

            #calcula p0
            ans = multiserver.p0(c, arrival_times, index_period_beginning_arrival, leave_times, index_period_beginning_leave)

            ans = round(ans*100,4)
            strAns = "%.2f" % ans

            #adiciona p0 a arvore
            h.addChild(QtWidgets.QTreeWidgetItem(['p0', strAns + "%"]))

            nMax = self.spNMax.value()

            for n in range(1,nMax+1):
                ans = multiserver.pn(n, c, arrival_times, index_period_beginning_arrival, leave_times, index_period_beginning_leave)
                ans = round(ans*100,4)
                strAns = "%.2f" % ans
                h.addChild(QtWidgets.QTreeWidgetItem(['p'+str(n), strAns + "%"]))
            
            l = QtWidgets.QTreeWidgetItem(['L', ''])

            ans = multiserver.lq(c, arrival_times, index_period_beginning_arrival, leave_times, index_period_beginning_leave)
            ans = round(ans,3)
            strAns = "%.2f" % ans

            l.addChild(QtWidgets.QTreeWidgetItem(['Lq', strAns]))

            ans = multiserver.ls(c, arrival_times, index_period_beginning_arrival, leave_times, index_period_beginning_leave)
            ans = round(ans,3)
            strAns = "%.2f" % ans

            l.addChild(QtWidgets.QTreeWidgetItem(['Ls', strAns]))

            w = QtWidgets.QTreeWidgetItem(['W', ''])

            ans = multiserver.wq(c, arrival_times, index_period_beginning_arrival, leave_times, index_period_beginning_leave)
            ans = round(ans,3)
            strAns = "%.2f" % ans

            w.addChild(QtWidgets.QTreeWidgetItem(['Wq', strAns]))

            ans = multiserver.ws(c, arrival_times, index_period_beginning_arrival, leave_times, index_period_beginning_leave)
            ans = round(ans,3)
            strAns = "%.2f" % ans

            w.addChild(QtWidgets.QTreeWidgetItem(['Ws', strAns]))

            t = QtWidgets.QTreeWidgetItem(['Taxas', ''])

            mlambda = stats.rate(arrival_times, index_period_beginning_arrival)
            strAns = "%.2f" % mlambda
            t.addChild(QtWidgets.QTreeWidgetItem(['λ', strAns]))

            mu = stats.rate(leave_times, index_period_beginning_leave)
            strAns = "%.2f" % mu
            t.addChild(QtWidgets.QTreeWidgetItem(['μ', strAns]))

            self.arvore.addTopLevelItem(h)
            self.arvore.addTopLevelItem(l)
            self.arvore.addTopLevelItem(w)
            self.arvore.addTopLevelItem(t)
            self.arvore.expandAll()
        except ValueError as err:
            print("Houve algum erro:")
            print(err.args)

    def btnChegadasPressed(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "csv (*.csv)", options=options)
        if fileName:
            self.txtArquivoChegadas.setText(fileName)
        arrivalFile = self.txtArquivoChegadas.text()
        datafile = open(arrivalFile)
        df = pd.read_csv(datafile)
        self.cbColunasChegadas.clear()
        for col in df.columns: 
            self.cbColunasChegadas.addItem(col)
    
    def btnPartidasPressed(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "", "csv (*.csv)", options=options)
        if fileName:
            self.txtArquivoPartidas.setText(fileName)
        leaveFile = self.txtArquivoPartidas.text()
        datafile = open(leaveFile)
        df = pd.read_csv(datafile)
        self.cbColunasPartidas.clear()
        for col in df.columns: 
            self.cbColunasPartidas.addItem(col)

    def btnExecChegadasPressed(self):
        try:
            modelo = self.cbModelos.currentText()
  
            arrival_times = self.getArrivalTimes()
            
            pontos = self.txtPontosChegadas.text()
            index_period_beginning_arrival = list(map(int, pontos.split(";")))
            
            ans = stats.real_theoretical_comparation(arrival_times, index_period_beginning_arrival, modelo)
            model = self.dicionarioToPdDataFrame(ans)
            self.tbChegadas.setModel(model)
            #Seta dados do grafico
            x,y,y2 = ans['ocurrence'],ans['real_relative_frequency'],ans['theoretical_relative_frequency']
            self.plotChegadasReal.setData(x, y)
            self.plotChegadasTeorica.setData(x, y2)
        except:
            print("Houve algum erro")
        
    def btnExecPartidasPressed(self):
        try:
            modelo = self.cbModelosP.currentText()
            leave_times = self.getLeaveTimes()

            pontos = self.txtPontosPartidas.text()
            index_period_beginning_leave = list(map(int, pontos.split(";")))

            ans = stats.real_theoretical_comparation(leave_times, index_period_beginning_leave, modelo)
            model = self.dicionarioToPdDataFrame(ans)
            self.tbPartidas.setModel(model)
            #Seta dados do grafico
            x,y,y2 = ans['ocurrence'],ans['real_relative_frequency'],ans['theoretical_relative_frequency']
            self.plotPartidasReal.setData(x, y)
            self.plotPartidasTeorica.setData(x, y2)
        except:
            print("Houve algum erro")

    def dicionarioToPdDataFrame(self, ans):
        obj = ans
        df = pd.DataFrame(data=obj)
        df = df.round(5)
        df = df.rename(columns={"ocurrence": "Ocorrencia", 
                                "frequency": "Frequência (F)", 
                                "real_relative_frequency": "FR Real", 
                                "theoretical_relative_frequency": "FR Teórica"})
        model = PandasModel(df)
        return model
    
    def getArrivalTimes(self):
        colunaChegadas = self.cbColunasChegadas.currentText()
        arrivalFile = self.txtArquivoChegadas.text()
        datafile = open(arrivalFile)
        df = pd.read_csv(datafile)
        arrival_times = df[colunaChegadas].values
        return arrival_times
    
    def getLeaveTimes(self):
        colunaPartidas = self.cbColunasPartidas.currentText()
        leaveFile = self.txtArquivoPartidas.text()
        datafile = open(leaveFile)
        df = pd.read_csv(datafile)
        leave_times = df[colunaPartidas].values
        return leave_times

      
app = QtWidgets.QApplication(sys.argv) # Create an instance of QtWidgets.QApplication
window = Ui() # Create an instance of our class
sys.exit(app.exec_()) # Start the application


