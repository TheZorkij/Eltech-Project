# Модуль ввода электрической цепи пользователем
import Classes


# Функция создания элемента цепи
def create_element(typ):
    element = None
    if typ == 'V':
        n = input("Введите имя элемента: ")
        v = input("Введите напряжение элемента: ")
        element = Classes.V(n, v)
    elif typ == 'I':
        n = input("Введите имя элемента: ")
        a = input("Введите силу тока элемента: ")
        element = Classes.I(n, a)
    elif typ == 'R':
        n = input("Введите имя элемента: ")
        r = input("Введите сопротивление элемента: ")
        element = Classes.R(n, r)
    elif typ == 'C':
        n = input("Введите имя элемента: ")
        c = input("Введите ёмкость элемента: ")
        element = Classes.C(n, c)
    elif typ == 'L':
        n = input("Введите имя элемента: ")
        l = input("Введите индуктивность элемента: ")
        element = Classes.L(n, l)
    return element


# Функция создания электрической цепи
def create_chain():
    chain = Classes.Chain
    chain.Nodes_count = int(input("Введите количество узлов в цепи: "))
    i = 0
    while i < chain.Nodes_count:
        chain.Nodes[i] = Classes.Node(i + 1)
    chain.Elements_count = int(input("Введите количество элементов в цепи: "))
    i = 0
    while i < chain.Elements_count:
        typ = input("Введите тип элемента (V/I/R/C/L): ")
        chain.Elements[i] = create_element(typ)
    for i in chain.Nodes:
        while 1:
            print("Введите номер элемента, в который втекает ток из", i, "-го узла: ")
            number = input()
            chain.Nodes[i].set_to(chain.Elements[number - 1])
            chain.Elements[number - 1].set_from(chain.Nodes[i])
            answer = input("Из узла вытекает ток ещё в одном направлении?")
            if answer == 'Нет' or answer == 'нет':
                break
        while 1:
            print("Введите номер элемента, из которого втекает ток в", i, "-й узел: ")
            number = input()
            chain.Nodes[i].set_from(chain.Elements[number - 1])
            chain.Elements[number - 1].set_to(chain.Nodes[i])
            answer = input("В узел втекает ещё ток?")
            if answer == 'Нет' or answer == 'нет':
                break
    return chain


__all__ = {'Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.Chain,
           Classes.Node}