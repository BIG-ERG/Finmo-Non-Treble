import numpy as np
import evdev
from evdev import ecodes
import serial
import time
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton,QWidget,QGridLayout,QGraphicsProxyWidget, QVBoxLayout, QLineEdit, QLabel, QDoubleSpinBox
from PyQt6.QtCore import QTimer
import sys
import threading
from svgpathtools import svg2paths, path
import matplotlib.pyplot as plt

#---------------------------------PID-GAINS--------------------------------------#
gainP = 0
gainI = 0
gainD = 0
#--------------------------------------------------------------------------------#

#-----------------------------------testplan-measurements------------------------#
measure = 0
timeUI = []
timeMouse = []
timeEF = []
penDeviation = []

def clearMeasurements():
    global timeUI, timeMouse, timeEF, penDeviation
    timeUI.clear()
    timeMouse.clear()
    timeEF.clear()
    penDeviation.clear()

def printMeasurements():
    global timeUI, timeMouse, timeEF, penDeviation
    print(f"Hz UI: {np.mean(timeUI)}")
    print(f"Hz mouse: {np.mean(timeMouse)}")
    print(f"Hz pen: {np.mean(timeEF)}")
    print(f"Average pen deviation: {np.mean(penDeviation)}")
    print(f"Max pen deviation: {max(penDeviation)}")
    print(f"Min pen deviation: {min(penDeviation)}")
    clearMeasurements()

#--------------------------------------------------------------------------------#


#-----------------------------------mouse-setup----------------------------------#
xRel = 0
yRel = 0

xAbs = 50
yAbs = 50

direction = 0
#--------------------------------------------------------------------------------#

#-----------------------------------paths----------------------------------------#
#ui cant show hole in path but pen will apply it regardless
straight = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/straight.svg"
squiggly = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/squiggly.svg"
ziggert = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/ziggert.svg"

# straight = r"/home/bigerg/Finmo-Non-Treble/svg/straight.svg"
# squiggly = r"/home/bigerg/Finmo-Non-Treble/svg/squiggly.svg"
# ziggert = r"/home/bigerg/Finmo-Non-Treble/svg/ziggert.svg"

xPath = []
yPath = []
lookup = []
lookup [:] = [-1] * 2970
path1End = 0
path2Start = 0

def svgToCoord(path):
    global lookup, xPath, yPath, path1End, path2Start
    lookup.clear()
    xPath.clear()
    yPath.clear()   
    lookup[:] = [-1] * 2970

    paths, _ = svg2paths(path)

    for path in paths:                      #for ui
        for segment in path:
            for i in range(100):
                t = i / 99
                pt = segment.point(t)
                xPath.append(pt.real)
                yPath.append(pt.imag)
    
    for path in paths:                      #for lookup table
        for segment in path:                #we want a higher resolution while keeping the scale normal for the ui
            for i in range(1000):
                t = i / 999
                pt = segment.point(t)
                y_mm = round(pt.imag*10)
                if 0 <= y_mm < 2970:
                    lookup[y_mm] = pt.real

    # Find all indices where value != -1
    valid = [i for i, v in enumerate(lookup) if v != -1]
    
    # Find the largest gap between consecutive valid indices
    gaps = [(valid[i+1] - valid[i], i) for i in range(len(valid)-1)]
    _, gap_idx = max(gaps)
    
    left_i = valid[gap_idx]
    right_i = valid[gap_idx + 1]
    
    path1End = lookup[left_i]
    path2Start = lookup[right_i]

    print(path1End)
    print(path2Start)


#--------------------------------------------------------------------------------#

#-----------------------------------serial-setup-arduino-------------------------#
ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
time.sleep(0.5)
#--------------------------------------------------------------------------------#

#---------------------------------TROUBLESHOOTING--------------------------------#
def sendPIDgains():
    global gainP, gainI, gainD
    ser.write(f'p:{gainP}\n'.encode())
    ser.write(f'i:{gainI}\n'.encode())
    ser.write(f'd:{gainD}\n'.encode())

#--------------------------------------------------------------------------------#

