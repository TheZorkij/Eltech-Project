# Модуль ввода электрической цепи пользователем
import Classes


# Функция создания элемента цепи
def create_element(typ):
    element = None
    if typ == 'V':
        n = input("Введите имя элемента: ")
        v = int(input("Введите напряжение элемента: "))
        element = Classes.V(n, v)
    elif typ == 'I':
        n = input("Введите имя элемента: ")
        a = int(input("Введите силу тока элемента: "))
        element = Classes.I(n, a)
    elif typ == 'R':
        n = input("Введите имя элемента: ")
        r = int(input("Введите сопротивление элемента: "))
        element = Classes.R(n, r)
    elif typ == 'C':
        n = input("Введите имя элемента: ")
        c = int(input("Введите ёмкость элемента: "))
        element = Classes.C(n, c)
    elif typ == 'L':
        n = input("Введите имя элемента: ")
        l = int(input("Введите индуктивность элемента: "))
        element = Classes.L(n, l)
    return element


# Функция создания электрической цепи
def create_chain():
    chain = Classes.Chain
    chain.Nodes_count = int(input("Введите количество узлов в цепи: "))
    i = 0
    while i < chain.Nodes_count:
        chain.Nodes.append(i)
        # Classes.Node.append(i)
        chain.Nodes[i] = Classes.Node(i + 1)
        chain.Nodes[i].To = []
        chain.Nodes[i].From = []
        i += 1
    chain.Elements_count = int(input("Введите количество элементов в цепи: "))
    i = 0
    while i < chain.Elements_count:
        typ = input("Введите тип элемента (V/I/R/C/L): ")
        chain.Elements.append(i)
        chain.Elements[i] = create_element(typ)
        i += 1
    for i in range(0, chain.Nodes_count):
        while 1:
            print("Введите номер элемента, в который втекает ток из", i, "-го узла: ")
            number = int(input())
            chain.Nodes[i].set_to(chain.Elements[number - 1])
            chain.Elements[number - 1].set_from(chain.Nodes[i])
            answer = input("Из узла вытекает ток ещё в одном направлении? (y/n) Ввод: ")
            if answer == 'N' or answer == 'n':
                break
        while 1:
            print("Введите номер элемента, из которого втекает ток в", i, "-й узел: ")
            number = int(input())
            chain.Nodes[i].set_from(chain.Elements[number - 1])
            chain.Elements[number - 1].set_to(chain.Nodes[i])
            answer = input("В узел втекает ещё ток? (y/n) Ввод: ")
            if answer == 'N' or answer == 'n':
                break
    return chain


def defaultchain():
    chain = Classes.Chain
    chain.Nodes_count = 3
    i = 0
    while i < chain.Nodes_count:
        chain.Nodes.append(Classes.Node(i + 1))
        chain.Nodes[i].To = []
        chain.Nodes[i].From = []
        i += 1

    chain.Elements_count = 5
    chain.Elements.append(Classes.R('R', 2))
    chain.Elements.append(Classes.R('R', 1))
    chain.Elements.append(Classes.V('V', 58))
    chain.Elements.append(Classes.R('R', 2))
    chain.Elements.append(Classes.R('R', 20))


    chain.Nodes[0].set_to(chain.Elements[2])
    chain.Elements[2].set_from(chain.Nodes[0])
    chain.Nodes[0].set_from(chain.Elements[0])
    chain.Elements[0].set_to(chain.Nodes[0])
    chain.Nodes[0].set_from(chain.Elements[3])
    chain.Elements[3].set_to(chain.Nodes[0])
    chain.Nodes[0].set_from(chain.Elements[4])
    chain.Elements[4].set_to(chain.Nodes[0])
    chain.Nodes[1].set_to(chain.Elements[0])
    chain.Elements[0].set_from(chain.Nodes[1])
    chain.Nodes[1].set_from(chain.Elements[1])
    chain.Elements[1].set_to(chain.Nodes[1])
    chain.Nodes[2].set_to(chain.Elements[1])
    chain.Elements[1].set_from(chain.Nodes[2])
    chain.Nodes[2].set_to(chain.Elements[3])
    chain.Elements[3].set_from(chain.Nodes[2])
    chain.Nodes[2].set_to(chain.Elements[4])
    chain.Elements[4].set_from(chain.Nodes[2])
    chain.Nodes[2].set_from(chain.Elements[2])
    chain.Elements[2].set_to(chain.Nodes[2])

    #print(chain.Nodes[0].From)

    return chain


def defaultchain2():
    chain = Classes.Chain
    chain.Nodes_count = 3
    i = 0
    while i < chain.Nodes_count:
        chain.Nodes.append(Classes.Node(i + 1))
        chain.Nodes[i].To = []
        chain.Nodes[i].From = []
        i += 1

    chain.Elements_count = 6
    chain.Elements.append(0)
    chain.Elements[0] = Classes.V('V', 15)
    chain.Elements.append(1)
    chain.Elements[1] = Classes.R('R', 2)
    chain.Elements.append(2)
    chain.Elements[2] = Classes.R('R', 1)
    chain.Elements.append(3)
    chain.Elements[3] = Classes.V('V', 58)
    chain.Elements.append(4)
    chain.Elements[4] = Classes.R('R', 2)
    chain.Elements.append(5)
    chain.Elements[5] = Classes.R('R', 20)

    chain.Nodes[0].set_to(chain.Elements[3])
    chain.Elements[3].set_from(chain.Nodes[0])

    chain.Nodes[0].set_from(chain.Elements[0])
    chain.Elements[0].set_to(chain.Nodes[0])
    chain.Elements[0].set_from(chain.Nodes[1])

    chain.Nodes[0].set_from(chain.Elements[1])
    chain.Elements[1].set_to(chain.Nodes[0])
    chain.Nodes[0].set_from(chain.Elements[4])
    chain.Elements[4].set_to(chain.Nodes[0])
    chain.Nodes[0].set_from(chain.Elements[5])
    chain.Elements[5].set_to(chain.Nodes[0])
    chain.Nodes[1].set_to(chain.Elements[1])
    chain.Elements[1].set_from(chain.Nodes[1])
    chain.Nodes[1].set_from(chain.Elements[2])
    chain.Elements[2].set_to(chain.Nodes[1])
    chain.Nodes[2].set_to(chain.Elements[2])
    chain.Elements[2].set_from(chain.Nodes[2])
    chain.Nodes[2].set_to(chain.Elements[4])
    chain.Elements[4].set_from(chain.Nodes[2])
    chain.Nodes[2].set_to(chain.Elements[5])
    chain.Elements[5].set_from(chain.Nodes[2])
    chain.Nodes[2].set_from(chain.Elements[3])
    chain.Elements[3].set_to(chain.Nodes[2])
    return chain


__all__ = {'Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.Chain,
           Classes.Node}
