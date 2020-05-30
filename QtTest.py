import sys
from PyQt5 import uic, QtCore, QtGui, QtWidgets

class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        # Загружаем интерфейс из ui файла
        uic.loadUi('Main.ui', self)

        #объявляем свойсва элементов формы (можно сделать и в QT Designer)
        self.lineEdit.setAlignment(QtCore.Qt.AlignRight)

        #объявляем рабочие переменные для вычислений
        self.OpenBrackets = 0
        self.calctext = ""
        self.SUMM = 0
        self.DOT = 0
        self.NumLen = 0
        self.IsCalculated = False

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

    def clear(self):
        self.OpenBrackets = 0
        self.calctext = ""
        self.SUMM = 0
        self.NumLen = 0
        self.lineEdit.setText("")
        self.IsCalculated = False

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
        print(Button.get(key))
        if (Button.get(key)!=None):
            Button.get(key).click()

    def clickValue(self):

        if (self.IsCalculated):
            self.clear()

        btntext = self.sender().text()

        #проверяем введенный символ если он первый
        if ((len(self.calctext)==0) &
                    ("0123456789(".find(btntext)!=-1)):
            self.lineEdit.insert(btntext)
            self.NumLen += 1
            if btntext=="(":
                self.OpenBrackets+=1


        #проверяем введенный символ, если он НЕ первый
        elif (len(self.calctext) > 0):

            prev = self.calctext[-1]

            if (("123456789".find(btntext) != -1) &
                        (")".find(prev) == -1)):
                self.lineEdit.insert(btntext)
                self.NumLen += 1

            elif (("0".find(btntext)!=-1) &
                        (("0)".find(prev) == -1) | (self.DOT == 1) | (self.NumLen > 1))):
                self.lineEdit.insert(btntext)
                self.NumLen += 1


            elif (("(".find(btntext)!=-1) &
                        ("+-*/(".find(prev)!=-1)):
                self.lineEdit.insert(btntext)
                self.OpenBrackets+=1
                self.NumLen = 0



            elif (("+-*/".find(btntext)!=-1) &
                        ("0123456789)".find(prev)!=-1)):
                self.lineEdit.insert(btntext)
                self.DOT = 0
                self.NumLen = 0


            elif ((")".find(btntext)!=-1) &
                        (self.OpenBrackets>0) &
                        ("0123456789)".find(prev)!=-1)):
                self.lineEdit.insert(btntext)
                self.OpenBrackets -= 1
                self.DOT = 0
                self.NumLen = 0


            elif ((".".find(btntext)!=-1) &
                        ("0123456789".find(prev)!=-1) &
                        (self.DOT==0)):
                self.lineEdit.insert(btntext)
                self.DOT=1
                self.NumLen += 1



            elif (("=".find(btntext)!=-1) &
                        ("0123456789)".find(prev)!=-1) &
                        (self.OpenBrackets==0)):
                self.SUMM = eval(self.calctext)
                self.lineEdit.setText(str(self.SUMM))
                self.IsCalculated = True
                self.NumLen = len(self.lineEdit.text())

            else:
                pass

        print(self.NumLen)
        self.calctext = self.lineEdit.text()



if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec_())



