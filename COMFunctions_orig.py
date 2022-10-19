from main import *

class COMClass(QThread):

    def __init__(self, comUI, self2):
        super().__init__()
        self.ui = self2.ui
        self.self = self2
        self.self.master = 0

    def run(self):
        self.self.calibAndImp = False
        self.self.debugMode = False
        self.self.curveLoaded = False
        self.self.feedActive = False
        self.self.stopCom = False
        self.self.curveOnCom = False
        if QTime.currentTime().toString() == "00:00:00":
            self.self.curveOnCom = True
        while True:
            comItem = self.self.dbConf.get(doc_id = 1)
            if self.self.master == 0:
                try:
                    print("CONNESSIONE MODBUS IN CORSO...")
                    print(comItem)
                    self.self.master = modbus_rtu.RtuMaster(serial.Serial(comItem.get('comPort'), baudrate = comItem.get('comBaud'), bytesize = 8, parity='N', stopbits=1))
                    self.self.master.set_timeout(1)
                    self.ui.chkHallCom.setChecked(True)
                    t.sleep(1)
                except:
                    print("CONNESSIONE NON RIUSCITA.")
                    break
            else:
                if self.self.calibAndImp == False:
                    print("RICHIESTA CALIBRAZIONE...")
                    COMClass.setTime(self)
                    self.self.calibAndImp = True
                    print("CALIBRAZIONE RIUSCITA.")
                elif self.self.debugMode == False:
                    print("MODALITA' DEBUG ATTIVATA...")
                    self.self.debugMode = True
                    print("MODALITA' DEBUG COMPLETATA")
                elif self.self.curveOnCom == False:
                    print("CARICAMENTO CURVA IN CORSO...")
                    COMClass.sendCurveOnCom(self)
                    self.self.curveOnCom = True
                if self.self.feedActive != self.self.activeFeed:
                    COMClass.startStopFeed(self)
                else:
                    if QTime.currentTime().toString("s") == "30":
                        print("LETTURA NORMALE IN CORSO...")
                        COMClass.readNowFeed(self)
            t.sleep(1)
            if self.self.stopCom:
                self.quit()
                self.stop()
                print("THREAD STOPPED")

    def startStopFeed(self):
        self.self.feedActive = self.self.activeFeed
        if self.self.feedActive:
            print("ATTIVAZIONE PASTO IN CORSO...")
            print(self.self.master.execute(0, cst.WRITE_SINGLE_COIL, 0, output_value=True))
            COMClass.sendCurveOnCom(self)
        else:
            print("DISATTIVAZIONE PASTO IN CORSO...")
            print(self.self.master.execute(0, cst.WRITE_SINGLE_COIL, 0, output_value=False))

    def readNowFeed(self):
            for item in self.self.dbHall:
                boxPos = self.self.dbBox.get(self.self.query.boxName == item.get('boxName'))
                boxCom = int(boxPos.get('comPos'))
                if boxCom > 0:
                    try:
                        readNowFeedKG = self.self.master.execute(boxCom, cst.READ_INPUT_REGISTERS,8,1)
                    #print(readNowFeedKG)
                        self.self.dbHall.upsert({'readNowFeedKG':readNowFeedKG}, self.self.query.boxName == item.get('boxName'))
                        t.sleep(0.02)
                        for i in range(self.ui.tblHall.rowCount()):
                            if self.ui.tblHall.item(i,0).text() == item.get('boxName'):
                                self.ui.tblHall.setItem(i,7,QTableWidgetItem(str(readNowFeedKG)))
                    except:
                        pass

    def sendCurveOnCom(self):
        print("AZZERA CURVE")
        #print(self.self.master.execute(0, cst.WRITE_SINGLE_REGISTER, 7, output_value=0))
        for item in self.self.dbHall:
            boxPos = self.self.dbBox.get(self.self.query.boxName == item.get('boxName'))
            boxCom = int(boxPos.get('comPos'))
            try:
                curToSend = item.get('curKGToday')
                rat = self.ui.txtTimeRat.text().strip('%')
                ratToSend = int(int(curToSend) * (int(rat)/100)*int(self.ui.txtTimeNrAct.text()))
                print(self.self.master.execute(boxCom, cst.WRITE_SINGLE_REGISTER, 7, output_value=ratToSend))
            except:
            	print("NON LETTO")

    def setTime(self):
        self.self.master.execute(0, cst.WRITE_SINGLE_REGISTER, 0, output_value=((QDateTime.currentSecsSinceEpoch() >> 16) & 0xFFFF))
        t.sleep(0.2)
        self.self.master.execute(0, cst.WRITE_SINGLE_REGISTER, 1, output_value=((QDateTime.currentSecsSinceEpoch() & 0xFFFF)))
        print(QDateTime.currentDateTime().toString()+" ORA AGGIORNATA")
