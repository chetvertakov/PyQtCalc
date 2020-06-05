import sys, os
from PyQt5 import uic, QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

#Get absolute path to resource, works for dev and for PyInstaller
def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        path = resource_path("res\Main.ui")
        #print("THIS IS IT:   "+path)
        # Загружаем интерфейс из ui файла
        uic.loadUi(path, self)

        #объявляем свойсва элементов формы (можно сделать и в QT Designer)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight)

        #объявляем рабочие переменные для вычислений
        self.calctext = ""
        self.SUMM = 0
        self.DOT = 0
        self.NumLen = 0
        self.IsCalculated = False
        self.OpenBrackets = 0

        #загружаем обработчики кликов
        self.Btn1.clicked.connect(self.clickValue)
        self.Btn2.clicked.connect(self.clickValue)
        self.Btn3.clicked.connect(self.clickValue)
        self.Btn4.clicked.connect(self.clickValue)
        self.Btn5.clicked.connect(self.clickValue)
        self.Btn6.clicked.connect(self.clickValue)
        self.Btn7.clicked.connect(self.clickValue)
        self.Btn8.clicked.connect(self.clickValue)
        self.Btn9.clicked.connect(self.clickValue)
        self.Btn0.clicked.connect(self.clickValue)
        self.BtnPlus.clicked.connect(self.clickValue)
        self.BtnMinus.clicked.connect(self.clickValue)
        self.BtnBracketC.clicked.connect(self.clickValue)
        self.BtnBracketO.clicked.connect(self.clickValue)
        self.BtnDot.clicked.connect(self.clickValue)
        self.BtnMulti.clicked.connect(self.clickValue)
        self.BtnSplit.clicked.connect(self.clickValue)
        self.BtnEqual.clicked.connect(self.clickValue)

        self.BtnClear.clicked.connect(self.clear)
        self.BtnErase.clicked.connect(self.erase)
        self.actionExit.triggered.connect(self.close)


    def closeEvent(self, a0: QtGui.QCloseEvent):
        msg = QMessageBox()
        msg.setText("Вы точно хотите выйти?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        _exit = msg.exec()
        if _exit == QMessageBox.No:
            a0.ignore()



    #очистка поля ввода
    def clear(self):
        self.OpenBrackets = 0
        self.calctext = ""
        self.SUMM = 0
        self.NumLen = 0
        self.lineEdit.setText("")
        self.IsCalculated = False

    #удаление последнего символа
    def erase(self):
        if self.calctext == "":
            return
        else:
            if ("0123456789".find(self.calctext[-1])!=-1):
                self.calctext = self.calctext[:-1]
                self.NumLen-=1
            elif ("(".find(self.calctext[-1])!=-1):
                self.calctext = self.calctext[:-1]
                self.OpenBrackets-=1
            elif (")".find(self.calctext[-1]) != -1):
                self.calctext = self.calctext[:-1]
                self.OpenBrackets += 1
            elif ("+-*/".find(self.calctext[-1]) != -1):
                self.calctext = self.calctext[:-1]

            self.lineEdit.setText(self.calctext)


    #ввод значений с клавиатуры (эмуляцию нажатия кнопок)
    def keyPressEvent(self, a0: QtGui.QKeyEvent):
        text = a0.text()
        key = a0.key()
        print(text + " - " + str(key))
        Button = {
            48: self.Btn0,
            49: self.Btn1,
            50: self.Btn2,
            51: self.Btn3,
            52: self.Btn4,
            53: self.Btn5,
            54: self.Btn6,
            55: self.Btn7,
            56: self.Btn8,
            57: self.Btn9,
            40: self.BtnBracketO,
            41: self.BtnBracketC,
            42: self.BtnMulti,
            43: self.BtnPlus,
            45: self.BtnMinus,
            46: self.BtnDot,
            47: self.BtnSplit,
            61: self.BtnEqual,
            16777220: self.BtnEqual,
            16777221: self.BtnEqual,
            16777223: self.BtnClear,
        }
        if (Button.get(key)!=None):
            Button.get(key).click()

    def clickValue(self):

        #если сейчас отображается результат вычисления то при новом вводе поле очищается
        if (self.IsCalculated):
            self.clear()

        btntext = self.sender().text()

        #проверяем введенный символ если он первый
        if ((len(self.calctext)==0) and
                    ("0123456789(".find(btntext)!=-1)):
            self.calctext += btntext
            self.NumLen += 1
            if btntext=="(":
                self.OpenBrackets+=1
            self.lineEdit.setText(self.calctext)

        #проверяем введенный символ, если он НЕ первый
        elif (len(self.calctext) > 0):

            prev = self.calctext[-1]

            if (("123456789".find(btntext) != -1) &
                        (")".find(prev) == -1)):
                if (prev == "0" and self.NumLen == 1):
                    self.calctext = self.calctext[:-1]
                    self.calctext += btntext
                else:
                    self.calctext += btntext
                    self.NumLen += 1

            elif (("0".find(btntext)!=-1) &
                        (("0)".find(prev) == -1) | (self.DOT == 1) | (self.NumLen > 1))):
                self.calctext += btntext
                self.NumLen += 1


            elif (("(".find(btntext)!=-1) &
                        ("+-*/(".find(prev)!=-1)):
                self.calctext += btntext
                self.OpenBrackets+=1
                self.NumLen = 0



            elif (("+-*/".find(btntext)!=-1) &
                        ("0123456789)".find(prev)!=-1)):
                self.calctext += btntext
                self.DOT = 0
                self.NumLen = 0


            elif ((")".find(btntext)!=-1) &
                        (self.OpenBrackets>0) &
                        ("0123456789)".find(prev)!=-1)):
                self.calctext += btntext
                self.OpenBrackets -= 1
                self.DOT = 0
                self.NumLen = 0


            elif ((".".find(btntext)!=-1) &
                        ("0123456789".find(prev)!=-1) &
                        (self.DOT==0)):
                self.calctext += btntext
                self.DOT=1
                self.NumLen += 1



            elif (("=".find(btntext)!=-1) &
                        ("0123456789)".find(prev)!=-1) &
                        (self.OpenBrackets==0)):
                try:
                    self.SUMM = eval(self.calctext)
                except Exception as e:
                    self.SUMM = e

                self.calctext = str(self.SUMM)
                self.IsCalculated = True
                self.NumLen = len(self.lineEdit.text())

            else:
                pass

        self.lineEdit.setText(self.calctext)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())



