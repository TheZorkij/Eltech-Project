# Модуль, реализующий обычный Метод Узловых Напряжений (максимум с 1 источником напряжения)

import Classes
import numpy


# Функция, реализующая МУН
def mesh_method(chain):
    # Выбираем базовый узел, так, чтобы он находился со стороны отрицательной полярности ИН
    for i in chain.Elements:
        if i.get_name() == "V":
            i.To.set_voltage(0)
            i.From.set_voltage(i.Voltage)
            base_node = chain.Nodes.index(i.To)
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
                if chain.Nodes[i].To[j] == 'R':
                    a[i, i] += 1/chain.Nodes.To[i].R
            for j in range(0, len(chain.Nodes[i].From)):
                if chain.Nodes[i].From[j] == 'R':
                    a[i, i] += 1/chain.Nodes.From[i].R
    # Заполняем остальные поля матрицы коэффициентов
    for i in chain.Elements:
        if i.Name == 'R':
            a[chain.Nodes.index(i.To), chain.Nodes.index(i.From)] += 1/i.Resistance
            a[chain.Nodes.index(i.From), chain.Nodes.index(i.To)] += 1/i.Resistance
    # Удаляем столбец с коэффициентами напряжения базового узла
    numpy.delete(a, base_node, axis=1)
    # Удаляем столбец с коэффициентами напряжения узла, равному напряжению ИН (если такой есть)
    for i in chain.Nodes:
        if i.Voltage != 0 and i.Voltage is not None:
            numpy.delete(a, i, axis=1)
    # Заполняем столбец ответов системы уравнений
    b = numpy.zeros((chain.Nodes_count, 1))
    for i in range(0, chain.Nodes_count):
        if chain.Nodes[i].Voltage is None:
            for j in range(0, len(chain.Nodes[i].To)):
                if chain.Nodes[i].To[j].Name == 'I':
                    b[i] += chain.Nodes[i].To[j].Amperage
            for j in range(0, len(chain.Nodes[i].From)):
                if chain.Nodes[i].From[j].Name == 'V':
                    b[i] -= chain.Nodes[i].From[j].Amperage
    # Удаляем строку с током базового узла
    numpy.delete(a, base_node, axis=0)
    # Удаляем строку с токами узла, равного по напряжению ИН (если такой есть)
    for i in chain.Nodes:
        if i.Voltage != 0 and i.Voltage is not None:
            numpy.delete(a, i, axis=0)
    # Решаем систему уравнений
    v = numpy.linalg.solve(a, b)
    # Записываем узловые напряжения в соответствующие узлы
    for i in chain.Nodes:
        j = 1
        if i.Voltage is None:
            i.set_voltage(v[j])
            j += 1
    # Вычисляем напряжения элементов цепи
    for i in chain.Elements:
        i.set_voltage(i.From.Voltage - i.To.Voltage)
    # Вычисляем силу тока во всех R-элементах цепи
    for i in chain.Elements:
        if hasattr(i, 'Resistance'):
            i.set_amperage(i.Voltage/i.Resistance)
    # Вычисляем силу тока в
    a = 0
    for i in chain.Elements:
        if i.get_name() == 'V' or i.get_name() == 'I':
            for j in i.To.To:
                a += j.amperage
            for j in i.To.From:
                a -= j.amperage
            break
    else:
        print("В цепи нет источника О_О")
    return chain

__all__ = ['Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.Chain,
           Classes.Node]

__all__ = ['numpy']