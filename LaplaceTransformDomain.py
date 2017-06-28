# Модуль, вычисляющий H(S), h(t), h1(t), АЧХ(w), ФЧХ(w)

import numpy
from scipy.signal import ss2tf
import sympy
from sympy import inverse_laplace_transform, symbols
import matplotlib.pyplot as plt
import SignalProcessing as SP

s = sympy.Symbol('s')
t = sympy.Symbol('t')


def talbot_inverse(f_s, t_z, M = 64):
    k = numpy.arange(M)
    # Задаём вектор значений функции дельта
    delta = numpy.zeros(M, dtype=complex)
    for i in k:
        if i != 0:
            delta[i] = 2*numpy.pi/5 * i * (numpy.tan(numpy.pi/M*i)**(-1)+1.j)
    delta[0] = 2*M/5
    # Задаём вектор значений функции гамма
    gamma = numpy.zeros(M, dtype=complex)
    for i in k:
        if i != 0:
            gamma[i] = (1 + 1.j*numpy.pi/M*i*(1+numpy.tan(numpy.pi/M*i)**(-2))-1.j*numpy.tan(numpy.pi/M*i)**(-1))*numpy.exp(delta[i])
    gamma[0] = 0.5*numpy.exp(delta[0])
    # Создаём сетки, чтобы избежать использования циклов
    delta_mesh, t_mesh = numpy.meshgrid(delta, t_z)
    gamma_mesh = numpy.meshgrid(gamma,t_z)[0]
    points = delta_mesh/t_mesh
    # Ищем значене f(s) нужных точках
    fun_res_ch = numpy.zeros(numpy.shape(points), dtype=complex)
    fun_res_zn = numpy.zeros(numpy.shape(points), dtype=complex)
    # Обходим числитель
    for i in range(len(f_s[0])):
        fun_res_ch = fun_res_ch + (f_s[0][i])*points**(len(f_s[0]) - i)
    # Обходим знаменатель
    for i in range(len(f_s[1])):
        fun_res_zn = fun_res_zn + (f_s[1][i])*points**(len(f_s[1]) - i)
    fun_res = fun_res_ch/fun_res_zn
    # Выделяем вещественную часть поэлементного произведения матриц
    sum_ar = numpy.real(gamma_mesh*fun_res)
    # Суммируем столбцы
    sum_ar = numpy.sum(sum_ar, axis = 1)
    # Получаем значение f(t) в заданных точках
    ilt = 0.4/t_z * sum_ar
    return ilt


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
        temp = str(i)
        temp1 = str(i)
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
    H1_den = numpy.zeros(len(H_den) + 1)
    for i in range(len(H_den)):
        H1_den[i] = H_den[i]
    HS = H_num, H_den
    H1S = H_num, H1_den
    print('H(S) =', sympy.sympify('('+HS_num+')/('+HS_den+')'))
    signal = SP.Pravilenko_11var()
    T = signal.tau/100
    t_graph = numpy.linspace(0.0001, 40, 200, dtype=float)
    h_graph = talbot_inverse(HS, t_graph)
    h1t_graph = talbot_inverse(H1S, t_graph)
    while abs(h_graph[len(h_graph) - 1] - h_graph[len(h_graph) - 2]) > 0.0001:
        temp = t_graph[len(t_graph) - 1] + T
        t_graph = numpy.append(t_graph, temp)
        h_graph = numpy.append(h_graph, talbot_inverse(HS, temp))
        h1t_graph = numpy.append(h1t_graph, talbot_inverse(H1S, temp))

    plt.figure(1)
    plt.xlabel('t')
    plt.ylabel('h1(t)')
    plt.title('h1(t)')
    plt.grid()
    plt.plot(t_graph, h1t_graph)

    plt.figure(2)
    plt.xlabel('t')
    plt.ylabel('h(t)')
    plt.title('h(t)')
    plt.grid()
    plt.plot(t_graph, h_graph)
    plt.show()
    return H_num, H_den, h_graph


# Функция, переводящая функции из области преобразований Лапласа во временную область
def S2t(HS):
    return inverse_laplace_transform(HS, s, t)


# Функция, вычисляющая АЧХ и ФЧХ
def FRandPR(HS_num, HS_den):
    w = numpy.linspace(0, 40, 400, dtype=complex)
    temp_num = numpy.zeros(numpy.shape(w), dtype=complex)
    temp_den = numpy.zeros(numpy.shape(w), dtype=complex)
    for i in range(len(HS_num)):
        temp_num = temp_num + (HS_num[i]) * (1.j * w) ** (len(HS_num) - i)
    for i in range(len(HS_den)):
        temp_den = temp_den + (HS_den[i]) * (1.j * w) ** (len(HS_den) - i)
    return numpy.abs(numpy.ndarray(shape=numpy.shape(temp_num), dtype=complex, buffer=temp_num/temp_den)), numpy.angle(numpy.ndarray(shape=numpy.shape(temp_num), dtype=complex, buffer=temp_num/temp_den))
__all__ = ['numpy']

