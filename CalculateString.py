
Digits = ('0','1','2','3','4','5','6','7','8','9','.')
Operations = ("+","-","*","/","^")
Priority = {'(':0,'+':1,'-':1,'*':2,'/':2,'^':3}

def is_digit(string):
    if string.isdigit():
       return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False

#преобразуем строку в последвательный список чисел и операций
def GetListOfString (Evaluation : str):
    Lexem = []
    Temp = ""
    Last = ""
    for i in Evaluation:
        if ((i in Digits) and ((Last in Digits) or Last =="")):
            Temp += str(i)
            Last = str(i)
        elif (i in Operations or (i=='(' or i == ')')) and (Temp != ""):
            Lexem.append(Temp)
            Lexem.append(i)
            Temp = ""
            Last = ""
        elif (i in Operations or (i=='(' or i == ')')) and (Temp == ""):
            Lexem.append(i)
    if Temp!="": Lexem.append(Temp)
    return Lexem

#реализуем обратную польскую нотацию с использованием стека
def ReversePolandNotation(Lexem):
    Stack = []
    Notation = []

    for i in Lexem:
        if is_digit(i):
            Notation.append(i)
        elif i=="(":
            Stack.append(i)
        elif i==")":
            P = Stack.pop()
            while P !="(":
                Notation.append(P)
                P = Stack.pop()
        elif i in Operations:
            if not Stack:
                Stack.append(i)
            else:
                while (Priority.get(i)<=Priority.get(Stack[-1])):
                    Notation.append(Stack.pop())
                    if not Stack: break
                Stack.append(i)
    while Stack: Notation.append(Stack.pop())
    return Notation

#вычисляем выражение по обратной польской нотации
def CalculateNotation (Notation):
    Calculation = []

    for i in Notation:
        if is_digit(i):
            Calculation.append(float(i))
        else:
            P2=Calculation.pop()
            P1=Calculation.pop()
            if i == "+":
                Calculation.append(P1+P2)
            elif i == "-":
                Calculation.append(P1-P2)
            elif i == "*":
                Calculation.append(P1*P2)
            elif i == "/":
                Calculation.append(P1/P2)
            elif i == "^":
                Calculation.append(P1**P2)
    return Calculation[0]

#пакуем все функции в одну
def CalculateString (STR):
    result = CalculateNotation(ReversePolandNotation(GetListOfString(STR)))
    return result

