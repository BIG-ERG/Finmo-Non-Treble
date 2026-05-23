import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton,QWidget,QGridLayout,QGraphicsProxyWidget
import sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.setFixedSize(1024, 600) #size of window
        self.graphicslayout = pg.GraphicsLayoutWidget()
        
        self.setCentralWidget(self.graphicslayout)
        
        self.plot1()
        self.plot2()
        self.create_button1()
        self.create_button2()
        self.create_button3()
        self.create_button4()
        self.create_button5()
        self.create_button6()

        layout = self.graphicslayout.ci.layout

        layout.setColumnPreferredWidth(0, 204)
        layout.setColumnPreferredWidth(1, 204)
        layout.setColumnPreferredWidth(2, 204)
        layout.setColumnPreferredWidth(3, 204)
        layout.setColumnPreferredWidth(4, 204)
        

        layout.setRowPreferredHeight(0, 150)
        layout.setRowPreferredHeight(1, 150)
        layout.setRowPreferredHeight(2, 150)
        layout.setRowPreferredHeight(3, 150)
        #self.v = self.graphicslayout.addViewBox(row=1, col=1)
        # Voorbeelddata
        self.graphicslayout.setBackground("#000000FF")
    def plot1(self):#plotitem
        self.p1 = self.graphicslayout.addPlot(row=0, col=0,rowspan =3,colspan=2) #rowspan = aantal rijen hoote
        self.p1.setTitle("Plot 1")
        self.p1.showGrid(x=True, y=True)
        self.p1.addLegend()
        self.pen1 = pg.mkPen(color=("#FF0000FF"))#line color
        self.pen2 = pg.mkPen(color=("#FFFFFFFF"))#line color
        self.pen3 = pg.mkPen(color=("#FFFF00FF"))#line color
        y = [1, 2, 3, 4]
        x1 = [1, 4, 2, 3]
        x2 = [2, 1, 4, 1]
        x3 = [3, 2, 1, 5]
        self.p1.plot(x1, y, pen=self.pen1,name="Pen")
        self.p1.plot(x2, y, pen=self.pen2,name="path")
        self.p1.plot(x3, y, pen=self.pen3,name="Mouse")
    def plot2(self):

        self.p2 = self.graphicslayout.addPlot(row=0, col=2,colspan=3,rowspan=2)

        self.p2.setTitle("Plot 2")
        self.p2.showGrid(x=True, y=True)
        self.p2.addLegend()
        self.pen4 = pg.mkPen(color=("#FFFF00FF"))#line color
        self.pen5 = pg.mkPen(color=("#FF9900FF"))#line color
        x = [1, 2, 3, 4]
        y1 = [4, 1, 3, 2]
        y2 = [2, 1, 4, 1]
        self.p2.plot(x, y1, pen=self.pen4,name="divertion")
        self.p2.plot(x, y2, pen=self.pen5,name="correction")
    def create_button1(self):
        
        self.button1 = QPushButton("mode 1")# title botton
        self.proxy1 = QGraphicsProxyWidget()
        self.proxy1.setWidget(self.button1)
        self.graphicslayout.addItem(self.proxy1, 2, 2) # row, col , rowspan,colspan
        self.button1.setCheckable(True)
        self.button1.clicked.connect(self.the_button1_was_toggled)
    def the_button1_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button2(self):
        
        self.button2 = QPushButton("mode 2")# title botton
        self.proxy2 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy2.setWidget(self.button2)
        self.graphicslayout.addItem(self.proxy2, 2, 3) # row, col , rowspan,colspan
        self.button2.setCheckable(True)
        self.button2.clicked.connect(self.the_button2_was_toggled)
    def the_button2_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button3(self):
        
        self.button3 = QPushButton("mode 3")# title botton
        self.proxy3 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy3.setWidget(self.button3)
        self.graphicslayout.addItem(self.proxy3, 2, 4) # row, col , rowspan,colspan
        self.button3.setCheckable(True)
        self.button3.clicked.connect(self.the_button3_was_toggled)
    def the_button3_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button4(self):
        
        self.button4 = QPushButton("reset")# title botton
        self.proxy4 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy4.setWidget(self.button4)
        self.graphicslayout.addItem(self.proxy4, 3, 2) # row, col , rowspan,colspan
        self.button4.setCheckable(True)
        self.button4.clicked.connect(self.the_button4_was_toggled)
    def the_button4_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button5(self):
        
        self.button5 = QPushButton("calibration")# title botton
        self.proxy5 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy5.setWidget(self.button5)
        self.graphicslayout.addItem(self.proxy5, 3, 3) # row, col , rowspan,colspan
        self.button5.setCheckable(True)
        self.button5.clicked.connect(self.the_button5_was_toggled)
    def the_button5_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button6(self):
        
        self.button6 = QPushButton("filter")# title botton
        self.proxy6 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy6.setWidget(self.button6)
        self.graphicslayout.addItem(self.proxy6, 3, 4) # row, col , rowspan,colspan
        self.button6.setCheckable(True)
        self.button6.clicked.connect(self.the_button6_was_toggled)
    def the_button6_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    
app=QApplication(sys.argv)
window = MainWindow()
window.show()

app.exec() # houd het venster actief