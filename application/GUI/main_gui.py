from pytemplates.mainwindow import *
import sys
from PyQt5 import QtWidgets, QtCore
import numpy as np
import time
import matplotlib
from utils import *
import os
import serial

class main_gui(Ui_MainWindow):
    def __init__(self, window):
        self.setupUi(window)
        self.textBrowser.append('initializing GUI')
        self.pushButtonStart.clicked.connect(self.start_device)
        self.pushButtonStop.clicked.connect(self.stop_device)
        self.pushButtonCalibrate.clicked.connect(self.calibrate)
        self.progressBar.setValue(0)
        self.pushButtonStop.setEnabled(False)

    def start_device(self):
        self.textBrowser.append('starting data collection')
        self.pushButtonStart.setEnabled(False)
        self.pushButtonStop.setEnabled(True)
    def stop_device(self):
        self.textBrowser.append('stopping data collection')
        if self.checkBoxSave.isChecked():
            self.textBrowser.append('saving data')
        self.pushButtonStop.setEnabled(False)
        self.pushButtonStart.setEnabled(True)
    def calibrate(self):
        self.textBrowser.append('calibrating readings')
        name = 'Concentration'
        value = np.random.randint(1,100)
        self.listWidgetMelanin.addItem(f'{name}: {value}')
        self.progress()
        self.Melanin.setDecMode()
        self.Melanin.setDigitCount(3)
        self.Melanin.display(value)
    def progress(self):
        start = time.time()
        while time.time() - start <= 4:
            percent_complete = ((time.time() - start)/4) * 100
            self.progressBar.setValue(percent_complete)
        self.progressBar.setValue(100)
    def _print_qprocess_std_out(self, proc):
        txt = proc.readAllStandardOutput().data().decode('utf8')
        self.textBrowser.append(txt)
    def show_serial_ports(self):
        pass
    def _get_serial_ports(self):
        ports = find_serial_ports()
        return ports

    def update_plot(self):
        # Drop off the first y element, append a new one.
        self.ydata = self.ydata[1:] + [random.randint(0, 10)]
        self.canvas.axes.cla()  # Clear the canvas.
        self.canvas.axes.plot(self.xdata, self.ydata, 'r')
        # Trigger the canvas to update and redraw.
        self.canvas.draw()

    # TODO: identify available ports and let user choose
    # TODO: Create refresh button
    # TODO: save data in buffer size len
    # TODO: os.mkdir to create known directory for sample data
    # TODO: consider how bluetooth will work
    # TODO: connection interface tab
    # TODO: Highlight sections of graph that indicate problem
    # TODO: Create version for consumer in addition to developer

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = main_gui(MainWindow)
MainWindow.show()
app.exec_()