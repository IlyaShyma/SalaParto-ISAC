from main import *


class FDFunctions():

    def checkFeedTime(self):
        self.activeFeed = False
        for item in self.dbTime:
            if item.get('active') == "SI":
                fr = QTime.fromString(item.get('fr'),"hh:mm")
                to = QTime.fromString(item.get('to'),"hh:mm")
                now = QTime.currentTime()
                if fr<now and to>now:
                    self.activeFeed = item.doc_id
                    self.ui.txtTimeDur.setText(str(int(fr.secsTo(to)/60))+" Minuti")
        if self.activeFeed:
            self.ui.txtTimeAct.setText("SI")
            self.ui.txtTimeNrAct.setText(str(self.activeFeed))
            self.ui.chkHallFeed.setChecked(True)
        else:
            self.ui.txtTimeAct.setText("NO")
            self.ui.chkHallFeed.setChecked(False)
            self.ui.txtTimeNrAct.setText("0")
        self.ui.txtTimeTotFeed.setText(str(self.dbTime.count(self.query.active =="SI")))
        self.ui.txtTimeRat.setText(str(int(100/int(self.ui.txtTimeTotFeed.text())))+"%")




    def writeReg(self,address,val):
        pass