#-----------------------------------UI-setup-------------------------------------#

yMouse = []
xMouse = []
xPen = []
yPen = []
xOffsetB = []
yOffsetB = []

nowUI = time.perf_counter()
prvTimeUI = None

class TroubleshootWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Troubleshooting")
        self.resize(200, 200)

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Gain P"))
        self.input1 = QDoubleSpinBox()
        layout.addWidget(self.input1)

        layout.addWidget(QLabel("Gain I"))
        self.input2 =  QDoubleSpinBox()
        layout.addWidget(self.input2)

        layout.addWidget(QLabel("Gain D"))
        self.input3 =  QDoubleSpinBox()
        layout.addWidget(self.input3)

        self.sendbutton = QPushButton("Send Gains")
        self.sendbutton.clicked.connect(self.applySettings)
        self.joltbutton = QPushButton("Jolt")
        self.joltbutton.clicked.connect(self.jolt)

        layout.addWidget(self.sendbutton)
        layout.addWidget(self.joltbutton)

        self.setLayout(layout)

    def applySettings(self):
        global gainP, gainI, gainD
        gainP = self.input1.value()
        gainI = self.input2.value()
        gainD = self.input3.value()
        sendPIDgains()

    def jolt(self):
        state = 0
        if state == 0:
            ser.write(f'x:{-20.0}\n'.encode())
            state = 1
        else:
            ser.write(f'x:{20}\n'.encode())
            state = 0

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("UI")
        self.setFixedSize(1024, 600) #size of window
        self.graphicslayout = pg.GraphicsLayoutWidget()
        self.troubleshootWindow = None
        
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
        self.showFullScreen()
    
    def updateGraph(self):
        self.curve1.setData(xMouse, yMouse)
        self.curve2.setData(xPen, yPen)
        self.curve4.setData(yOffsetB, xOffsetB)
        self.curve5.setData(yPen, xPen)

        #for test 10

        if measure == 1:
            global nowUI, prvTimeUI
            nowUI = time.perf_counter()
            if prvTimeUI is not None:
                dt = nowUI - prvTimeUI
                hz = 1 / dt
                timeUI.append(hz)
            prvTimeUI = nowUI

    def plot1(self):#plotitem
        self.p1 = self.graphicslayout.addPlot(row=0, col=0,rowspan =4,colspan=2) #rowspan = aantal rijen hoote
        self.p1.setTitle("Plot 1")
        self.p1.showGrid(x=False, y=False)
        self.p1.setXRange(0,210, padding = 0)
        self.p1.setYRange(0,297, padding = 0)
        self.p1.addLegend()
        self.pen1 = pg.mkPen(color=("#FF0000FF"))#line color
        self.pen2 = pg.mkPen(color=("#FFFFFFFF"))#line color
        self.pen3 = pg.mkPen(color=("#FFFF00FF"))#line color
        self.curve1 = self.p1.plot(xMouse, yMouse, pen=self.pen1,name="Hand")
        self.curve2 = self.p1.plot(xPen, yPen, pen=self.pen2, name="Correction")
        self.curve3 = self.p1.plot(xPath, yPath, pen=self.pen3, name="Path")
        
    def plot2(self):

        self.p2 = self.graphicslayout.addPlot(row=0, col=2,colspan=3,rowspan=2)

        self.p2.setTitle("Plot 2")
        self.p2.showGrid(x=True, y=True)
        self.p2.addLegend()
        self.p2.setXRange(-200,-90, padding = 0)
        self.p2.setYRange(-30,30, padding = 0)
        self.pen4 = pg.mkPen(color=("#FFFF00FF"))#line color
        self.pen5 = pg.mkPen(color=("#FF9900FF"))#line color
        self.curve4 = self.p2.plot(yOffsetB, xOffsetB, pen=self.pen4,name="Offset")
        self.curve5 = self.p2.plot(yPen, xPen, pen=self.pen5, name="Correction")
    
    def create_button1(self):
        
        self.button1 = QPushButton("Straight")# title botton
        self.button1.setFixedSize(204, 150)
        self.proxy1 = QGraphicsProxyWidget()
        self.proxy1.setWidget(self.button1)
        self.graphicslayout.addItem(self.proxy1, 2, 2) # row, col , rowspan,colspan
        self.button1.setCheckable(False)
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
        global xAbs, yAbs, measure, lookup
        svgToCoord(straight)
        xAbs = xPath[0]
        yAbs = yPath[0]
        xMouse.clear()
        yMouse.clear()
        xOffsetB.clear()
        yOffsetB.clear()
        self.curve3.setData(xPath, yPath)
        measure = 1
        
    def create_button2(self):
        
        self.button2 = QPushButton("Squiggly")# title botton
        self.button2.setFixedSize(204, 150)
        self.proxy2 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy2.setWidget(self.button2)
        self.graphicslayout.addItem(self.proxy2, 2, 3) # row, col , rowspan,colspan
        self.button2.setCheckable(False)
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
        global xAbs, yAbs, measure
        svgToCoord(squiggly)
        xAbs = xPath[0]
        yAbs = yPath[0]
        xMouse.clear()
        yMouse.clear()
        xOffsetB.clear()
        yOffsetB.clear()
        self.curve3.setData(xPath, yPath)
        measure = 1

    def create_button3(self):
        
        self.button3 = QPushButton("Zig-Zag")# title botton
        self.button3.setFixedSize(204, 150)
        self.proxy3 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy3.setWidget(self.button3)
        self.graphicslayout.addItem(self.proxy3, 2, 4) # row, col , rowspan,colspan
        self.button3.setCheckable(False)
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
        global xAbs, yAbs, measure
        svgToCoord(ziggert)
        xAbs = xPath[0]
        yAbs = yPath[0]
        xMouse.clear()
        yMouse.clear()
        xOffsetB.clear()
        yOffsetB.clear()
        self.curve3.setData(xPath, yPath)
        measure = 1

    def create_button4(self):
        
        self.button4 = QPushButton("reset")# title botton
        self.button4.setFixedSize(204, 150)
        self.proxy4 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy4.setWidget(self.button4)
        self.graphicslayout.addItem(self.proxy4, 3, 2) # row, col , rowspan,colspan
        self.button4.setCheckable(False)
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
        global measure
        measure = 0
        printMeasurements()
        xPath.clear()
        yPath.clear()
        xPen.clear()
        yPen.clear()
        xMouse.clear()
        yMouse.clear()

    def create_button5(self):
        
        self.button5 = QPushButton("Troubleshooting")# title botton
        self.button5.setFixedSize(204, 150)
        self.proxy5 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy5.setWidget(self.button5)
        self.graphicslayout.addItem(self.proxy5, 3, 3) # row, col , rowspan,colspan
        self.button5.setCheckable(False)
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
        if self.troubleshootWindow is None:
                self.troubleshootWindow = TroubleshootWindow()

        self.troubleshootWindow.show()

    def create_button6(self):
        
        self.button6 = QPushButton("EXIT")# title botton
        self.button6.setFixedSize(204, 150)
        self.proxy6 = QGraphicsProxyWidget() # to set buttons in black
        self.proxy6.setWidget(self.button6)
        self.graphicslayout.addItem(self.proxy6, 3, 4) # row, col , rowspan,colspan
        self.button6.setCheckable(False)
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
    def the_button6_was_toggled(self):
        QApplication.quit()

