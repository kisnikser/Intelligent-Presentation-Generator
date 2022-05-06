#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QLabel, QWidget, QToolTip
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QMovie, QFont

from tkinter import Tk # библиотка для работы с всплывающими окнами
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os
import time
import threading

def consuming_work(arg1, arg2):
    import time
    print(arg1, arg2)
    time.sleep(5)                               #  Какая-то трудоемкая задача
    print("finish")


class WorkerMessageBox(QtWidgets.QMessageBox):
    started  = QtCore.pyqtSignal()
    finished = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.finished.connect(self.accept)
        self.move(820, 420)


    def execute(self, func, args):
        threading.Thread(target=self._execute, args=(func, args,), daemon=True).start()
        return self.exec_()

    def _execute(self, func, args):
        self.started.emit()
        func(*args)                             #  Вызываем трудоемкую задачу  
        self.finished.emit()



        
class Ui_mainWindow(object):
        # главный метод
        def setupUi(self, mainWindow):
            mainWindow.setObjectName("mainWindow")
            mainWindow.setEnabled(True)
            mainWindow.resize(800, 600)
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(10)
            font.setBold(False)
            font.setWeight(50)
            mainWindow.setFont(font)
            mainWindow.setStyleSheet("background-color: rgb(255, 255, 255);")
            self.centralwidget = QtWidgets.QWidget(mainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.generate = QtWidgets.QPushButton(self.centralwidget)
            self.generate.setGeometry(QtCore.QRect(590, 490, 151, 41))
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.generate.setFont(font)
            self.generate.setStyleSheet("background-color: rgb(51, 51, 178);\n"
    "color: rgb(230, 230, 230);")
            self.generate.setToolTip("Сгенерировать презентацию")
            
            QToolTip.setFont(QFont('CMU Sans Serif', 10))
            
            self.generate.setObjectName("generate")

            self.choose = QtWidgets.QPushButton(self.centralwidget)
            self.choose.setGeometry(QtCore.QRect(50, 490, 151, 41))
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.choose.setFont(font)
            self.choose.setStyleSheet("background-color: rgb(51, 51, 178);\n"
    "color: rgb(230, 230, 230);\n"
    "")
            self.choose.setObjectName("choose")
            self.choose.setToolTip("Выбрать документ для создания презентации")

            self.label_c1 = QtWidgets.QLabel(self.centralwidget)
            self.label_c1.setGeometry(QtCore.QRect(0, 0, 841, 25))
            self.label_c1.setStyleSheet("background-color: rgb(5, 12, 145);\n"
    "background-color: rgb(25, 25, 89);")
            self.label_c1.setObjectName("label_c1")
            self.label_IPG = QtWidgets.QLabel(self.centralwidget)
            self.label_IPG.setGeometry(QtCore.QRect(0, 40, 841, 51))
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(14)
            self.label_IPG.setFont(font)
            self.label_IPG.setStyleSheet("background-color: rgb(97, 139, 216);\n"
    "background-color: rgb(51, 51, 178);")
            self.label_IPG.setObjectName("label_IPG")
            self.label_c2 = QtWidgets.QLabel(self.centralwidget)
            self.label_c2.setGeometry(QtCore.QRect(0, 20, 841, 23))
            self.label_c2.setStyleSheet("background-color: rgb(67, 0, 202);\n"
    "background-color: rgb(38, 38, 134);")
            self.label_c2.setText("")
            self.label_c2.setObjectName("label_c2")
            self.label_c1_d = QtWidgets.QLabel(self.centralwidget)
            self.label_c1_d.setGeometry(QtCore.QRect(0, 560, 841, 41))
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(10)
            self.label_c1_d.setFont(font)
            self.label_c1_d.setStyleSheet("background-color: rgb(5, 12, 145);\n"
    "background-color: rgb(25, 25, 89);")
            self.label_c1_d.setText("")
            self.label_c1_d.setObjectName("label_c1_d")
            self.instruct = QtWidgets.QPushButton(self.centralwidget)
            self.instruct.setGeometry(QtCore.QRect(249, 489, 301, 41))
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.instruct.setFont(font)
            self.instruct.setStyleSheet("background-color: rgb(51, 51, 178);\n"
    "color: rgb(230, 230, 230);")
            self.instruct.setObjectName("instruct")
            self.save_as = QtWidgets.QPushButton(self.centralwidget)
            self.save_as.setGeometry(QtCore.QRect(250, 440, 300, 30))
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(12)
            font.setBold(True)
            font.setWeight(75)
            self.save_as.setFont(font)
            self.save_as.setStyleSheet("background-color: rgb(51, 51, 178);\n"
    "\n"
    "color: rgb(230, 230, 230);\n"
    "")
            self.save_as.setToolTip("Сохранить документ")
            
            icon = QtGui.QIcon.fromTheme("pip")
            self.save_as.setIcon(icon)
            self.save_as.setAutoDefault(False)
            self.save_as.setDefault(False)
            self.save_as.setFlat(False)
            self.save_as.setObjectName("save_as")
            self.line_1 = QtWidgets.QFrame(self.centralwidget)
            self.line_1.setGeometry(QtCore.QRect(0, 470, 841, 20))
            self.line_1.setFrameShape(QtWidgets.QFrame.HLine)
            self.line_1.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_1.setObjectName("line_1")
            self.output = QtWidgets.QLabel(self.centralwidget)
            self.output.setGeometry(QtCore.QRect(30, 140, 739, 31))
            font = QtGui.QFont()
            font.setFamily("CMU Sans Serif")
            font.setPointSize(12)
            font.setBold(False)
            font.setItalic(False)
            font.setUnderline(False)
            font.setWeight(50)
            font.setStrikeOut(False)
            self.output.setFont(font)
            self.output.setStyleSheet("background-color: rgb(38, 38, 134);")
            self.output.setFrameShape(QtWidgets.QFrame.StyledPanel)
            self.output.setObjectName("output")

            self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
            self.textEdit.setGeometry(QtCore.QRect(30, 170, 739, 259))
            font = QtGui.QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(12)
            self.textEdit.setFont(font)
            self.textEdit.setStyleSheet("background-color: rgb(233, 233, 243);")
            self.textEdit.setObjectName("textEdit")
            self.label_c2_d = QtWidgets.QLabel(self.centralwidget)
            self.label_c2_d.setGeometry(QtCore.QRect(0, 540, 841, 21))
            self.label_c2_d.setStyleSheet("background-color: rgb(67, 0, 202);\n"
    "background-color: rgb(38, 38, 134);")
            self.label_c2_d.setText("")
            self.label_c2_d.setObjectName("label_c2_d")
            self.line_2 = QtWidgets.QFrame(self.centralwidget)
            self.line_2.setGeometry(QtCore.QRect(0, 110, 841, 16))
            self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
            self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
            self.line_2.setObjectName("line_2")
            self.label_cl = QtWidgets.QLabel(self.centralwidget)
            self.label_cl.setGeometry(QtCore.QRect(50, 530, 151, 10))
            self.label_cl.setStyleSheet("background-color: rgb(233, 233, 243);")
            self.label_cl.setText("")
            self.label_cl.setObjectName("label_cl")
            self.label_cr = QtWidgets.QLabel(self.centralwidget)
            self.label_cr.setGeometry(QtCore.QRect(590, 530, 151, 10))
            self.label_cr.setStyleSheet("background-color: rgb(233, 233, 243);")
            self.label_cr.setText("")
            self.label_cr.setObjectName("label_cr")
            self.label_cm = QtWidgets.QLabel(self.centralwidget)
            self.label_cm.setGeometry(QtCore.QRect(250, 530, 301, 10))
            self.label_cm.setStyleSheet("background-color: rgb(233, 233, 243);")
            self.label_cm.setText("")
            self.label_cm.setObjectName("label_cm")
            mainWindow.setCentralWidget(self.centralwidget)
            self.menubar = QtWidgets.QMenuBar(mainWindow)
            self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
            self.menubar.setObjectName("menubar")
            mainWindow.setMenuBar(self.menubar)
    
            self.retranslateUi(mainWindow)
            QtCore.QMetaObject.connectSlotsByName(mainWindow)
            self.add_functions()

            self.is_chosen = False
            self.is_saved = False

        def retranslateUi(self, mainWindow):
            _translate = QtCore.QCoreApplication.translate
            mainWindow.setWindowTitle(_translate("mainWindow", "Intelligent Presentation Generator"))
            self.generate.setText(_translate("mainWindow", "Generate "))
            self.choose.setText(_translate("mainWindow", "Choose file"))

            self.label_IPG.setText(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "</style></head><body style=\" font-family:\'CMU Sans Serif\'; font-size:14pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-family:\'MS Shell Dlg 2\'; color:#e6e6e6;\">   Intelligent Presentation Generator</span></p></body></html>"))
            self.instruct.setText(_translate("mainWindow", "Instructions for use"))
            self.save_as.setText(_translate("mainWindow", "Save as"))
            self.output.setText(_translate("mainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
    "p, li { white-space: pre-wrap; }\n"
    "</style></head><body style=\" font-family:\'CMU Sans Serif\'; font-size:12pt; font-weight:400; font-style:normal;\">\n"
    "<p style=\" margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600; color:#e6e6e6;\">  Welcome</span></p></body></html>"))


        def add_functions(self):
            self.choose.clicked.connect(self.browse_folder)
            self.save_as.clicked.connect(self.file_save_as)   
            self.generate.clicked.connect(self.generate_presentaion)
            self.instruct.clicked.connect(self.instruction)
        # функция загрузки файла через диалоговое окно
        def browse_folder(self):
            Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
            self.filename = askopenfilename(filetypes=(("TXT files", "*.txt"),
                    ("All files", "*.*"))) # show an "Open" dialog box and return the path to the selected file

        def file_save_as(self):
                Tk().withdraw() # we don't want a full GUI, so keep the root window from appearing
                file_name = asksaveasfilename(initialfile = ".txt", filetypes=(("TXT files", "*.txt"),
                            ("All files", "*.*")))
                if file_name:
                    file = open(file_name, 'w', encoding = "utf-8")
                    text = self.textEdit.toPlainText()
                    file.write(text)
                    file.close()

        def generate_presentaion(self):
            print(self.filename)
            print(type(self.filename))
            cmd = "python ..\\topic_modelling\\slides_partition.py " + self.filename
            print(cmd)
            os.system(cmd)

        def instruction(self):
            inst = QMessageBox()
            inst.setWindowTitle("Instructions for use")
            inst.setText("Read the instructions before starting work")
            inst.setIcon(QMessageBox.Information)#есть множество шаблонов иконок всплывающих окон
            #функционал встроенных кнопок пока ограничен просто закрытием окна
            inst.setStandardButtons(QMessageBox.Ok)

            #error.setInformativeText("This action can't be performed twice")
            #вывод полной информации ошибки
            inst.setDetailedText("just do it")

            inst.exec_()
        
    
    
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    
   
    
    #создание загрузочного экрана
    msgBox = WorkerMessageBox()
    msgBox.setWindowTitle("Working ....")
    msgBox.setText("Работает, пожалуйста, подождите ...")
    msgBox.setStandardButtons(QtWidgets.QMessageBox.NoButton)        

    msgBox.execute(consuming_work, ["Stack", "Overflow"])
    
    mainWindow = QtWidgets.QMainWindow()
    ui = Ui_mainWindow()
    ui.setupUi(mainWindow)
    
    mainWindow.show()
    sys.exit(app.exec_())


# In[ ]:





# In[ ]:




