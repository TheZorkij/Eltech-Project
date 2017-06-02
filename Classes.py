# Модуль, содержащий объявления всех классов, используемых в курсовой работе


# Базовый класс для всех элементов
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

    def set_voltage(self, v):
        self.Voltage = v

    def set_amperage(self, a):
        self.Amperage = a

    def get_name(self):
        return self.Name


# Класс для источников тока
class I(Element):
    def __init__(self, n, a, i):
        self.Name = n
        self.Amperage = a
        self.Num = i


# Класс для источников напряжения
class V(Element):
    def __init__(self, n, v, i):
        self.Name = n
        self.Voltage = v
        self.Num = i


# Класс для R-элементов
class R(Element):
    Resistance = None  # Сопротивление

    def __init__(self, n, r, i):
        self.Name = n
        self.Resistance = r
        self.Num = i

# Класс для нагрузки
class H(Element):
    Resistance = None  # Сопротивление

    def __init__(self, n, r, i):
        self.Name = n
        self.Resistance = r
        self.Num = i

# Класс для C-элементов
class C(Element):
    Capacity = None  # Ёмкость

    def __init__(self, n, c, i):
        self.Name = n
        self.Capacity = c
        self.Num = i


# Класс для L-элементов
class L(Element):
    Inductance = None  # Индуктивность

    def __init__(self, n, c, i):
        self.Name = n
        self.Inductance = c
        self.Num = i


# Класс для холостого хода
class Idling(Element):
    From = None
    Amperage = 0

    def __init__(self, f):
        self.From = f


# Класс для короткого замыкания
class SC(Element):
    Voltage = 0
    From = None
    To = None

    def __init__(self, t, f):
        self.From = f
        self.To = t


# Класс для узлов
class Node:
    #Voltage = None
    #Key = None  # Ключ узла (номер)
    #To = None  # Куда вытекает ток из узла
    #From = None  # Откуда втекает ток в узел

    def __init__(self, k):
        self.Key = k
        self.Voltage = None
        self.To = None
        self.From = None

    def set_to(self, t):
        self.To.append(t)

    def set_from(self, f):
        self.From.append(f)

    def set_voltage(self, v):
        self.Voltage = v


# Класс для цепи
class Chain:
    #Nodes = None  # Список узлов в цепи (включая устранимые)
    #Nodes_count = None  # Количество узлов в цепи (включая устранимые)
    #Elements = None  # Список элементов цепи
    #Elements_count = None  # Количество элементов в цепи

    def __init__(self, n, e):
        self.Nodes = []
        self.Elements = []
        self.Nodes_count = n
        self.Elements_count = e

    """def __del__(self):
        print("aaa")
        i = 0
        while i < self.Nodes_count:
            del self.Nodes[i].To
            del self.Nodes[i].From
            i += 1
        del self.Nodes
        del self.Elements
        self.Elements_count = None
        self.Nodes_count = None
        del self"""

    @staticmethod
    def output_chain(chain):
        for i in range(0, chain.Elements_count):
            print()
            print(i, end='')
            print(chain.Elements[i].From.Key, end='')
            print(chain.Elements[i].To.Key, end=' ')
            print(chain.Elements[i].Name, end=' ')
            print("Напр:", end=' ')
            if chain.Elements[i].Voltage is None:
                print("?", end=' ')
            else:
                print(chain.Elements[i].Voltage, "В", end=' ')
            print("Ток:", end=' ')
            if chain.Elements[i].Amperage is None:
                print("?", end=' ')
            else:
                print(chain.Elements[i].Amperage, "А", end=' ')
            if hasattr(chain.Elements[i], 'Resistance'):
                print("Сопротивление: ", chain.Elements[i].Resistance, "Ом", end=' ')
            if hasattr(chain.Elements[i], 'Capacity'):
                print("Эл.ёмкость: ", chain.Elements[i].Capacity, "Ф", end=' ')
            if hasattr(chain.Elements[i], 'Inductance'):
                print("Индуктивность: ", chain.Elements[i].Inductance, "Гн", end='')
        print()
        #print(chain.Nodes[1].To)
        #print(Chain.Nodes_count)