#--------------------------------------------------------------------------------#

#---------------------------SERVO-LOGIC------------------------------------------#
servoState = None     # to avoid spamming serial buffer with servo commands

def servoUp():
    global servoState
    if servoState != 1:
        ser.write(f's:0\n'.encode())
        servostate = 1

def servoDown():
    global servoState
    if servoState != 0:
        ser.write(f's:1\n'.encode())
        servostate = 0
#--------------------------------------------------------------------------------#

#---------------------------MOVEMENT-LOGIC---------------------------------------#
#based on lookup table and mouse movement, calculate the correction and apply it to the pen position
def xOffset(xMouse, yMouse):
    global lookup
    if (0 <= yMouse < 297) and (0 <= xMouse < 210):
        if lookup[int(yMouse*10)] != -1:
            xOffset = lookup[int(yMouse*10)] - xMouse
            return xOffset
        else:
            return False
#--------------------------------------------------------------------------------#

#---------------------------·LIST-DEVICES-(TROUBLESHOOTING)----------------------#
devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
for device in devices:
     print(device.path, device.name, device.phys)
#--------------------------------------------------------------------------------#

#---------------------------MOUSE-READER-----------------------------------------#

device = evdev.InputDevice('/dev/input/event0') #change eventn to correct peripheral

def cpiToMM(dots):
    CPI = 1000
    return dots*25.4 / CPI

