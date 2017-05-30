# Модуль, вычисляющий H(S), h(t), h1(t), АЧХ(w), ФЧХ(w)

import numpy
from scipy.signal import ss2tf
import sympy
from sympy import inverse_laplace_transform, symbols

s = sympy.Symbol('s')
t = sympy.Symbol('t')


# Функция, вычисляющая H(S) по четырём матрицам и записывающая её в виде деления многочленов
def HS_calc(a, b, c, d):
    # Вычисление коэффициентов числителя и знаменателя
    [[H_num], H_den] = ss2tf(a, b, c, d)
    HS_num = ''
    HS_den = ''
    H1S_den = ''
    f = 0
    j = H_num.size-1
    # Использование символьной переменной S для представления числителя в виде многочлена
    for i in H_num:
        temp = str(i)
        if i:
            if j > 1:
                temp += '*s**' + str(j)
            else:
                if j > 0:
                    temp += '*s'
            if f:
                if i < 0:
                    HS_num += '-'
                else:
                    HS_num += '+'
            else:
                f = 1
            HS_num += temp
        j -= 1
    j = H_den.size - 1
    f = 0
    # Использование символьной переменной S для представления знаменателя в виде многочлена
    for i in H_den:
        temp = str(int(i))
        temp1 = str(int(i))
        if i:
            if j > 1:
                temp += '*s**' + str(j)
                temp1 += '*s**' + str(j + 1)
            else:
                if j > 0:
                    temp += '*s'
                    temp1 += '*s**' + str(j + 1)
                else:
                    temp1 += '*s'
            if f:
                if i < 0:
                    HS_den += '-'
                    H1S_den += '-'
                else:
                    HS_den += '+'
                    H1S_den += '+'
            else:
                f = 1
            HS_den += temp
            H1S_den += temp1
        j -= 1
    return HS_num, HS_den, H1S_den, H_num, H_den


# Функция, переводящая функции из области преобразований Лапласа во временную область
def S2t(HS):
    return inverse_laplace_transform(HS, s, t)


# Функция, вычисляющая АЧХ и ФЧХ
def FRandPR(HS_num, HS_den):
    w = numpy.linspace(1, 20, 200, dtype=complex)
    temp_num = numpy.zeros(numpy.shape(w), dtype=complex)
    temp_den = numpy.zeros(numpy.shape(w), dtype=complex)
    for i in range(0, len(HS_num)):
        temp_num = temp_num + (HS_num[i]) * (1.j * w) ** (len(HS_num) - i)
    for i in range(0, len(HS_num)):
        temp_den = temp_den + (HS_num[i]) * (1.j * w) ** (len(HS_num) - i)
    print(temp_num, temp_den)
    return numpy.abs(numpy.ndarray(shape=numpy.shape(temp_num), dtype=complex, buffer=temp_num/temp_den)), numpy.angle(numpy.ndarray(shape=numpy.shape(temp_num), dtype=complex, buffer=temp_num/temp_den))
__all__ = ['numpy']

