from PyQt5.QtWidgets import QWidget, QApplication,QMainWindow,QListWidgetItem, QMessageBox
from PyQt5.uic import  loadUi
import sys
from PyQt5 import QtCore,QtGui 
import sqlite3
#from PyQt5.QtGui import *

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()
        loadUi("main.ui",self)
        self.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.pushButton.clicked.connect(self.saveChanges)
        self.pushButton_2.clicked.connect(self.addNewTask)
        self.setWindowTitle("To DO LIST")
        self.setWindowIcon(QtGui.QIcon('download.png'))

    def calendarDateChanged(self):
        print("The calendar was changed")
        dateSelected = self.calendarWidget.selectedDate().toPyDate()
        print("Date selected: ", dateSelected)
        self.updateTaskList(dateSelected)

    def updateTaskList(self,date):
        self.listWidget.clear()
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        query = "SELECT task, completed FROM tasks WHERE date = ?"
        row = (date,)
        results = cursor.execute(query,row).fetchall()
        for result in results:
            item = QListWidgetItem(result[0])
            item.setFlags(item.flags() | QtCore.Qt.ItemIsUserCheckable)
            item.setCheckState(QtCore.Qt.Unchecked)
            if result[1] == "YES":
                    item.setCheckState(QtCore.Qt.Checked)
            elif result[1] == "NO":
                item.setCheckState(QtCore.Qt.Unchecked)
            self.listWidget.addItem(item)    

    def saveChanges(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()
        date = self.calendarWidget.selectedDate().toPyDate()

        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            task = item.text()
            if item.checkState() == QtCore.Qt.Checked:
                query = "UPDATE tasks SET completed = 'YES' WHERE task = ? AND date = ?"
            else:
                query = "UPDATE tasks SET completed = 'NO' WHERE task = ? AND date = ?"
            row = (task, date,)
            cursor.execute(query, row)
        db.commit()

        messageBox = QMessageBox()
        messageBox.setText("Changes saved.")
        messageBox.setStandardButtons(QMessageBox.Ok)
        messageBox.exec()

    def addNewTask(self):
        db = sqlite3.connect("data.db")
        cursor = db.cursor()

        newTask = str(self.lineEdit.text())
        date = self.calendarWidget.selectedDate().toPyDate()

        query = "INSERT INTO tasks(task, completed, date) VALUES (?,?,?)"
        row = (newTask, "NO", date,)

        cursor.execute(query, row)
        db.commit()
        self.updateTaskList(date)
        self.lineEdit.clear()        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec())        