def adsToMM(input):
    sliderLength = 60.0
    temp = sliderLength / 1024
    mm = (input * temp) - 30
    return mm

# print("xAbs:   |yAbs:    ")

prvTimeMouse = None
nowMouse = time.perf_counter

def mouseReader():
    global xAbs, yAbs, xRel, yRel, prvTimeMouse, measure, nowMouse, yPath, direction


    for event in device.read_loop():

        if event.type == ecodes.EV_KEY:
            if event.code == ecodes.BTN_RIGHT and event.value == 1:
                print("Right click detected stopping")
                break

        if event.type == evdev.ecodes.EV_REL:               #if movement
            if event.code == evdev.ecodes.REL_X:            #if movement x
                xRel = cpiToMM(event.value)
                xAbs += xRel
            
            elif event.code == evdev.ecodes.REL_Y:          #if movement y
                yRel = cpiToMM(event.value)
                yAbs -= yRel
                if yRel < 0:
                    direction = 1
                else:
                    direction = -1

        if event.type == evdev.ecodes.SYN_REPORT:           #if sync event happens i.e. every time mouse updates

            # ser.write(f'x:{xAbs}\n'.encode())
            # print(f"{xAbs:8.2f}| {yAbs:8.2f}")

            #for test 2
            if measure == 1:
                nowMouse = time.perf_counter()

                if prvTimeMouse is not None:
                    hz = 1.0 / (nowMouse - prvTimeMouse)
                    timeMouse.append(hz)

                prvTimeMouse = nowMouse

            xMouse.append(xAbs)
            yMouse.append(yAbs)
            temp = xOffset(xAbs, yAbs)

            if temp != False:
                if temp > -30.0 and temp < 30.0:
                    ser.write(f'x:{temp}\n'.encode())
                    xOffsetB.append(temp)
                    yOffsetB.append(yAbs*-1)
                    servoDown()
                    print("inside path")
                else:
                    servoUp()
                    xOffsetB.append(0)
                    yOffsetB.append(yAbs*-1)
                    print('outside path')
            elif temp == False:
                servoUp()
                xOffsetB.append(0)
                yOffsetB.append(yAbs*-1)
                if direction > 0:
                    ser.write(f'x:{path1End - xAbs}\n'.encode())
                else:
                    ser.write(f'x:{path2Start - xAbs}\n'.encode())
                print('hole')


prvTimeEF = None
nowEF = time.perf_counter()

def serialReader():
    global prvTimeEF, nowEF, nowMouse, measure, penDeviation
    while True:
        line = ser.readline().decode().strip()
        try:
            value = float(line)
            xPen.append(adsToMM(value)+xAbs)
            yPen.append(yAbs)
            penDeviation.append(xOffset(adsToMM(value)+xAbs, yAbs))

            #for test 1
            if measure == 1:
                nowEF = time.perf_counter()

                if prvTimeEF is not None:
                    hz = 1.0 / (nowEF - prvTimeEF)
                    timeEF.append(hz)

                prvTimeEF = nowEF

        except ValueError:
            pass

#--------------------------------------------------------------------------------#

#---------------------------------THREADING--------------------------------------#
threading.Thread(
    target=mouseReader,
    daemon = True
).start()

threading.Thread(
    target=serialReader,
    daemon=True
).start()
#--------------------------------------------------------------------------------#

#---------------------------------MAIN-------------------------------------------#
app=QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
#--------------------------------------------------------------------------------#
