# Модуль, реализующий обычный Метод Узловых Напряжений (максимум с 1 источником напряжения)

import Classes
import numpy


# Функция, реализующая МУН
def mesh_method(chain):
    # Выбираем базовый узел, так, чтобы он находился со стороны отрицательной полярности ИН
    for i in chain.Elements:
        if i.get_name() == "V":
            i.To.set_voltage(i.Voltage)
            i.From.set_voltage(0)
            base_node = chain.Nodes.index(i.From)
            break
    # Если в цепи отсутствует ИН, то базовым узлом назначется первый узел в списке узлов
    else:
        base_node = 0
        chain.Nodes[0].set_voltage = 0
    a = numpy.zeros((chain.Nodes_count, chain.Nodes_count))
    # Заполняем матрицу коэффициентов
    # Заполняем собственные проводимости узлов
    for i in range(0, chain.Nodes_count):
            for j in range(0, len(chain.Nodes[i].To)):
                if hasattr(chain.Nodes[i].To[j], 'Resistance'):
                    a[i, i] += 1/chain.Nodes[i].To[j].Resistance
            for j in range(0, len(chain.Nodes[i].From)):
                if hasattr(chain.Nodes[i].From[j], 'Resistance'):
                    a[i, i] += 1/chain.Nodes[i].From[j].Resistance
    # Заполняем остальные поля матрицы коэффициентов
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].Name == 'R':
            a[chain.Nodes.index(chain.Elements[i].To), chain.Nodes.index(chain.Elements[i].From)] += 1 / chain.Elements[
                i].Resistance
            a[chain.Nodes.index(chain.Elements[i].From), chain.Nodes.index(chain.Elements[i].To)] += 1 / chain.Elements[
                i].Resistance
    # Удаляем столбец с коэффициентами напряжения базового узла
    a = numpy.delete(a, base_node, 1)
    a = numpy.delete(a, base_node, 0)
    # Удаляем столбец с коэффициентами напряжения узла, равному напряжению ИН (если такой есть)
    # Заполняем столбец ответов системы уравнений
    b = numpy.zeros((chain.Nodes_count, 1))
    for i in range(0, chain.Nodes_count):
        if chain.Nodes[i].Voltage is None:
            for j in range(0, len(chain.Nodes[i].To)):
                if chain.Nodes[i].To[j].Name == 'I':
                    b[i] = b[i] + chain.Nodes[i].To[j].Amperage
            for j in range(0, len(chain.Nodes[i].From)):
                if chain.Nodes[i].From[j].Name == 'I':
                    b[i] = b[i] - chain.Nodes[i].From[j].Amperage
    # Удаляем строку с током базового узла
    b = numpy.delete(b, base_node, 0)
    # Удаляем строку с токами узла, равного по напряжению ИН (если такой есть)
    for i in range(0, chain.Nodes_count):
        if chain.Nodes[i].Voltage != 0 and chain.Nodes[i].Voltage is not None:
            for j in range(0, len(b) - 1):
                b[j] += a[i - 1, j] * chain.Nodes[i].Voltage
            a = numpy.delete(a, i - 1, 0)
            a = numpy.delete(a, i - 1, 1)
            b = numpy.delete(b, i - 1, 0)
    # Решаем систему уравнений
    if b is not None:
        v = numpy.linalg.solve(a, b)
        flag = 0
    else:
        flag = 1
    # Записываем узловые напряжения в соответствующие узлы
    j = 0
    if flag != 1:
        for i in chain.Nodes:
            if i.Voltage is None:
                i.set_voltage(int(v[j]))
                j += 1
    # Вычисляем напряжения элементов цепи
    for i in chain.Elements:
        if i.Voltage is None:
            i.set_voltage(i.From.Voltage - i.To.Voltage)
    # Вычисляем силу тока во всех R-элементах цепи
    for i in chain.Elements:
        if hasattr(i, 'Resistance'):
            i.set_amperage(i.Voltage/i.Resistance)
    # Вычисляем силу тока в источнике
    a = 0
    for i in chain.Elements:
        if i.get_name() == 'V':
            for j in i.To.To:
                if hasattr(j, 'Amperage') and j.Amperage is not None:
                    a += j.Amperage
            for j in i.To.From:
                if hasattr(j, 'Amperage') and j.Amperage is not None:
                    a -= j.Amperage
            i.set_amperage(a)
            break
    else:
        print("В цепи нет источника О_О")

    return chain

__all__ = ['Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.Chain,
           Classes.Node]

__all__ = ['numpy']
