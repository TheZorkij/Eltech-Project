# Модуль, выполняющий обработку входного сигнала и построение амплитудного и фазового спектров
from sympy import cos, Heaviside, symbols
from sympy.abc import t
import numpy
import matplotlib.pyplot as plt
import copy
import math


# Класс для хранения параметров сигнала
class Signal:
    expr = None
    tau = None
    A = None
    T = None


# Функция, задающая сигнал десятого варианта курсовой работы (вариант Петрова И.)
def Petrov_10var():
    signal = Signal
    signal.A = 10
    signal.tau = 2
    signal.T = 4
    signal.expr = signal.A*Heaviside(t) - 2*signal.A*Heaviside(t - signal.tau/2) + signal.A*Heaviside(t - signal.tau)
    return signal


# Функция, задающая сигнал одиннадцатого варианта курсовой работы (вариант Правиленко М.)
def Pravilenko_11var():
    signal = Signal
    signal.A = 10
    signal.tau = 20
    signal.T = 40
    signal.expr = 2 * signal.A/signal.tau * (t - t * Heaviside(t - signal.tau/2)) + (-2 * signal.A/signal.tau * t + 2 * signal.A)*(Heaviside(t - signal.tau/2)-Heaviside(t - signal.tau))
    return signal


# Функция, задающая сигнал шестого варианта курсовой работы (вариант Клюкина А.)
def Klykin_6var():
    signal = Signal
    signal.A = 2
    signal.tau = 3
    signal.T = 6
    signal.expr = signal.A * (cos(t * numpy.pi/signal.tau) - cos(t * numpy.pi/signal.tau) * Heaviside(t - signal.tau))
    return signal


# Функция, вычисляющая значения входного сигнала
def InputSignalGraphic(signal):
    y = []
    f2 = copy.deepcopy(signal.expr)
    x = numpy.linspace(0.0001, signal.T, 200)
    for i in x:
        if int(i) == i:
            f2 = f2.subs(Heaviside(t - int(i)), 1)
        else:
            f2 = f2.subs(Heaviside(t - i), 1)
        y.append(f2.subs(t, i))
    return x, y


def ConvolveIntegral(x, y1, y2):
    delta = x[1] - x[0]
    y_ret = numpy.zeros(numpy.shape(x))
    for i in range(len(x) - 1):
        temp_y1 = y1[0:i + 1]
        temp_y2 = y2[0:i + 1]
        temp_y2 = numpy.flipud(temp_y2)
        y_int = temp_y1 * temp_y2
        y_ret[i] = numpy.trapz(y_int, dx=delta)
    return y_ret

# Функция, вычисляющая и строящая спектры амплитудного и фазового спектра для непереодического сигнала
def AmpPhaseSingle(signal, FR, PR):
    # Вычисление спектров по образу сигнала
    w = numpy.linspace(0, 40, 400, dtype=complex)
    w += 0.0001
    temp = numpy.zeros(numpy.shape(w), dtype=complex)
    # Вариант 10 (Петров И.)
    # temp = signal.A * (1 - 2 * numpy.exp(-w * 1.j * signal.tau/2) + numpy.exp(-w * 1.j * signal.tau))/(w * 1.j)
    # Вариант 11 (Правиленко М.)
    temp = signal.A * numpy.exp(-signal.tau * w * 1.j)*(numpy.exp(signal.tau/2 * w *1.j) - 1) ** 2/(signal.tau/2 * (w*1.j)**2)
    # Вариант 6 (Клюкин А.)
    # temp = signal.A * (signal.tau ** 2) * (numpy.exp(-signal.tau * w *1.j) + 1) * w *1.j/((signal.tau * w *1.j) ** 2 + numpy.pi ** 2)
    Amp1 = numpy.abs(temp)
    Phase1 = numpy.angle(temp)
    Amp2 = Amp1 * FR
    Phase2 = Phase1 + PR
    # Вычисление полосы пропускания цепи
    for i in range(0, len(FR)):
        if math.isnan(FR[i]):
            FR[i] = FR[i+1]
    Hwmax = 0.707 * numpy.max(FR)
    beg = None
    end = None
    for i in range(0, len(FR)):
        if FR[i] >= Hwmax:
            if beg is None:
                beg = i
                end = i
            else:
                end += 1
    delta_w = [float(w[beg]), float(w[end])]
    print('Полоса пропускания цепи =', delta_w)
    # Вычисление дельта омега 1
    Imax = 0.1 * numpy.max(Amp1)
    maxi = 0
    for i in range(len(Amp1)):
        if (Amp1[i] >= Imax):
            maxi = i
    delta_w1 = float(w[maxi])
    print('delta w1 =', delta_w1)
    # Амплитуда входного сигнала
    plt.figure(1)
    plt.xlabel('Omega')
    plt.ylabel('|A|')
    plt.title('Ampletude spectre IN')
    plt.grid()
    plt.plot(w, Amp1)
    # Фаза входного сигнала
    plt.figure(2)
    plt.xlabel('Omega')
    plt.ylabel('arg(A)')
    plt.title('Phase spectre IN')
    plt.grid()
    plt.plot(w, Phase1)
    # Амплитуда выходного сигнала
    plt.figure(3)
    plt.xlabel('Omega')
    plt.ylabel('|A|')
    plt.title('Ampletude spectre OUT')
    plt.grid()
    plt.plot(w, Amp2)
    # Фаза выходного сигнала
    plt.figure(4)
    plt.xlabel('Omega')
    plt.ylabel('arg(A)')
    plt.title('Phase spectre OUT')
    plt.grid()
    plt.plot(w, Phase2)
    # АЧХ
    plt.figure(5)
    plt.xlabel('Omega')
    plt.ylabel('|H(jw)|')
    plt.title('АЧХ')
    plt.grid()
    plt.plot(w, FR)
    # ФЧХ
    plt.figure(6)
    plt.xlabel('Omega')
    plt.ylabel('arg(H(jw))')
    plt.title('ФЧХ')
    plt.grid()
    plt.plot(w, PR)
    plt.show()


