import sys
import time
import datetime
import os
from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import (QApplication, QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
        QMessageBox, QProgressBar, QPushButton, QWidget)

import mainwindow_rc
from ui_mainwindow import Ui_MainWindow

try:
	from ctypes import windll
	global io
	io = windll.dlportio # requires dlportio.dll !!!
	print('Parallel port open\n')
except:
	print('The parallel port couldn\'t be opened\n')

# Ensure that relative paths start from the same directory as this script
# _thisDir = os.path.dirname(os.path.abspath(__file__)).decode(sys.getfilesystemencoding())
# os.chdir(_thisDir)
# expTime = data.getDateStr()
# filenametxt = _thisDir + os.sep + u'data/ERP%s' %(expTime)

flag = 0
count = 0
start = time.time()
# Coordinated Multicasting with Opportunistic User Selection in Multicell Wireless Systems, yao win peter hong
# The psychophysics of chasing: A case study in the perception of animacy. Cognitive Psychology, Tao Gao
# Understanding In-Video Dropouts and Interaction Peaks in Online Lecture Videos, Juho Kim
urls = ["https://www.u-tokyo.ac.jp/en/index.html", 
"https://www.ee.nthu.edu.tw/~ywhong/", 
"https://www.math.ust.hk/~magan/", 
"https://www.stanford.edu", 
"https://juhokim.com/",
"https://www.polito.it/?lang=en"]
# urls = ["https://www.u-tokyo.ac.jp/en/index.html", "https://www.polito.it/?lang=en", "https://www.stanford.edu", "https://www.tu-berlin.de/menue/home/parameter/en/", "https://www.ee.nthu.edu.tw/~ywhong/", "http://www.stat.ucla.edu/~taogao/pubs.html", "https://juhokim.com/publications.html", "https://www.amazon.in"]
# search_instruction = ["murata", "carmagnola", "larry", "meran", "p1", "p2", "boat", "boat"]
search_instruction = ["murata", 
"yao", 
"tao", 
"larry", 
"juho",
"carmagnola"]
msg = ["Faculty Name : S. Murata \n Department : Department of Pharmaceutical Sciences", 
"Publication : Coordinated Multicasting with Opportunistic User Selection in Multicell Wireless Systems", 
"Publication : On the role of wind and tide in generating variability of Pearl River plume during summer in a coupled wide estuary and shelf system", 
"Faculty Name : Larry Ragent \n Department : Music", 
"Publication : Understanding In-Video Dropouts and Interaction Peaks in Online Lecture Videos",
"Faculty Name : CARMAGNOLA IRENE \n Department : Mechanical and Aerospace Engineering"]
# msg = ["Faculty Name : S. Murata \n Department : Department of Pharmaceutical Sciences", "Faculty Name : CARMAGNOLA IRENE \n Department : Mechanical and Aerospace Engineering", "Faculty Name : Larry Ragent \n Department : Music", "Faculty Name : Meran, Georg \n Department : Economics", "Brands: Xiomi, Mi, Poco, Samsung \n Price Range : 15,000-20,000 \n Processor : Qualcomm SnapDragon845", "Brands: Xiomi, Mi, Poco, Samsung \n Price Range : 0-5,000 \n Battery : 4000MAH \n Camera : 12MP", "Brand : Boat", "Brand : Boat"]
message = ""
# product = ["Poco F1 Qualcomm SnapDragon845 price range under 15k-20k", "Xiaomi Redmi 7A 4000 MAH battery 12MP Rear Camera under 5k", "boat Stone 700"]
instruction = ["file:///E:/courses/sem7/ell890(CN)/STIMULUS/instruction.html"]
class MainWindow(QMainWindow, Ui_MainWindow):
    # Maintain the list of browser windows so that they do not get garbage
    # collected.
    _window_list = []

    def __init__(self):
        super(MainWindow, self).__init__()

        MainWindow._window_list.append(self)

        self.setupUi(self)

        # Qt Designer (at least to v4.2.1) can't handle arbitrary widgets in a
        # QToolBar - even though uic can, and they are in the original .ui
        # file.  Therefore we manually add the problematic widgets.
        self.lblAddress = QLabel("Address", self.tbAddress)
        self.tbAddress.insertWidget(self.actionGo, self.lblAddress)
        self.addressEdit = QLineEdit(self.tbAddress)
        self.tbAddress.insertWidget(self.actionGo, self.addressEdit)

        self.addressEdit.returnPressed.connect(self.actionGo.trigger)
        self.actionBack.triggered.connect(self.WebBrowser.GoBack)
        self.actionForward.triggered.connect(self.WebBrowser.GoForward)
        self.actionStop.triggered.connect(self.WebBrowser.Stop)
        self.actionRefresh.triggered.connect(self.WebBrowser.Refresh)
        self.actionHome.triggered.connect(self.search)
        self.actionSearch.triggered.connect(self.WebBrowser.GoSearch)

        self.pb = QProgressBar(self.statusBar())
        self.pb.setTextVisible(False)
        self.pb.hide()
        self.statusBar().addPermanentWidget(self.pb)
        self.WebBrowser.dynamicCall('GoHome()')
        self.setWindowTitle("PyQt messagebox example - pythonprogramminglanguage.com") 

        self.text_box = QPlainTextEdit(self)
        self.text_box.insertPlainText("You can write text here.\n")
        self.text_box.move(950,910)
        self.text_box.resize(300,80)
    
    def closeEvent(self, e):
        MainWindow._window_list.remove(self)
        e.accept()

    def on_WebBrowser_TitleChange(self, title):
        self.setWindowTitle("Qt WebBrowser - " + title)

    def on_WebBrowser_ProgressChange(self, a, b):
        if a <= 0 or b <= 0:
            self.pb.hide()
            return

        self.pb.show()
        self.pb.setRange(0, b)
        self.pb.setValue(a)

    def on_WebBrowser_CommandStateChange(self, cmd, on):
        if cmd == 1:
            self.actionForward.setEnabled(on)
        elif cmd == 2:
            self.actionBack.setEnabled(on)

    def on_WebBrowser_BeforeNavigate(self):
        self.actionStop.setEnabled(True)

    def on_WebBrowser_NavigateComplete(self, _):
        self.actionStop.setEnabled(False)

    @pyqtSlot()
    def on_actionGo_triggered(self):
        self.WebBrowser.dynamicCall('Navigate(const QString&)',
                self.addressEdit.text())

    @pyqtSlot()
    def on_actionNewWindow_triggered(self):
        window = MainWindow()
        window.show()
        window.addressEdit.setText(self.addressEdit.text())
        window.actionStop.setEnabled(True)
        window.on_actionGo_triggered()

    @pyqtSlot()
    def on_actionAbout_triggered(self):
        QMessageBox.about(self, "About WebBrowser",
                "This Example has been created using the ActiveQt integration into Qt Designer.\n"
                "It demonstrates the use of QAxWidget to embed the Internet Explorer ActiveX\n"
                "control into a Qt application.")

    @pyqtSlot()
    def on_actionAboutQt_triggered(self):
        QMessageBox.aboutQt(self, "About Qt")

    def search(self):
        global count
        global flag
        global start
        # print (count)
        self.text_box.hide()
        self.text_box.clear()
        if(flag == 0):
            self.addressEdit.setText(instruction[0])
            self.actionGo.trigger()
            flag = 1
        else:
            if(count > 18):
                MainWindow._window_list.remove(self)
                exit()
            elif(count == 18):
                self.addressEdit.setText("file:///E:/courses/sem7/ell890(CN)/STIMULUS/end.html")
                self.actionGo.trigger()
            elif (count%3==0):
                self.addressEdit.setText("file:///E:/courses/sem7/ell890(CN)/STIMULUS/"+search_instruction[int(count/3)]+".html")
                self.actionGo.trigger()
            elif(count%3==1):
                print (int(count/3))
                print ("website Loading.....")
                end = time.time()
                print (end - start)
                self.addressEdit.setText(urls[int(count/3)])
                self.actionGo.trigger()
                end = time.time()
                self.text_box.show()
                self.text_box.insertPlainText(msg[int(count/3)])
            else:
                print ("website navigation completed")
                end = time.time()
                print (end - start)
                self.addressEdit.setText("file:///E:/courses/sem7/ell890(CN)/STIMULUS/fixation.html")
                self.actionGo.trigger()
                # time.sleep(15)
                # self.search()
            count = count + 1
            

if __name__ == "__main__":
    a = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    w.search()
    sys.exit(a.exec_())
