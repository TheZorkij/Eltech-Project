# Модуль, содержащий объявления всех классов, используемых в курсовой работе


# Баовый класс для всех элементов
class Element:
    Name = None  # Имя элемента
    Voltage = None  # Напряжение
    Amperage = None  # Сила тока
    To = None  # Указатель на узел, в который течет ток (он же -)
    From = None  # Указатель на узел из которого вытекает ток (он же +)

    def set_to(self, t):
        self.To = t

    def set_from(self, f):
        self.From = f


# Класс для источников тока
class I(Element):
    def __init__(self, n, a):
        self.Name = n
        self.Amperage = a


# Класс для источников напряжения
class V(Element):
    def __init__(self, n, v):
        self.Name = n
        self.Voltage = v


# Класс для R-элементов
class R(Element):
    Resistance = None  # Сопротивление

    def __init__(self, n, r):
        self.Name = n
        self.Resistance = r


# Класс для C-элементов
class C(Element):
    Capacity = None  # Ёмкость

    def __init__(self, n, c):
        self.Name = n
        self.Capacity = c


# Класс для L-элементов
class L(Element):
    Inductance = None  # Индуктивность

    def __init__(self, n, i):
        self.Name = n
        self.Inductance = i


# Класс для узлов
class Node:
    Voltage = None
    Key = None  # Ключ узла (номер)
    To = []  # Куда вытекает ток из узла
    From = []  # Откуда втекает ток в узел

    def __init__(self, k):
        self.Key = k

    def set_to(self, t):
        self.To.append(t)

    def set_from(self, f):
        self.From.append(f)

    def set_voltage(self, v):
        self.Voltage = v

# Класс для цепи
class Chain:
    Nodes = []  # Список узлов в цепи (включая устранимые)
    Nodes_count = None  # Количество узлов в цепи (включая устранимые)
    Elements = []   # Список элементов цепи
    Elements_count = None   # Количество элементов в цепи