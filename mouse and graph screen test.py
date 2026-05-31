import evdev
from evdev import ecodes
import serial
import time
import pyqtgraph as pg
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton,QWidget,QGridLayout,QGraphicsProxyWidget
from PyQt6.QtCore import QTimer
import sys
import threading
from svgpathtools import svg2paths, path
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO


#-----------------------------------mouse-setup----------------------------------#
xRel = 0
yRel = 0

xAbs = 0
yAbs = 0
#--------------------------------------------------------------------------------#

#-----------------------------------paths----------------------------------------#
#ui cant show hole in path but pen will apply it regardless
straight = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/straight.svg"
squiggly = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/squiggly.svg"
ziggert = r"/home/user/Documents/ProjectFinmo/Finmo-Non-Treble/svg/ziggert.svg"

xPath = []
yPath = []
lookup = []

def svgToCoord(path):
    global lookup, xPath, yPath
    lookup.clear()
    xPath.clear()
    yPath.clear()   
    lookup[:] = [-1] * 297

    paths, _ = svg2paths(path)

    for path in paths:
        for segment in path:
            for i in range(100):
                t = i / 99
                pt = segment.point(t)
                y_mm = round(pt.imag)
                xPath.append(pt.real)
                yPath.append(pt.imag)
                if 0 <= y_mm < 297:
                    lookup[y_mm] = pt.real

#--------------------------------------------------------------------------------#

#-----------------------------------serial-setup-arduino-------------------------#
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
time.sleep(2)
#--------------------------------------------------------------------------------#

#-----------------------------------UI-setup-------------------------------------#

yMouse = []
xMouse = []
xPen = []
yPen = []

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
        self.showFullScreen()
    
    def updateGraph(self):
        self.curve1.setData(xMouse, yMouse)
        self.curve2.setData(xPen, yPen)

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
        self.pen4 = pg.mkPen(color=("#FFFF00FF"))#line color
        self.pen5 = pg.mkPen(color=("#FF9900FF"))#line color
        x = [1, 2, 3, 4]
        y1 = [4, 1, 3, 2]
        y2 = [2, 1, 4, 1]
        self.p2.plot(x, y1, pen=self.pen4,name="divertion")
        self.p2.plot(x, y2, pen=self.pen5,name="correction")
    
    def create_button1(self):
        
        self.button1 = QPushButton("Straight")# title botton
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
        global xAbs, yAbs
        print("Button state:", checked)
        svgToCoord(straight)
        self.curve3.setData(xPath, yPath)
        xAbs = 0 #to be implemented: set xAbs and yAbs to the end point of the path, so that the mouse starts at the end of the path when the button is pressed
        yAbs = 0
        
    def create_button2(self):
        
        self.button2 = QPushButton("Squiggly")# title botton
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
        svgToCoord(squiggly)
        self.curve3.setData(xPath, yPath)
        
    def create_button3(self):
        
        self.button3 = QPushButton("Zig-Zag")# title botton
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
        svgToCoord(ziggert)
        self.curve3.setData(xPath, yPath)

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
        xPath.clear()
        yPath.clear()
        xPen.clear()
        yPen.clear()
        xMouse.clear()
        yMouse.clear()
        self.curve3.setData(xPath, yPath)

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
    def the_button6_was_toggled(self)
        QApplication.quit()

#--------------------------------------------------------------------------------#

#---------------------------SERVO-LOGIC------------------------------------------#
# ---------- Configuratie ----------
SERVO_PIN  = 18         # PWM-capabele GPIO pin
BUTTON_PIN = 17         # GPIO pin voor de drukknop
PWM_FREQ   = 50         # MG90S werkt op 50 Hz

# Hoeken voor de twee toestanden (pas aan op jouw mechanisme)
ANGLE_REST   = 0        # pen ligt (rusttoestand)
ANGLE_ACTIVE = 60       # pen opgetild (actieve toestand)

DEBOUNCE_MS = 200       # ontdender-tijd in milliseconden

pwm = None

pen_is_up = False   # begint in rusttoestand (pen ligt)

def angle_to_duty(angle):
    """Zet een hoek (0-180°) om naar duty cycle (%) voor 50 Hz PWM."""
    return 2.5 + (angle / 180.0) * 10.0

def set_angle(pwm, angle):
    pwm.ChangeDutyCycle(angle_to_duty(angle))
    time.sleep(0.4)              # tijd om naar positie te bewegen
    pwm.ChangeDutyCycle(0)       # signaal uit -> voorkomt jitter/zoemen

def button_pressed(channel):
    global pen_is_up
    if pen_is_up:
        print("Knop ingedrukt -> pen neerleggen")
        set_angle(pwm, ANGLE_REST)
        pen_is_up = False
    else:
        print("Knop ingedrukt -> pen optillen")
        set_angle(pwm, ANGLE_ACTIVE)
        pen_is_up = True

def servoUp():
    set_angle(pwm, ANGLE_REST)

def servoDown():
    set_angle(pwm, ANGLE_ACTIVE)

def servoSetup():
    global pwm
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SERVO_PIN, GPIO.OUT)
    GPIO.setup(BUTTON_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    pwm = GPIO.PWM(SERVO_PIN, PWM_FREQ)
    pwm.start(0)
#--------------------------------------------------------------------------------#

#---------------------------MOVEMENT-LOGIC---------------------------------------#
#based on lookup table and mouse movement, calculate the correction and apply it to the pen position
def offset(xMouse, yMouse):
    if 0 <= yMouse < 297:
        if lookup[yMouse] != -1:
            xOffset = lookup[yMouse] - xMouse
            servoDown()
            return xOffset
        else:
            servoUp()
            return 0
#--------------------------------------------------------------------------------#

#---------------------------·LIST-DEVICES-(TROUBLESHOOTING)----------------------#
# devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
# for device in devices:
#      print(device.path, device.name, device.phys)
#--------------------------------------------------------------------------------#

#---------------------------MOUSE-READER-----------------------------------------#

device = evdev.InputDevice('/dev/input/event4') #change eventn to correct peripheral

def cpiToMM(dots):
    CPI = 1000
    return dots*25.4 / CPI

def adsToMM(input):
    sliderLength = 60.0
    temp = sliderLength / 1024
    mm = (input * temp) - 30
    return mm

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
            # print(f"{xAbs:8.2f}| {yAbs:8.2f}")
            xMouse.append(xAbs)
            yMouse.append(yAbs)

def serialReader():
    while True:
        line = ser.readline().decode().strip()

        try:
            value = float(line)
            xPen.append(adsToMM(value)+xAbs)
            yPen.append(yAbs)
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
servoSetup()
app=QApplication(sys.argv)
window = MainWindow()
window.show()

sys.exit(app.exec())
#--------------------------------------------------------------------------------#
