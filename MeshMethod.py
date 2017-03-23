# Модуль, реализующий обычный Метод Узловых Напряжений (максимум с 1 источником напряжения)

import Classes
import numpy


# Функция, реализующая МУН
def mesh_method(chain):
    # Выбираем базовый узел, так, чтобы он находился со стороны отрицательной полярности ИН
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].get_name() == "V":
            chain.Elements[i].To.set_voltage(0)
            chain.Elements[i].From.set_voltage(chain.Elements[i].Voltage)
            base_node = chain.Nodes.index(chain.Elements[i].To)
            break
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
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].Name == 'R':
            a[chain.Nodes.index(chain.Elements[i].To), chain.Nodes.index(chain.Elements[i].From)] += 1/chain.Elements[
                i].Resistance
            a[chain.Nodes.index(chain.Elements[i].From), chain.Nodes.index(chain.Elements[i].To)] += 1/chain.Elements[
                i].Resistance
    # Удаляем столбец с коэффициентами напряжения базового узла
    numpy.delete(a, base_node, axis=1)
    # Удаляем столбец с коэффициентами напряжения узла, равному напряжению ИН
    for i in range(0, chain.Nodes_count):
        if chain.Nodes[i].Voltage != 0 and chain.Nodes[i].Voltage is not None:
            numpy.delete(a, i, axis=1)
    # Заполняем столбец ответов систему уравнений
    b = numpy.zeros((chain.Nodes_count, 1))
    for i in range(0, chain.Nodes_count):
        if chain.Nodes[i].Voltage is None:
            for j in range(0, len(chain.Nodes[i].To)):
                if chain.Nodes[i].To[j].Name == 'I':
                    b[i] = b[i] + chain.Nodes[i].To[j].Amperage
            for j in range(0, len(chain.Nodes[i].From)):
                if chain.Nodes[i].From[j].Name == 'V':
                    b[i] = b[i] - chain.Nodes[i].From[j].Voltage
    # Удаляем стоку с токами
    numpy.delete(a, base_node, axis=0)
    # Удаляем строку с токами узла, равному по напряжению ИН
    for i in range(0, chain.Nodes_count):
        if chain.Nodes[i].Voltage != 0 and chain.Nodes[i].Voltage is not None:
            numpy.delete(a, i, axis=0)
    # Решаем систему уравнений
    v = numpy.linalg.solve(a, b)
    # Записываем узловые напряжения в соответствующие узлы
    for i in range(0, chain.Nodes_count):
        j = 1
        if chain.Nodes[i].Voltage is None:
            chain.Nodes[i].set_voltage(v[j])
            j += 1
    # Вычисляем напряжения элементов цепи
    for i in range(0, chain.Elements_count):
        chain.Elements[i].set_voltage(chain.Elements[i].From.Voltage - chain.Elements[i].To.Voltage)
    return chain

__all__ = ['Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.Chain,
           Classes.Node]

__all__ = ['numpy']