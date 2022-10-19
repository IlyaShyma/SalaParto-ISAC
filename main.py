# BASE IMPORT
import sys
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from ui_main import Ui_MainWindow
import pendulum as plm
import modbus_tk.modbus
import modbus_tk.defines as cst
import modbus_tk.modbus_rtu as modbus_rtu
import serial
import time as t
from tinydb import TinyDB, Query, where
from tinydb.table import Document
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware
import xlsxwriter
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import (
          FigureCanvas, NavigationToolbar2QT as NavigationToolbar)

from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar



import numpy as np

# FUNCTIONS IMPORT
from UIFunctions import *
from SWFunctions import *
from COMFunctions import *
from TRFunctions import *
# from COMFunctions import *


# MAIN CLASS
class MainWindow(QMainWindow):

    # MAIN ROUTINE
    def __init__(self):

        # WINDOW LOAD
        QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.show()
        comUI = self.ui

        # LOAD INITIAL FUNCTIONS
        plm.set_locale('it')
        UIFunctions.defineUI(self)
        UIFunctions.loadCurveUI(self)
        #
        SWFunctions.loadDB(self)
        SWFunctions.loadSow(self)
        SWFunctions.loadSowInBox(self)
        SWFunctions.loadCurve(self)
        SWFunctions.loadTime(self)
        SWFunctions.loadBox(self)
        SWFunctions.loadAddSowInBox(self)
        SWFunctions.loadConf(self)
        # # TMFunctions.setCom(self)
        # # TMFunctions.showDateTime(self)
        SWFunctions.loadHall(self)
        UIFunctions.sowGraph(self)
        #COMFunctions.startCom(self)
        #TMFunctions.singleShotLoadRation(self)

        # RATION FUNCTIONS
        # self.com = COMClass(comUI, self)
        # self.com.start()


        # DATE TIME FUNCTIONS
        self.timer = QTimer(self)
        self.timer.timeout.connect(lambda: SWFunctions.updateTime(self))
        self.timer.start(1000)
        self.com = COMClass(comUI, self)

        # LOAD BUTTONS AND PAGES
        self.ui.comLanguage.currentTextChanged.connect(lambda: TRFunctions.updLanguage(self))
        self.ui.btnHall.pressed.connect(lambda: (self.ui.stackedWidget.setCurrentIndex(1), SWFunctions.loadHall(self)))
        self.ui.btnCurve.pressed.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        self.ui.btnTime.pressed.connect(lambda: self.ui.stackedWidget.setCurrentIndex(3))
        self.ui.btnStock.pressed.connect(lambda: self.ui.stackedWidget.setCurrentIndex(4))
        self.ui.btnCom.pressed.connect(lambda: self.ui.stackedWidget.setCurrentIndex(5))
        self.ui.btnData.pressed.connect(lambda: self.ui.stackedWidget.setCurrentIndex(6))
        self.ui.btnHallAdd.pressed.connect(lambda: (self.ui.stackedWidget.setCurrentIndex(7), SWFunctions.boxSelected(self)))
        self.ui.btnSettings.pressed.connect(lambda: self.ui.stackedWidget.setCurrentIndex(8))
        self.ui.btnMenu.pressed.connect(lambda: UIFunctions.animazioneMenu(self))


        # PAGE HALL FUNCTIONS
        self.ui.spiHall.valueChanged.connect(lambda: SWFunctions.loadHall(self))
        self.ui.btnHallExp.pressed.connect(lambda: SWFunctions.exportXLSXHall(self))
        self.ui.btnClose.pressed.connect(lambda: SWFunctions.closeAll(self))
        self.ui.btnHallRem.pressed.connect(lambda: SWFunctions.removeHall(self))
        self.ui.btnHallLoadCur.pressed.connect(lambda: self.com.start())
        self.ui.btnHallStopCur.pressed.connect(lambda: SWFunctions.stopCom(self))
        # PAGE CURVE FUNCTIONS
        self.ui.spiCurve.valueChanged.connect(lambda: SWFunctions.loadCurve(self))
        self.ui.btnCurveSave.pressed.connect(lambda: SWFunctions.saveCurve(self))
        self.ui.tblCurve.pressed.connect(lambda: UIFunctions.updateGraph(self))
        self.ui.btnCurveExp.pressed.connect(lambda: SWFunctions.exportXLSXCurve(self))
        self.ui.tblCurve.cellChanged.connect(lambda: SWFunctions.correctCurve(self))

        #PAGE TIME FUNCTIONS
        self.ui.tblTime.itemChanged.connect(lambda: SWFunctions.autocompleteTime(self))
        self.ui.btnTimeSave.pressed.connect(lambda: SWFunctions.saveTime(self))
        self.ui.btnTimeRem.pressed.connect(lambda: SWFunctions.removeTime(self))
        #self.ui.txtTimeRat.textChanged.connect(lambda: TMFunctions.loadKGRation(self))

        # PAGE DATA FUNCTIONS
        self.ui.btnDataAdd.pressed.connect(lambda: UIFunctions.animazioneMenuData(self))
        self.ui.btnDataSowAdd.pressed.connect(lambda: SWFunctions.saveSow(self))
        self.ui.btnDataRemSow.pressed.connect(lambda: SWFunctions.removeSow(self))
        self.ui.btnDataRemBox.pressed.connect(lambda: SWFunctions.removeBox(self))
        self.ui.btnDataBoxAdd.pressed.connect(lambda: SWFunctions.saveBox(self))
        self.ui.btnDataSaveCom.pressed.connect(lambda: SWFunctions.saveBoxCom(self))
        self.ui.btnDataTestCom.pressed.connect(lambda: SWFunctions.startTest(self))

        #PAGE ADD SOW IN BOX FUCNTIONS
        self.ui.radAddBirthY.toggled.connect(lambda: UIFunctions.animazioneMenuParto(self,self.ui.radAddBirthY.isChecked()))
        self.ui.btnAddAdd.pressed.connect(lambda: SWFunctions.saveSowInBox(self))
        self.ui.spiAddSelPigDate.dateChanged.connect(lambda: SWFunctions.updateDaysInBirth(self))
        self.ui.comAddSelBox.currentIndexChanged.connect(lambda: SWFunctions.checkBoxExisting(self))

        #PAGE CONF FUNCTIONS
        self.ui.btnSetConfCalib.pressed.connect(lambda: SWFunctions.saveConf(self,3))
        self.ui.btnSetConfImp.pressed.connect(lambda: SWFunctions.saveConf(self,2))
        self.ui.btnSetConfCom.pressed.connect(lambda: SWFunctions.saveConf(self,0))
        self.ui.btnSetConfBaud.pressed.connect(lambda: SWFunctions.saveConf(self,1))
# SHOW WINDOW
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec())



    ## DA USARE DOPO
    # self.ui.spiAddSelEntryDate.setMaximumDate(plm.now().date())
    # self.ui.spiAddSelPigDate.setMaximumDate(plm.now().date())