# Функция, вычисляющая спектры периодического сигнала
def AmpPhaseFourier(signal, HS_num, HS_den, k=10):
    # Вычисление спектров по образу сигнала
    w1 = 2*numpy.pi/signal.T
    w = numpy.zeros(0, dtype=complex)
    for i in range(0, k):
        w = numpy.append(w, [w1 * i + 0.00001])
    # Вариант 10 (Петров И.)
    # temp = 2 * signal.A * (1 - 2 * numpy.exp(-w * 1.j * signal.tau / 2) + numpy.exp(-w * 1.j * signal.tau)) / (w * 1.j * signal.T)
    # Вариант 11 (Правиленко М.)
    temp = 2 * signal.A * numpy.exp(-signal.tau * w * 1.j)*(numpy.exp(signal.tau/2 * w *1.j) - 1) ** 2/(signal.T * signal.tau/2 * (w*1.j)**2)
    # Вариант 6 (Клюкин А.)
    # temp = 2 * signal.A * (signal.tau ** 2) * (numpy.exp(-signal.tau * w *1.j) + 1) * w *1.j/(((signal.tau * w *1.j) ** 2 + numpy.pi ** 2) * signal.T)
    temp_num = numpy.zeros(numpy.shape(w), dtype=complex)
    temp_den = numpy.zeros(numpy.shape(w), dtype=complex)
    for i in range(0, len(HS_num)):
        temp_num = temp_num + (HS_num[i]) * (1.j * w) ** (len(HS_num) - i)
    for i in range(0, len(HS_num)):
        temp_den = temp_den + (HS_den[i]) * (1.j * w) ** (len(HS_den) - i)
    FR = numpy.abs(numpy.ndarray(shape=numpy.shape(temp_num), dtype=complex, buffer=temp_num/temp_den))
    PR = numpy.angle(numpy.ndarray(shape=numpy.shape(temp_num), dtype=complex, buffer=temp_num/temp_den))
    Amp1 = numpy.abs(temp)
    Phase1 = numpy.angle(temp)
    Amp2 = Amp1 * FR
    Phase2 = Phase1 + PR
    # Входной и выходной сигнал периодического воздействия
    x = numpy.linspace(0, signal.T, 200)
    f1 = numpy.zeros(numpy.shape(x))
    f2 = numpy.zeros(numpy.shape(x))
    f1 = f1 + Amp1[0] / 2
    f2 = f2 + Amp2[0] / 2
    # Расчитываем f1(t) и f2(t) через частоты и амплитуды
    for i in range(0, k-1):
        f1 = f1 + Amp1[i + 1] * numpy.cos(w[i + 1] * x + Phase1[i + 1])
        f2 = f2 + Amp2[i + 1] * numpy.cos(w[i + 1] * x + Phase2[i + 1])
    # Амплитуда входного сигнала
    plt.figure(7)
    plt.xlabel('Omega')
    plt.ylabel('|A|')
    plt.title('Ampletude spectre IN Fourier')
    plt.grid()
    plt.stem(w, Amp1)
    # Фаза входного сигнала
    plt.figure(8)
    plt.xlabel('Omega')
    plt.ylabel('arg(A)')
    plt.title('Phase spectre IN Fourier')
    plt.grid()
    plt.stem(w, Phase1)
    # Амплитуда выходного сигнала
    plt.figure(9)
    plt.xlabel('Omega')
    plt.ylabel('|A|')
    plt.title('Ampletude spectre OUT Fourier')
    plt.grid()
    plt.stem(w, Amp2)
    # Фаза выходного сигнала
    plt.figure(10)
    plt.xlabel('Omega')
    plt.ylabel('arg(A)')
    plt.title('Phase spectre OUT Fourier')
    plt.grid()
    plt.stem(w, Phase2)
    # Входной сигнал
    plt.figure(11)
    plt.xlabel('t')
    plt.ylabel('f1(t)')
    plt.title('Input signal')
    plt.grid()
    plt.plot(x, f1)
    # Выходной сигнал
    plt.figure(12)
    plt.xlabel('t')
    plt.ylabel('f2(t)')
    plt.title('Output signal')
    plt.grid()
    plt.plot(x, f2)
    plt.show()