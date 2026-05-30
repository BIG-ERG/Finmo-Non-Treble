#pip install evdev
#sudo usermod -a -G groupName userName
#   do line above if no device pop up

import evdev
from evdev import ecodes
import serial
import time
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton,QWidget,QGridLayout,QGraphicsProxyWidget
from PyQt6.QtCore import QTimer
import sys
import threading

yMouse = []
xMouse = []
xPen = []

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.setFixedSize(1024, 600) #size of window
        self.graphicslayout = pg.GraphicsLayoutWidget()
        
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGraph)
        self.timer.start(100)

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

    
    def updateGraph(self):
        self.curve1.setData(xMouse, yMouse)
        self.curve2.setData(xPen, yMouse)

    def plot1(self):#plotitem
        self.p1 = self.graphicslayout.addPlot(row=0, col=0,rowspan =4,colspan=2) #rowspan = aantal rijen hoote
        self.p1.setTitle("Plot 1")
        self.p1.showGrid(x=True, y=True)
        self.p1.addLegend()
        self.pen1 = pg.mkPen(color=("#FF0000FF"))#line color
        self.pen2 = pg.mkPen(color=("#FFFFFFFF"))#line color
        self.pen3 = pg.mkPen(color=("#FFFF00FF"))#line color
        self.curve1 = self.p1.plot(xMouse, yMouse, pen=self.pen1,name="Mouse")
        self.curve2 = self.p1.plot(xPen, yMouse, pen=self.pen2, name="Correction")\
        
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
        self.button1.setFixedSize(204, 150)
        self.proxy1 = QGraphicsProxyWidget()
        self.proxy1.setWidget(self.button1)
        self.graphicslayout.addItem(self.proxy1, 2, 2) # row, col , rowspan,colspan
        self.button1.setCheckable(True)
        self.button1.clicked.connect(self.the_button1_was_toggled)
        self.button1.setStyleSheet("""
            QPushButton {
            background-color: #0080FF;
            color: white;
            }
            QPushButton:checked {
            background-color: #232FD7;
            }
            """)
    def the_button1_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button2(self):
        
        self.button2 = QPushButton("mode 2")# title botton
        self.button2.setFixedSize(204, 150)
        self.proxy2 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy2.setWidget(self.button2)
        self.graphicslayout.addItem(self.proxy2, 2, 3) # row, col , rowspan,colspan
        self.button2.setCheckable(True)
        self.button2.clicked.connect(self.the_button2_was_toggled)
        self.button2.setStyleSheet("""
            QPushButton {
            background-color: #0080FF;
            color: white;
            }
            QPushButton:checked {
            background-color: #232FD7;
            }
            """)
    def the_button2_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button3(self):
        
        self.button3 = QPushButton("mode 3")# title botton
        self.button3.setFixedSize(204, 150)
        self.proxy3 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy3.setWidget(self.button3)
        self.graphicslayout.addItem(self.proxy3, 2, 4) # row, col , rowspan,colspan
        self.button3.setCheckable(True)
        self.button3.clicked.connect(self.the_button3_was_toggled)
        self.button3.setStyleSheet("""
            QPushButton {
            background-color: #0080FF;
            color: white;
            }
            QPushButton:checked {
            background-color: #232FD7;
            }
            """)
    def the_button3_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button4(self):
        
        self.button4 = QPushButton("reset")# title botton
        self.button4.setFixedSize(204, 150)
        self.proxy4 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy4.setWidget(self.button4)
        self.graphicslayout.addItem(self.proxy4, 3, 2) # row, col , rowspan,colspan
        self.button4.setCheckable(True)
        self.button4.clicked.connect(self.the_button4_was_toggled)
        self.button4.setStyleSheet("""
            QPushButton {
            background-color: #0080FF;
            color: white;
            }
            QPushButton:checked {
            background-color: #232FD7;
            }
            """)
    def the_button4_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button5(self):
        
        self.button5 = QPushButton("calibration")# title botton
        self.button5.setFixedSize(204, 150)
        self.proxy5 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy5.setWidget(self.button5)
        self.graphicslayout.addItem(self.proxy5, 3, 3) # row, col , rowspan,colspan
        self.button5.setCheckable(True)
        self.button5.clicked.connect(self.the_button5_was_toggled)
        self.button5.setStyleSheet("""
            QPushButton {
            background-color: #0080FF;
            color: white;
            }
            QPushButton:checked {
            background-color: #232FD7;
            }
            """)
    def the_button5_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)
    def create_button6(self):
        
        self.button6 = QPushButton("filter")# title botton
        self.button6.setFixedSize(204, 150)
        self.proxy6 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy6.setWidget(self.button6)
        self.graphicslayout.addItem(self.proxy6, 3, 4) # row, col , rowspan,colspan
        self.button6.setCheckable(True)
        self.button6.clicked.connect(self.the_button6_was_toggled)
        self.button6.setStyleSheet("""
            QPushButton {
            background-color: #0080FF;
            
            color: white;
            }
            QPushButton:checked {
            background-color: #232FD7;
            }
            """)
    def the_button6_was_toggled(self, checked): #checked gives button pressed or not pressed (true/False)
        print("Button state:", checked)

#---------------------------·LIST-DEVICES---------------------------------
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
     print(device.path, device.name, device.phys)

#-------------------------------------------------------------------------

xRel = 0
yRel = 0

xAbs = 0
yAbs = 0

device = evdev.InputDevice('/dev/input/event4') #change eventn to correct peripheral

def cpiToMM(dots):
    CPI = 1000
    return dots*25.4 / CPI

print("xAbs:   |yAbs:    ")

def mouseReader():
    global xAbs, yAbs, xRel, yRel
    for event in device.read_loop():

        if event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_RIGHT and event.value == 1:
                print("Right click detected — stopping")
                break

        if event.type == evdev.ecodes.EV_REL:               #if movement
            if event.code == evdev.ecodes.REL_X:            #if movement x
                xRel = cpiToMM(event.value)
                xAbs += xRel
            
            elif event.code == evdev.ecodes.REL_Y:          #if movement y
                yRel = cpiToMM(event.value)
                yAbs -= yRel

        if event.type == evdev.ecodes.SYN_REPORT:           #if sync event happens i.e. every time mouse updates

            ser.write(f'x:{xAbs}\n'.encode())
            print(f"{xAbs:8.2f}| {yAbs:8.2f}")
            xMouse.append(xAbs)
            yMouse.append(yAbs)


threading.Thread(
    target=mouseReader,
    daemon = True
).start()

app=QApplication(sys.argv)
window = MainWindow()
window.show()

xPen.append(int(ser.readline().decode().strip()))

sys.exit(app.exec())
