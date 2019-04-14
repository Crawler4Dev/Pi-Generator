from decimal import getcontext, Decimal
import datetime
from threading import Thread

def writeToFile(path, text):
    with open(path, 'w') as file:
        file.write(text + "\n")
        file.close()

def generatePi(decimal, dialog):
    getcontext().prec = decimal + 3
    a = 1
    b = 1 / Decimal(2).sqrt()
    s = 1 / Decimal(4)
    n = 0
    lastPi = 0
    timeStart = datetime.datetime.now()
    while True:
        generationTimeStart = datetime.datetime.now()
        A = (a + b) / 2
        B = Decimal(a * b).sqrt()
        S = s - 2 ** n * (a - A) ** 2
        pi = A**2/s
        print(n + 1, ":", str(pi)[:-2])
        dialog.generation.setText("Generation: " + str(n + 1))
        a = A
        b = B
        s = S
        generationTimeEnd = datetime.datetime.now()
        dialog.genTime.setText("Generation Time: " + str(generationTimeEnd - generationTimeStart))
        n += 1
        if lastPi == pi:
            break
        lastPi = pi
    timeEnd = datetime.datetime.now()
    dialog.time.setText("Time: " + str(timeEnd - timeStart))
    dialog.generations.setText("Generations: " + str(n))
    writeToFile("pi.txt", str(lastPi)[:-2])
    return lastPi

from PyQt5 import QtWidgets, QtGui
import sys

class Dialog(object):

    def on_click(self):
        self.button.setDisabled(True)
        def gen():
            self.state.setText("State: " + "Generating...")
            self.time.setText("")
            self.generations.setText("")
            self.generation.setText("")
            self.genTime.setText("")
            pi = generatePi(self.decimal.value(), self)
            self.state.setText("State: " + "Generated ->> pi.txt")
            self.generation.setText("")
            self.genTime.setText("")
            self.button.setDisabled(False)
        Thread(target=gen).start()

    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.dialog.setWindowTitle("Pi-Generator")
        self.dialog.setWindowIcon(QtGui.QIcon("icon.png"))
        self.dialog.setFixedSize(360, 240)

        self.decimal_text = QtWidgets.QLabel(self.dialog)
        self.decimal_text.move(20, -3)
        self.decimal_text.setFixedSize(320, 30)
        self.decimal_text.setFont(QtGui.QFont("Time", 8, QtGui.QFont.Normal))
        self.decimal_text.setText("Nachkommastellen:")

        self.decimal = QtWidgets.QSpinBox(self.dialog)
        self.decimal.setMinimum(1)
        self.decimal.setMaximum(1000000000)
        self.decimal.setFixedSize(320, 30)
        self.decimal.setFont(QtGui.QFont("Time", 10, QtGui.QFont.Normal))
        self.decimal.move(20, 20)

        self.state = QtWidgets.QLabel(self.dialog)
        self.state.move(20, 80)
        self.state.setFixedSize(320, 30)
        self.state.setFont(QtGui.QFont("Time", 10, QtGui.QFont.Normal))
        self.state.setText("State: " + "Waiting")

        self.time = QtWidgets.QLabel(self.dialog)
        self.time.move(20, 100)
        self.time.setFixedSize(320, 30)
        self.time.setFont(QtGui.QFont("Time", 10, QtGui.QFont.Normal))

        self.generations = QtWidgets.QLabel(self.dialog)
        self.generations.move(20, 120)
        self.generations.setFixedSize(320, 30)
        self.generations.setFont(QtGui.QFont("Time", 10, QtGui.QFont.Normal))

        self.generation = QtWidgets.QLabel(self.dialog)
        self.generation.move(20, 140)
        self.generation.setFixedSize(320, 30)
        self.generation.setFont(QtGui.QFont("Time", 10, QtGui.QFont.Normal))

        self.genTime = QtWidgets.QLabel(self.dialog)
        self.genTime.move(20, 160)
        self.genTime.setFixedSize(320, 30)
        self.genTime.setFont(QtGui.QFont("Time", 10, QtGui.QFont.Normal))

        self.button = QtWidgets.QPushButton("Generate", self.dialog)
        self.button.move(260, 190)
        self.button.setFixedSize(80, 30)
        self.button.setFont(QtGui.QFont("Time", 10, QtGui.QFont.Normal))
        self.button.clicked.connect(self.on_click)

    def show(self):
        self.dialog.show()

app = QtWidgets.QApplication(sys.argv)
dialog = Dialog()
dialog.show()
sys.exit(app.exec_())