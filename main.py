#!/usr/bin/python3
"""
	LogiTech g933 GUI by ksaadDE
	
	Thanks for g933-utils  https://github.com/ashkitten/g933-utils (@ashkitten)
	icon: Icon made by Freepik perfect from www.flaticon.com"
	bing.mp3 https://freesound.org/data/previews/91/91926_7037-lq.mp3
"""
import sys, subprocess
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import * 

iconFile = "logitech.png"

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
		shownNotification_Full = True
	# if load is less than 45 and  greater than 10% and no notification send
	if round(load) < 45 and round(load) > 10 and not shownNotification_Half:
		print("less than half")
		trycon.showMessage("Logitech g933", "Halftime! 45%", icon)
		shownNotification_Half = True
	# if load is less than 10% and no notification already send
	if load < 10 and not shownNotification_LessTen:
		print("less 10%")
		trycon.showMessage("Logitech g933", "Less than 10% battery\n Please charge!", icon)
		shownNotification_LessTen = True
	# set progressBar value
	progressBar.setValue(int(load))
def runTimer():
	global shownNotification_Offline
	loadst = getLoadState()
	notificationLessLoad(loadst)
	if len(loadst) > 0:
		label.setText(loadst)
		if shownNotification_Offline:
			shownNotification_Offline = False
			trycon.showMessage("Logitech g933", "I am back mate!\nThanks for using me ;-)", icon)
			progressBar.show()
	else:
		label.setText("turned off")
		progressBar.hide()

app = QApplication([])
icon = QIcon(iconFile)
window = QWidget()
layout = QVBoxLayout()

label = QLabel(getLoadState())
layout.addWidget(label)

progressBar = QProgressBar()
layout.addWidget(progressBar)

trycon = QSystemTrayIcon(icon, parent=app)
trycon.show()
trycon.showMessage("Logitech G933", "Let me know, if you want to see something!", icon)

tryconMenu = QMenu()
exitAction = tryconMenu.addAction('Exit')
exitAction.triggered.connect(app.quit)

trycon.setContextMenu(tryconMenu)

window.setLayout(layout)

#window.resize(600,600)
window.setWindowFlags(Qt.WindowStaysOnTopHint)

timer = QTimer()
timer.timeout.connect(runTimer)
timer.start(2000)

window.show()
window.setWindowTitle("Logitech G933")
window.setStyleSheet("background-color: rgba(255,255,255,0)")
label.setStyleSheet("background-color: rgba(0,0,0,0); color:red;")
progressBar.setStyleSheet("background-color: #05B8CC; color: white;")
app.exec_()
sys.exit()
