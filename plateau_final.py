from decimal import Decimal, ROUND_HALF_EVEN
import signal
import threading
from turtle import bk
import pandas as pd
import os
from os import listdir, stat
from os.path import isfile, join
import sys
import re
import time
from typing import List
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threading import *
from attr import NOTHING
import numpy as np
from time import sleep

back_color = '#008375'
user = os.getlogin()

class Plateau(QWidget):
    def __init__(self, parent = None):
      super(Plateau, self).__init__(parent)
      layMain = QVBoxLayout()
      grdLayMain = QGridLayout()
      self.cmb = QComboBox()
      self.SRDPath = '//ohclea01psge/apps/Mfgtestapps/SRD Test Data'
      pixLogo = QPixmap('//twnpres01/shrdata/Calibration/Iconography/imgTitle.png')
      lblLogo = QLabel()
            
      lblLogo.setPixmap(pixLogo)
      layMain.addWidget(lblLogo)
      self.btnRun = QPushButton('Run Output')
      self.btnRun.setFixedWidth(75)
      self.btnRun.clicked.connect(self.BackPlatESSVerification)
      grpSetup = self.Setup()
      grpPlatEval = self.PlatEval()
      grpOutput = self.Output()
      grdLayMain.addWidget(grpSetup,0,0)
      grdLayMain.addWidget(grpPlatEval,1,0)
      grdLayMain.addWidget(self.btnRun,2,0,alignment=Qt.AlignCenter)
      grdLayMain.addWidget(grpOutput,3,0)
      layMain.addLayout(grdLayMain)
      layMain.addStretch()
      self.setLayout(layMain)
    
    def Setup(self):
        grpSetup = QGroupBox('Path Setup')
        self.btnOutputFolder = QPushButton('Output Folder')
        self.btnOutputFolder.setFixedWidth(125)
        self.btnOutputFolder.clicked.connect(lambda:self.FindFiles(self.btnOutputFolder))
        # //ohclea01psge/apps/Mfgtestapps/SRD Test Data/SOT-LOT PLT and ESS data analysis
        self.txtOutputFolder = QLineEdit('//ohclea01psge/apps/Mfgtestapps/SRD Test Data/SOT-LOT PLT and ESS data analysis')
        self.txtOutputFolder.setFixedWidth(500)
        self.txtOutputFolder.setDisabled(True)
        self.btnBackFolder = QPushButton('Background Folder')
        self.btnBackFolder.setFixedWidth(125)
        self.btnBackFolder.clicked.connect(lambda:self.FindFiles(self.btnBackFolder))
        # //ohclea01psge/apps/Mfgtestapps/SRD Test Data/0754-501-B/Plateau Test
        self.txtBackFolder = QLineEdit('//ohclea01psge/apps/Mfgtestapps/SRD Test Data/0754-501-B/Plateau Test')
        self.txtBackFolder.setFixedWidth(500)
        self.txtBackFolder.setDisabled(True)
        self.btnPlatFolder = QPushButton('Plateau Folder')
        self.btnPlatFolder.setFixedWidth(125)
        self.btnPlatFolder.clicked.connect(lambda:self.FindFiles(self.btnPlatFolder))
        # //ohclea01psge/apps/Mfgtestapps/SRD Test Data/0754-501/Plateau Test
        self.txtPlatFolder = QLineEdit('//ohclea01psge/apps/Mfgtestapps/SRD Test Data/0754-501/Plateau Test')
        self.txtPlatFolder.setFixedWidth(500)
        self.txtPlatFolder.setDisabled(True)
        self.btnESSFolder = QPushButton('ESS Folder')
        self.btnESSFolder.setFixedWidth(125)
        self.btnESSFolder.clicked.connect(lambda:self.FindFiles(self.btnESSFolder))
        # //ohclea01psge/apps/Mfgtestapps/SRD Test Data/0754-501/ESS Test
        self.txtESSFolder = QLineEdit('//ohclea01psge/apps/Mfgtestapps/SRD Test Data/0754-501/ESS Test')
        self.txtESSFolder.setFixedWidth(500)
        self.txtESSFolder.setDisabled(True)
        lblFileTime = QLabel('File Time (days)')
        lblFileTime.setToolTip('Determines How Far Back In Time To Retrieve Files')
        self.txtFileTime = QLineEdit('2')
        self.txtFileTime.setFixedWidth(45)
        self.txtFileTime.setToolTip('Determines How Far Back In Time To Retrieve Files')
        self.btnAuto = QPushButton('Auto')
        self.btnAuto.setFixedWidth(75)
        self.btnAuto.clicked.connect(lambda:self.AutoManual(self.btnAuto))
        self.btnGo = QPushButton('Get Files!')
        self.btnGo.setFixedWidth(75)
        self.btnGo.clicked.connect(self.PathVerification)
        vlaySetup = QVBoxLayout()
        hlayOutputFolder = QHBoxLayout()
        hlayBackFolder = QHBoxLayout()
        hlayPlatFolder = QHBoxLayout()
        hlayESSFolder = QHBoxLayout()
        hlayFileTime = QHBoxLayout()
        hlayAuto = QHBoxLayout()
        hlayGo = QHBoxLayout()
        hlayOutputFolder.addWidget(self.btnOutputFolder)
        hlayOutputFolder.addWidget(self.txtOutputFolder)
        hlayOutputFolder.addStretch()
        hlayBackFolder.addWidget(self.btnBackFolder)
        hlayBackFolder.addWidget(self.txtBackFolder)
        hlayBackFolder.addStretch()
        hlayPlatFolder.addWidget(self.btnPlatFolder)
        hlayPlatFolder.addWidget(self.txtPlatFolder)
        hlayPlatFolder.addStretch()
        hlayESSFolder.addWidget(self.btnESSFolder)
        hlayESSFolder.addWidget(self.txtESSFolder)
        hlayESSFolder.addStretch()
        hlayFileTime.addWidget(lblFileTime)
        hlayFileTime.addWidget(self.txtFileTime)
        hlayFileTime.addStretch()
        hlayAuto.addWidget(self.btnAuto)
        hlayAuto.addStretch()
        hlayGo.addWidget(self.btnGo)
        hlayGo.addStretch()
        vlaySetup.setAlignment(Qt.AlignLeft)
        hlayOutputFolder.setAlignment(Qt.AlignLeft)
        hlayBackFolder.setAlignment(Qt.AlignLeft)
        hlayPlatFolder.setAlignment(Qt.AlignLeft)
        hlayESSFolder.setAlignment(Qt.AlignLeft)
        hlayFileTime.setAlignment(Qt.AlignLeft)
        hlayGo.setAlignment(Qt.AlignLeft)
        hlayAuto.setAlignment(Qt.AlignLeft)
        vlaySetup.addLayout(hlayOutputFolder)
        vlaySetup.addLayout(hlayBackFolder)
        vlaySetup.addLayout(hlayPlatFolder)
        vlaySetup.addLayout(hlayESSFolder)
        vlaySetup.addLayout(hlayFileTime)
        vlaySetup.addLayout(hlayAuto)
        vlaySetup.addLayout(hlayGo)
        grpSetup.setLayout(vlaySetup)
        return grpSetup
    
    def PlatEval(self):
        grpPlatEval = QGroupBox('Plateau Evaluation')
        lblBackList = QLabel('Background File List')
        self.lstBackList = QListWidget()
        self.lstBackList.setFixedHeight(300)
        self.lstBackList.setSelectionMode(QAbstractItemView.MultiSelection)
        lblPlatList = QLabel('Plateau File List')
        self.lstPlatList = QListWidget()
        self.lstPlatList.setFixedHeight(300)
        self.lstPlatList.setEnabled(False)
        self.lstPlatList.setSelectionMode(QAbstractItemView.MultiSelection)
        lblESSList = QLabel('ESS File List')
        self.lstESSList = QListWidget()
        self.lstESSList.setFixedHeight(300)
        self.lstESSList.setEnabled(False)
        self.lstESSList.setSelectionMode(QAbstractItemView.MultiSelection)
        hlayPlatEval = QHBoxLayout()
        vlayBackList = QVBoxLayout()
        vlayPlatList = QVBoxLayout()
        vlayESSList = QVBoxLayout()
        hlayPlatEval.setAlignment(Qt.AlignLeft)
        vlayBackList.setAlignment(Qt.AlignLeft)
        vlayPlatList.setAlignment(Qt.AlignLeft)
        vlayESSList.setAlignment(Qt.AlignLeft)
        vlayBackList.addWidget(lblBackList)
        vlayBackList.addWidget(self.lstBackList)
        vlayPlatList.addWidget(lblPlatList)
        vlayPlatList.addWidget(self.lstPlatList)
        vlayESSList.addWidget(lblESSList)
        vlayESSList.addWidget(self.lstESSList)
        hlayPlatEval.addLayout(vlayBackList)
        hlayPlatEval.addLayout(vlayPlatList)
        hlayPlatEval.addLayout(vlayESSList)
        hlayPlatEval.addStretch()
        grpPlatEval.setLayout(hlayPlatEval)
        return grpPlatEval

    def Output(self):
        grpOutput = QGroupBox('Output')
        self.lstOutput = QListWidget()
        self.lstOutput.setFixedHeight(200)
        self.lstOutput.setFixedWidth(1000)
        hlayOutput = QHBoxLayout()
        hlayOutput.setAlignment(Qt.AlignCenter)
        hlayOutput.addWidget(self.lstOutput)
        grpOutput.setLayout(hlayOutput)
        return grpOutput
    
    def AutoManual(self, v):
        if v.text() == 'Auto':
            self.btnAuto.setText('Manual')
            self.lstPlatList.setEnabled(True)
            self.lstESSList.setEnabled(True)
            self.lstBackList.clear()
            self.lstPlatList.clear()
            self.lstESSList.clear()
        elif v.text() == 'Manual':
            self.btnAuto.setText('Auto')
            self.lstPlatList.setEnabled(False)
            self.lstESSList.setEnabled(False)
            self.lstBackList.clear()
            self.lstPlatList.clear()
            self.lstESSList.clear()
    
    def FindFiles(self, v):
        try:
            days = float(self.txtFileTime.text())
            #options = QFileDialog.Options()
            if v.text() == 'Background Folder':
                folder = QFileDialog.getExistingDirectory(directory=self.SRDPath)
                self.txtBackFolder.setText(folder)
            elif v.text() == 'Plateau Folder':
                folder = QFileDialog.getExistingDirectory(directory=self.SRDPath)
                self.txtPlatFolder.setText(folder)
                    #platFiles = QFileDialog.getOpenFileNames(self,"QFileDialog.getOpenFileNames()", "//ohclea01psge/APPS/Mfgtestapps/SRD Test Data/0754-501/Plateau Test","Excel Files (*.xls)", options=options)
                    #platFileNamesExt = [QFileInfo(f).fileName() for f in platFiles[0]]
                    #platFileNames = [f.split(".",1)[0] for f in platFileNamesExt]
                    #platBackMatch = [f for f in platFiles]
                    #platFiles = [f.split(".",1)[0] for f in listdir(folder) if ((stat(join(folder,f)).st_mtime > time.time() - days*24*3600) & (isfile(join(folder, f)) & f[:2].isdigit()))] #get all the files
            elif v.text() == 'ESS Folder':
                folder = QFileDialog.getExistingDirectory(directory=self.SRDPath)
                self.txtESSFolder.setText(folder)
            elif v.text() == 'Output Folder':
                folder = QFileDialog.getExistingDirectory(directory=os.environ['HOMEPATH'] + '/Documents')
                self.txtOutputFolder.setText(folder)        
        except ValueError as err:
            self.txtFileTime.setText('2')
        except FileNotFoundError as err:
            if v.text() == 'Background Folder':
                self.txtBackFolder.setText()
            elif v.text() == 'Plateau Folder':
                self.txtPlatFolder.setText()
            elif v.text() == 'ESS Folder':
                self.txtESSFolder.setText()
        except TypeError as err:
            if v.text() == 'Background Folder':
                self.txtBackFolder.setText()
            elif v.text() == 'Plateau Folder':
                self.txtPlatFolder.setText()
            elif v.text() == 'ESS Folder':
                self.txtESSFolder.setText()
            
    def PathVerification(self):
        if self.txtOutputFolder.text() != '' and self.txtBackFolder.text() != '' and self.txtPlatFolder.text() != '' and self.txtESSFolder.text() != '':
            self.process1 = threading.Thread(target=self.ProcessOp)
            self.process1.start() 
            
    def BackPlatESSVerification(self):
        if self.lstBackList.currentItem() != None and self.lstPlatList.currentItem() != None and self.lstESSList.currentItem() != None:
            self.process2=Thread(target=self.Analysis(self.lstBackList.selectedItems(), self.lstPlatList.selectedItems(), self.lstESSList.selectedItems()))
            self.process2.start()
        elif self.lstBackList.currentItem() != None and self.btnAuto.text() == 'Auto':
            platList = []
            ESSList = []
            for x in self.lstBackList.selectedItems():
                bname = x.text().split("_",1)[0]
                for y in range(self.lstPlatList.count()):
                    pname = self.lstPlatList.item(y).text().split("_",1)[0]
                    if bname == pname:
                        platList.append(self.lstPlatList.item(y))
                        break
                for z in range(self.lstESSList.count()):
                    ESSname = self.lstESSList.item(z).text().split("_",1)[0]
                    if bname == ESSname:
                        ESSList.append(self.lstESSList.item(z))
                        break
            self.process2=Thread(target=self.Analysis(self.lstBackList.selectedItems(), platList, ESSList))
            self.process2.start()
            
    def ProcessOp(self):
        try:
            days = float(self.txtFileTime.text())
            self.lstBackList.clear()
            self.lstPlatList.clear()
            self.lstESSList.clear()
            if self.btnAuto.text() == 'Auto':
                backFileNames = [f.split(".",1)[0] for f in listdir(self.txtBackFolder.text()) if ((stat(join(self.txtBackFolder.text(),f)).st_mtime > time.time() - days*24*3600) \
                    & (isfile(join(self.txtBackFolder.text(), f)) & f[:2].isdigit()))] #get all the files
                backFileNames.sort(reverse=True)
                self.backLast = []
                lastFile = ''
                for back in backFileNames:
                    bname = back.split("_",1)[0]
                    if lastFile != bname:
                        backFound = [x if re.findall(bname, x) else '' for x in backFileNames]
                        backfile = [x for x in backFound if x]
                        self.backLast.append(backfile[0])
                    lastFile = bname
                self.backLast.sort()
                self.lstBackList.addItems(self.backLast)
                platFiles = listdir(self.txtPlatFolder.text())
                platFileNames = [f.split(".",1)[0] for f in platFiles] 
                platBackMatch = [x for x in platFileNames for y in backFileNames if x.split("_",1)[0] == y.split("_",1)[0]]
                platBackMatch.sort(reverse=True)
                self.platLast = []
                lastFile = ''
                for plat in platBackMatch:
                    pname = plat.split("_",1)[0]
                    if lastFile != pname:
                        platFound = [x if re.findall(pname, x) else '' for x in platBackMatch]
                        platfile = [x for x in platFound if x]
                        self.platLast.append(platfile[0])
                    lastFile = pname
                self.platLast.sort()
                self.lstPlatList.addItems(self.platLast)                      
                ESSFiles = listdir(self.txtESSFolder.text())
                ESSFileNames = [f.split(".",1)[0] for f in ESSFiles]
                ESSBackMatch = [x for x in ESSFileNames for y in backFileNames if x.split("_",1)[0] == y.split("_",1)[0]]
                ESSBackMatch.sort(reverse=True)
                self.ESSLast = []
                lastFile = ''
                for ESS in ESSBackMatch:
                    ename = ESS.split("_",1)[0]
                    if lastFile != ename:
                        ESSFound = [x if re.findall(ename, x) else '' for x in ESSBackMatch]
                        ESSfile = [x for x in ESSFound if x]
                        self.ESSLast.append(ESSfile[0])
                    lastFile = ename
                self.ESSLast.sort()
                self.lstESSList.addItems(self.ESSLast)
            elif self.btnAuto.text() == 'Manual':
                backFileNames = [f.split(".",1)[0] for f in listdir(self.txtBackFolder.text()) if ((stat(join(self.txtBackFolder.text(),f)).st_mtime > time.time() - days*24*3600) \
                    & (isfile(join(self.txtBackFolder.text(), f)) & f[:2].isdigit()))] #get all the files
                backFileNames.sort()
                self.lstBackList.addItems(backFileNames)
                platFiles = listdir(self.txtPlatFolder.text())
                platFileNames = [f.split(".",1)[0] for f in platFiles] 
                platBackMatch = []
                for x in platFileNames:
                    for y in backFileNames:
                        if x.split("_",1)[0] == y.split("_",1)[0]:
                            if x not in platBackMatch:
                                platBackMatch.append(x)
                #platBackMatch.sort()
                self.lstPlatList.addItems(platBackMatch)                      
                ESSFiles = listdir(self.txtESSFolder.text())
                ESSFileNames = [f.split(".",1)[0] for f in ESSFiles]
                ESSBackMatch = []
                for x in ESSFileNames:
                    for y in backFileNames:
                        if x.split("_",1)[0] == y.split("_",1)[0]:
                            if x not in ESSBackMatch:
                                ESSBackMatch.append(x)
                ESSBackMatch.sort()
                self.lstESSList.addItems(ESSBackMatch)
        except ValueError as err:
            self.txtFileTime.setText('2')    
                    
    def Analysis(self, background: List[QListWidgetItem], plateau: List[QListWidgetItem], ESS: List[QListWidgetItem]):
        try:
            if background.__len__ != 0 and plateau.__len__ != 0 and ESS.__len__ != 0:
                for back in background:
                    bname = back.text().split("_",1)[0]
                    for plat in plateau:
                        pname = plat.text().split("_",1)[0]
                        for e in ESS:
                            ename = e.text().split("_",1)[0]
                            if bname == pname and bname == ename:
                                thresh = 1.5 #Threshold to determine where noise edge starts
                                distNoiseEdge = 75. #minimum separation between HV set point and noise edge
                                minHV = 1000. #minimum HV
                                bindex = back.text().split("_",1)[1]
                            
                                timestr = time.strftime("%Y%m%d-%H%M%S")
                                ofilename = f"{self.txtOutputFolder.text()}/{bname}_{timestr}.xlsx"
                                #writer = pd.ExcelWriter(outputfolder + fname+ "_" + ".xlsx",engine='xlsxwriter') #open main output file
                                writer = pd.ExcelWriter(ofilename,engine='xlsxwriter')

                                #create the dummy dictionary so I can create a blank worksheet in the output workbook.
                                dummy = {}
                                dc = pd.DataFrame(dummy)
                                dc.to_excel(writer, sheet_name='Charts')

                                #this should be the most recent file (highest numbered filem plateau data)
                                df = pd.DataFrame(pd.read_excel(self.txtBackFolder.text() + '/' + back.text() + '.xls','Data'))
                                #print(df)
                            
                                #print(df.iloc[7,5]) #PMT SN
                                #print(df.iloc[7,9]) #Plateau Start
                                #print(df.iloc[7,10]) #Plateau End

                                #print(df.iloc[10:48,1:9]) #Table of Plateau Data

                                #TODO: need to change this stuff here if the format of the plateau file ever changes
                                #the following are all in excel cell space, index starts at 1
                                ambientStart = [11,2] #Ambient
                                ambientEnd = [48,2] #End of Ambient Data
                                elevatedStart = [11,3] #Elevated
                                elevatedEnd = [48,3] #End of Elevated Data
                                vStart = [11,5] #HV
                                vEnd = [48,5]

                                voltages = df.iloc[10:48,4] #get this for fitting later
                                elevatedCPS = df.iloc[10:48,2] #get this for fitting later
                                ambientCPS = df.iloc[10:48,1]
                                #workbook = xlsxwriter.Workbook(f+".xlsx")
                                #TODO: all this charting stuff can probably get refactored at some point
                                df.to_excel(writer, sheet_name='BkgPlateauData') #write dataframe to excel file
                                workbook = writer.book
                                worksheet = writer.sheets['BkgPlateauData']
                                #set up and create chart for background platau data
                                cwidth = 600
                                cheight = 400
                                bchart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
                                bchart.set_title({'name': 'Background Plateau: ' + back.text()})
                                bchart.set_y_axis({'name': 'CPS', 'min' : 0, 'max':50})
                                bchart.set_x_axis({'name': 'Voltage', 'min':800,'max':1800})
                                bchart.set_size({'width':cwidth, 'height':cheight})
                                #worksheet = workbook.add_worksheet()
                                #add the ambient and background data to chart        
                                bchart.add_series({'categories' : [worksheet.name]+vStart + vEnd, 'values': [worksheet.name]+ambientStart + ambientEnd, 'name': 'Ambient'})
                                bchart.add_series({'categories' : [worksheet.name]+vStart + vEnd, 'values': [worksheet.name]+elevatedStart + elevatedEnd, 'name': 'Elevated'})
                            
                                chartsheet = writer.sheets['Charts']
                                chartsheet.insert_chart('D1',bchart)
                                #chartsheet.write('A1','Bkg Plateau Status')
                                #chartsheet.write('B1',df.iloc[9,14])
                            
                            
                                #tf = [x if re.findall(fname, x) else '' for x in platList]
                                #platfile = [x for x in tf if x]
                                df = pd.DataFrame(pd.read_excel(self.txtPlatFolder.text() + '/' + plat.text() + '.xls','Data'))
                                df.to_excel(writer, sheet_name='PlateauData') #write dataframe to excel file
                                platPassFail = df.iloc[9,14].upper()
                                #print(df.iloc[9,14])
                                workbook = writer.book
                                worksheet = writer.sheets['PlateauData']
                                chartsheet.write('A2','Plateau Status')
                                chartsheet.write('B2',platPassFail)
                                chartsheet.write('A5','Plateau HV')
                                pHV = df.iloc[8,13]
                                chartsheet.write('B5',pHV)
                                #TODO: this charting stuff could probably get refactored
                                        #set up and create chart for background plateau data
                                pchart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
                                pchart.set_title({'name': 'Plateau: ' + plat.text()})
                                pchart.set_y_axis({'name': 'CPS', 'min' : 0, 'max':800})
                                pchart.set_x_axis({'name': 'Voltage', 'min':800,'max':1800})
                                pchart.set_size({'width':cwidth, 'height':cheight})
                                #worksheet = workbook.add_worksheet()
                                #add the ambient and background data to chart        
                                pchart.add_series({'categories' : [worksheet.name]+vStart + vEnd, 'values': [worksheet.name]+ambientStart + ambientEnd, 'name': 'Ambient'})
                                pchart.add_series({'categories' : [worksheet.name]+vStart + vEnd, 'values': [worksheet.name]+elevatedStart + elevatedEnd, 'name': 'Elevated'})
                            
                                chartsheet = writer.sheets['Charts']
                                chartsheet.insert_chart('D1',pchart,{'x_offset':cwidth+20,'y_offset':0})                                
                                
                                #print('ESS: ' + essfile[0])
                                df = pd.DataFrame(pd.read_excel(self.txtESSFolder.text() + '/' + e.text() + '.xls','Data'))
                                df.to_excel(writer, sheet_name='ESSData') #write dataframe to excel file
                                ESSPassFail1 = df.iloc[3,8].upper()
                                ESSPassFail2 = df.iloc[4,8].upper()
                                chartsheet.write('A3','ESS Status')
                                chartsheet.write('B3',ESSPassFail1 + ', ' + ESSPassFail2)
                                chartsheet.write('A6','ESS Voltage')
                                pHV = df.iloc[5,8]
                                #pHV2 = pHV if pHV >0 and pHV < 5 else pHV*350              
                                chartsheet.write('B6',pHV)
                            
                                essrowcount = len(df.index)
                                essrowcount = (df.iloc[:,0] >0).sum() - 2
                                timestart = [1,1]
                                tempstart = [1,3]
                                countstart = [1,4]
                                movingavgstart = [1,15] 
                                deltastart = [1,16]
                                timeend = [essrowcount,1]
                                tempend = [essrowcount,3]
                                countend = [essrowcount,4]
                                movingavgend = [essrowcount,15] 
                                deltaend = [essrowcount,16]

                                #print(df.iloc[:,1])
                                workbook = writer.book
                                worksheet = writer.sheets['ESSData']
                                #set up and create chart for background plateau data
                                echart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
                                echart.set_title({'name': 'ESS: ' + e.text()})
                                echart.set_y_axis({'name': 'CPS', 'min' : 00, 'max':40})
                                echart.set_x_axis({'name': 'Time'})
                                echart.set_size({'width':cwidth, 'height':cheight})
                                #worksheet = workbook.add_worksheet()
                                #add the ambient and background data to chart        
                                echart.add_series({'categories' : [worksheet.name]+timestart + timeend, 'values': [worksheet.name]+countstart + countend, 'name': 'CPS'})
                                echart.add_series({'categories' : [worksheet.name]+timestart + timeend, 'values': [worksheet.name]+tempstart + tempend, 'name': 'Temperature'})
                                echart.add_series({'categories' : [worksheet.name]+timestart + timeend, 'values': [worksheet.name]+movingavgstart + movingavgend, 'name': 'Moving Average'})
                            
                                chartsheet = writer.sheets['Charts']
                                chartsheet.insert_chart('D1',echart,{'x_offset':0,'y_offset':cheight+20})
                            
                                dchart = workbook.add_chart({'type': 'scatter', 'subtype': 'straight'})
                                dchart.set_title({'name': 'ESS Delta'})
                                dchart.set_y_axis({'name': 'CPS'})
                                dchart.set_x_axis({'name': 'Time'})
                                dchart.set_size({'width':cwidth, 'height':cheight})
                                #worksheet = workbook.add_worksheet()
                                #add the ambient and background data to chart        
                                dchart.add_series({'categories' : [worksheet.name]+timestart + timeend, 'values': [worksheet.name]+deltastart + deltaend, 'name': 'Delta CPS'})
                                        
                                chartsheet = writer.sheets['Charts']
                                chartsheet.insert_chart('D1',dchart,{'x_offset':cwidth+20,'y_offset':cheight+20})
                                #have to wait until here to adjust the chart axes so they coincide with the HV. 
                                #note if HV is <= 5V then multiplies the value by 350 since some plateau voltages are in control voltage not HV. hardcoded repeatedly but too lazy right now to figure out best place to put one definition of the hvsetting
                                pchart.set_x_axis({'name': 'Voltage', 'min':800,'max':1800, 'minor_gridlines':{'visible':True, 'line':{'dash_type':'dash'}}, 'minor_unit':25, 'major_unit':100, 'major_gridlines':{'visible':True,'line':{'color':'red', 'dash_type':'dash'}}, 'crossing':pHV*350 if pHV <= 5 else pHV*1.})
                                bchart.set_x_axis({'name': 'Voltage', 'min':800,'max':1800,'minor_gridlines':{'visible':True, 'line':{'dash_type':'dash'}}, 'minor_unit':25, 'major_unit':100, 'major_gridlines':{'visible':True,'line':{'color':'red', 'dash_type':'dash'}}, 'crossing':pHV*350 if pHV <= 5 else pHV*1.})
                                    
                                hvSetting = pHV*350 if pHV <= 5 else pHV*1. 
                                x = np.array(pd.to_numeric(voltages))
                                y = np.array(pd.to_numeric(elevatedCPS))
                                yamb = np.array(pd.to_numeric(ambientCPS))

                            

                                xf = x[x >= hvSetting - 50.]
                                yf = y[len(y) - len(xf):]
                            
                                yele_test = y[x>=1000]
                                yamb_test = yamb[x>=1000]

                                #check to see if the elevated curve is systematically lower than the ambient curve
                                if sum(yele_test > yamb_test) >0: #sum should = zero if the elevated is lower than ambient

                                    coeffs = np.polyfit(xf, yf, 4) #4th order poly
                                    p = np.poly1d(coeffs);

                                    chi_squared = np.sum((np.polyval(p, x) - y) ** 2)/len(xf)
                                                            #calculate the voltage at which the delta is > thresh
                                    startval = hvSetting
                                    endval = startval
                                    stepSize = 5.
                                    hendval = 1750.
                                    if hvSetting > 1000.:
                                        smeas = y[abs(x - startval) < 1]
                                        #if smeas.size() > 0:
                                        refVal = smeas if smeas > p(startval) else p(startval)
                                        while p(endval) - refVal < thresh: #start from setpoint HV and go up
                                            endval += stepSize
                                        while p(hendval) - refVal > thresh:#start from the high end and work your way down
                                            hendval -=stepSize
                                                                                        #    print(f'{hendval}, {p(hendval)},  {p(hendval) - p(startval)}')

                                                                                        #take the higher of the two noise edge possibilities
                                        fendval = endval if endval > hendval else hendval

                                                                                        #xp = np.linspace(0, 18, 1800)
                                                                                        #plt.ylim(0,100)
                                                                                        #plt.plot(x,y)
                                                                                        #plt.plot(xf,p(xf))

                                                                                        #plt.show()
                                    chartsheet.write('A7','Noise Edge Solutions')
                                    chartsheet.write('B7', f'{endval} or {hendval}')
                                    chartsheet.write('A8','Distance to Higher Noise Edge')
                                    chartsheet.write('B8', fendval - startval)
                                    chartsheet.write('A9',"Chi2/dof")
                                    chartsheet.write('B9',chi_squared)
                                    noiseEdge = 'PASS' if fendval - startval >= distNoiseEdge else 'FAIL'
                                    bkgstatus = 'PASS' if noiseEdge == 'PASS' and platPassFail == 'PASS' and ESSPassFail1 == 'PASS' \
                                        and ESSPassFail2 == 'PASS' else 'FAIL' #require noise edge to be 75V or more away from HV set point.
                                    bkgstatus = bkgstatus if hvSetting > minHV else 'Invalid HV'
                                    bkgstatus = bkgstatus if abs(endval - hendval) < 150 else 'Manual Eval (Did not Converge)' + bkgstatus
                                    #bkgstatus = bkgstatus if chi_squared < 8000000 else 'Manual Eval (Chi-Squared)' + bkgstatus
                                    chartsheet.write('A4','Background Status')
                                    chartsheet.write('B4',bkgstatus)
                                    #print(bkgstatus)
                                    listWidgetItem = QListWidgetItem('[Background: ' + back.text() + '] - ' + bkgstatus.upper() + ' - [Plateau: ' + plat.text() + '] - ' + platPassFail \
                                        + ' - [ESS: ' + e.text() + '] - ' +  ESSPassFail1 + '/' + ESSPassFail2 + ' - [Noise Edge: '+ str(fendval - startval) + '] - ' + noiseEdge)
                                    self.lstOutput.addItem(listWidgetItem)                                    
                                    #else:
                                    #    chartsheet.write('A4','Background Status')
                                    #    chartsheet.write('B4','FAIL - Elevated Below Ambient')
                                    #    listWidgetItem = QListWidgetItem('Background: ' + background.text() + ' Plat: ' + plateau.text() + ' ESS: ' + ESS.text() + ' - ' +  bkgstatus)
                                    #   self.lstOutput.addItem(listWidgetItem)
                                else:
                                    listWidgetItem = QListWidgetItem('[Background: ' + back.text() + '] - ' + bkgstatus.upper() + ' - [Plateau: ' + plat.text() + '] - ' + platPassFail \
                                        + ' - [ESS: ' + e.text() + '] - ' +  ESSPassFail1 + '/' + ESSPassFail2 + ' FAILED - ' + str(yele_test > yamb_test) + ' < 0 NO CONVERGENCE!!!')
                                    self.lstOutput.addItem(listWidgetItem)
                                workbook.close()
            else:
                listWidgetItem = QListWidgetItem(back.text() + ' NO PLATEAU & NO ESS FILE MATCHES!!!')
                self.lstOutput.addItem(listWidgetItem)
            for x in range(self.lstBackList.count()):
                self.lstBackList.item(x).setSelected(False)
            for x in range(self.lstPlatList.count()):
                self.lstPlatList.item(x).setSelected(False)
            for x in range(self.lstESSList.count()):
                self.lstESSList.item(x).setSelected(False)
        except AttributeError as err:    
            print(str(err))
            
    def intVerification(self, v, i: QLineEdit, lower: int, upper: int):
        if int(i.text()) < lower or int(i.text()) > upper:
            return NOTHING
        else:
            return int(i.text())
        
    def floatVerification(self, v, i: QLineEdit, lower: float, upper: float):
        floatNo = '{:.15f}'.format(float(i.text()))
        roundNo = Decimal(floatNo).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN)
        if roundNo < Decimal(lower).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN) or \
            roundNo > Decimal(upper).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN):
            return NOTHING
        else:
            return roundNo
        
    def floatLowPowerVerification(self, v, i: QLineEdit, power: QLineEdit, lower: float, upper: float):
        floatNo = '{:.16f}'.format(float(i.text() + 'e-' + power.text()))
        roundNo = Decimal(floatNo).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN)
        if roundNo < Decimal(lower).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN) or \
            roundNo > Decimal(upper).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN):
            return NOTHING
        else:
            return roundNo
    
    def floatPowerVerification(self, v, i: QLineEdit, power: QLineEdit, lower: float, upper: float):
        print('Number: ' + i.text() + ' E ' + power.text())
        floatNo = '{:.16f}'.format(float(i.text() + 'e' + power.text()))
        roundNo = Decimal(floatNo).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN)
        if roundNo < Decimal(lower).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN) or \
            roundNo > Decimal(upper).quantize(Decimal('.000000000000001'), rounding=ROUND_HALF_EVEN):
            return NOTHING
        else:
            return roundNo
    
    def selectionchange(self,i):
        print('Items in the list are :')
        
        for count in range(self.cb.count()):
            print(self.cmb.itemText(count),' Current index ',i,'selection changed ',self.cmb.currentText())
          
            
class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__(None)
        
        #menus = self.menuBar()
        #options = menus.addMenu('Options')
        self.move(0,0)
        self.mAction = QAction('Manual', self)
        self.mAction.setShortcut('Ctrl+m')
        self.mAction.triggered.connect(self.MProcess)
        #options.addAction(self.mAction)
        self.sAction = QAction('Sweep', self)
        self.sAction.setShortcut('Ctrl+s')
        self.sAction.triggered.connect(self.SProcess)
       # options.addAction(self.sAction)
        
        self.plateau = Plateau()
        #self.sweep = Sweep()
        widget = QWidget()
        self.stackMain = QStackedLayout()
        widget.setLayout(self.stackMain)
        self.stackMain.addWidget(self.plateau)
        #self.stackMain.addWidget(self.sweep)
                
        self.setCentralWidget(widget)
        self.setWindowTitle('Plateau Test Analysis | User: ' + user)
        self.setStyleSheet('background: white')
    
    def MProcess(self):
        self.stackMain.setCurrentIndex(0)
        
    def SProcess(self):
        self.stackMain.setCurrentIndex(1)
		
def main():
   app = QApplication(sys.argv)
   window = MyWindow()
   window.show()
   sys.exit(app.exec_())

if __name__ == '__main__':
    main()