from PyQt5 import QtWidgets
from Gonzales_UI_Code import Ui_MainWindow   
from PyQt5.QtGui import QIcon
from Gonzales_Logic_Code import *
import sys

# LSP: this is the main class. dito na naglalaro ang mga objects na instance ng GameManager
def getCheck(checkGame: GameManager):
    checkGame.game_actions.check()

class MAIN(QtWidgets.QMainWindow):
    def __init__(self):
        super(MAIN, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon("Logo.png"))
        
        self.connect_buttons()
        
    def about(self):
            self.ui.stackedWidget.setCurrentIndex(3)

    def home(self, ):
            self.ui.stackedWidget.setCurrentIndex(0) 

    def connect_buttons(self): 
        # ito ang mga objects na instance ng GameManager. 
        # dito naglalaro ang mga objects na instance ng GameManager.
        solo = GameManager(self, self.ui, "solo")
        player_1 = GameManager(self, self.ui, 1)
        player_2 = GameManager(self, self.ui, 2)
        
        self.ui.pb4.clicked.connect(lambda:self.about())
        self.ui.pb5.clicked.connect(lambda:self.home())
        self.ui.pb3.clicked.connect(lambda:self.home())
        self.ui.pb2.clicked.connect(lambda:self.home())
        self.ui.HistoryButton.clicked.connect(lambda: solo.history_manager.historyPage())
        
        self.ui.pb2.clicked.connect(lambda: solo.renew.try_again(self.ui))
        self.ui.Retry.clicked.connect(lambda: solo.renew.retry(self.ui))
        
        self.ui.pb2_2.clicked.connect(lambda: self.TryAnother_PVP(self.ui, player_1, player_2))
        self.ui.Retry_2.clicked.connect(lambda: self.retry_PVP(self.ui, player_1, player_2))
        self.checkAnswer(solo, player_1, player_2)
        
        radio_buttons = [
            self.ui.rb1_3, self.ui.rb2_3, self.ui.rb3_3, self.ui.rb4_3,
            self.ui.rb5_3, self.ui.rb6_3, self.ui.rb7_3, self.ui.rb8_5,
            self.ui.rb9, self.ui.rb10, self.ui.rb4_5, self.ui.rb12,
            self.ui.SOLORB, self.ui.PVPRB
        ]
        
        for rb in radio_buttons:
            rb.clicked.connect(lambda: self.handle_operation_selection(solo, player_1, player_2))
            
        self.ui.Le1_2.focusInEvent = lambda event: self.Player1Trigger(event, player_1, player_2)
        self.ui.Le1_3.focusInEvent = lambda event: self.Player2Trigger(event, player_1, player_2)
            
    def ClickTimerTrigger(self, source, player_1, player_2):
        if self.ui.PVPRB.isChecked:
            if source == self.ui.Le1_2:
                player_2.timer._stop()
                player_1.timer._start(player_1.timer._countdown)
            elif source == self.ui.Le1_3:
                player_1.timer._stop()
                player_2.timer._start(player_2.timer._countdown)
                
    def Player1Trigger(self, event, player_1, player_2):
        self.ClickTimerTrigger(self.ui.Le1_2, player_1, player_2)
        QtWidgets.QLineEdit.focusInEvent(self.ui.Le1_2, event)
            
    def Player2Trigger(self, event, player_1, player_2):
        self.ClickTimerTrigger(self.ui.Le1_3, player_1, player_2)
        QtWidgets.QLineEdit.focusInEvent(self.ui.Le1_3, event)
        
    def handle_operation_selection(self, solo, player_1, player_2):
        if self.ui.SOLORB.isChecked():
            solo.math_operation.executeOperation()   
        elif self.ui.PVPRB.isChecked():
            self.ui.lineEdit_11.setText("CLICK TO ANSWER!")
            self.ui.lineEdit_12.setText("CLICK TO ANSWER!")
            for x in [player_1, player_2]:
                x.math_operation.executeOperation()
            player_1.timer._stop()
            player_2.timer._stop()
            
    def checkAnswer(self, solo, player_1, player_2):
         # polymorph
        checkB  = [
            (self.ui.Submit, solo),
            (self.ui.Submit_2, player_1),
            (self.ui.Submit_3, player_2)
        ] 
         
        for Bt, plyrs in checkB:
            Bt.clicked.connect(lambda _, x=plyrs: getCheck(x))  
            
                
    def TryAnother_PVP(self, ui, player_1, player_2):
        player_1.renew.try_again(ui)
        player_2.renew.try_again(ui)
            
        self.ui.Le1_2.setEnabled(True)
        self.ui.Submit_2.setEnabled(True)
        self.ui.Le1_3.setEnabled(True)
        self.ui.Submit_3.setEnabled(True)
            
            # Reset timers
        player_1.timer._stop()
        player_2.timer._stop()
        
            
    def retry_PVP(self, ui, player_1, player_2):
        player_1.renew.retry(ui)
        player_2.renew.retry(ui)
        player_1.timer._stop()
        player_2.timer._stop()

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    application = MAIN()
    application.show()
    sys.exit(app.exec_())

