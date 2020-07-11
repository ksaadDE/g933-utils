#!/usr/bin/python3
"""
	LogiTech g933 GUI by ksaadDE
	
	Thanks for g933-utils  https://github.com/ashkitten/g933-utils (@ashkitten)
	icon: Icon made by Freepik perfect from www.flaticon.com"
	bing.mp3 https://freesound.org/data/previews/91/91926_7037-lq.mp3
"""
import sys, subprocess, os
lpath = os.path.dirname(os.path.abspath(__file__)) + os.path.sep
print(lpath)
os.chdir(lpath)

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

iconFile = lpath + "logitech.png"

m_nMouseClick_X_Coordinate = 0
m_nMouseClick_Y_Coordinate = 0

shownNotification_Offline = False
shownNotification_Full = False
shownNotification_LessTen = False
shownNotification_Half = False

def loadToFloat(state):
	try:
		return float(state.split(" ")[1].replace("%",""))
	except:
		return -1
def getLoadState():
	try:
		com = subprocess.Popen(['g933-utils', 'get', 'battery'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
		stdout, stderr = com.communicate()
		return stdout.decode('utf-8')
	except:
		return -1

def resetNotifications():
	global shownNotification_Full
	global shownNotification_Half
	global shownNotification_LessTen
	global shownNotification_Offline

	if shownNotification_Full:
		shownNotification_Full = False
	if shownNotification_Half:
		shownNotification_Half = False
	if shownNotification_LessTen:
		shownNotification_LessTen = False
	if shownNotification_Offline:
		shownNotification_Offline = False

def notificationLessLoad(loadst):
	global shownNotification_Full
	global shownNotification_Half
	global shownNotification_LessTen
	global shownNotification_Offline

	# gets the battery status from getLoadState()
	load = loadToFloat(loadst)
	if load == -1:
		if not shownNotification_Offline:
			trycon.showMessage("Logitech g933", "turned off", icon)
			shownNotification_Offline = True
		return
	# load is greater than 90% and no notification send
	if load > 90 and not shownNotification_Full:
		print("above 90")
		trycon.showMessage("Logitech g933", "90% Loaded! :>", icon)
		resetNotifications()
		shownNotification_Full = True
	# if load is less than 45 and  greater than 10% and no notification send
	if round(load) <= 50 and round(load) > 40 and not shownNotification_Half:
		print("less than half")
		trycon.showMessage("Logitech g933", "Halftime! 50%", icon)
		resetNotifications()
		shownNotification_Half = True
	# if load is less than 10% and no notification already send
	if load < 10 and not shownNotification_LessTen:
		print("less 10%")
		trycon.showMessage("Logitech g933", "Less than 10% battery\n Please charge!", icon)
		resetNotifications()
		shownNotification_LessTen = True
	# set progressBar value
	progressBar.setValue(int(load))

def mousePressed(event):
	#mousePressEvent
	global m_nMouseClick_X_Coordinate
	global m_nMouseClick_Y_Coordinate
	m_nMouseClick_X_Coordinate = event.x
	m_nMouseClick_Y_Coordinate = event.y

def mouseMoved(event):
	global m_nMouseClick_X_Coordinate
	global m_nMouseClick_Y_Coordinate
	window.move(event.globalX(), event.globalY())

def runTimer():
	global shownNotification_Offline
	loadst = getLoadState()
	notificationLessLoad(loadst)
	if len(loadst) > 0:
		label.setText(loadst)
		if shownNotification_Offline:
			resetNotifications()
			timer.setInterval(2000)
			trycon.showMessage("Logitech g933", "I am back mate!\nThanks for using me ;-)", icon)
			progressBar.show()
	else:
		label.setText("turned off")
		progressBar.hide()
		timer.setInterval(5000)

@pyqtSlot(QSystemTrayIcon.ActivationReason)
def tryConActivated(reason):
        if reason == QSystemTrayIcon.DoubleClick:
            if window.isHidden():
                window.show()
            else:
                window.hide()

app = QApplication([])
icon = QIcon(iconFile)
window = QWidget()
layout = QVBoxLayout()

labelTitle = QLabel("Logitech G933")
layout.addWidget(labelTitle)
label = QLabel(getLoadState())
layout.addWidget(label)

progressBar = QProgressBar()
layout.addWidget(progressBar)

trycon = QSystemTrayIcon(icon, parent=app)
trycon.activated.connect(tryConActivated)
trycon.show()
trycon.showMessage("Logitech G933", "Let me know, if you want to see something!", icon)

tryconMenu = QMenu()
exitAction = tryconMenu.addAction('Exit')
exitAction.triggered.connect(app.quit)

trycon.setContextMenu(tryconMenu)

window.mousePressEvent = mousePressed
window.mouseMoveEvent = mouseMoved
window.setLayout(layout)
window.setWindowFlags(Qt.FramelessWindowHint)
#window.setWindowFlags(Qt.WindowTitleHint)
#window.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.WindowMinimizeButtonHint)

timer = QTimer()
timer.timeout.connect(runTimer)
timer.start(2000)

window.show()
window.setWindowTitle("Logitech G933")

window.setStyleSheet("background-color: rgba(255,255,255,0); color: white")
label.setStyleSheet("background-color: rgba(0,0,0,0); color:red;")
progressBar.setStyleSheet("background-color: #05B8CC; color: white;")

app.exec_()
sys.exit()
