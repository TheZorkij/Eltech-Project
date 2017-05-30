# Модуль, реализующий Метод Наложения (используется вместе с МУН)

import Classes
import MeshMethod
import CopyChain

def overlay_method(chain):
    step_count = 0
    v_index = []

    #Находим количество шагов МН
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].get_name() == "V":
            v_index.append(i)
            step_count += 1
        i += 1

    #Матрицы результатов
    step_voltages = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]
    step_currents = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]

    #Метод наложения
    for step in range(0, step_count):
        delete_node = []
        delete_elem = []
        stepchain = CopyChain.copy_chain(chain)

        #Определяем узлы, между которыми короткое замыкание
        sc_from = stepchain.Elements[v_index[step]].From
        sc_to = stepchain.Elements[v_index[step]].To

        #Перестраиваем цепь, чтобы обесточенные элементы были подключены к одному узлу
        for j in range(0, stepchain.Elements_count):
            if stepchain.Elements[j].From == sc_from and stepchain.Elements[j].To == sc_to:
                stepchain.Elements[j].From = stepchain.Elements[j].To
                for k in range(0, stepchain.Nodes_count):
                    if stepchain.Nodes[k] == sc_to:
                        stepchain.Nodes[k].To.append(stepchain.Elements[j])
        for q in range(0, stepchain.Elements_count):
            if stepchain.Elements[q].To == sc_from:
                stepchain.Elements[q].To = sc_to
                for k in range(0, stepchain.Nodes_count):
                    if stepchain.Nodes[k] == sc_to:
                        stepchain.Nodes[k].From.append(stepchain.Elements[q])
        for j in range(0, stepchain.Nodes_count):
            if stepchain.Nodes[j] == sc_from:
                delete_node.append(j)
        for j in delete_node:
            del stepchain.Nodes[j]
            stepchain.Nodes_count -= 1

        #Удаляем лишние элементы из цепи
        temp = 0
        offset = 0
        while temp < stepchain.Elements_count:
            if stepchain.Elements[temp].From == stepchain.Elements[temp].To:
                delete_elem.append(temp + offset)
                trash = stepchain.Elements[temp]
                trashnode = stepchain.Elements[temp].From
                del stepchain.Elements[temp]
                stepchain.Elements_count -= 1
                #print(chain.Elements_count)
                temp = -1
                offset += 1
                for j in range(0, stepchain.Nodes_count):
                    if stepchain.Nodes[j] == trashnode:
                        loopcount = len(stepchain.Nodes[j].From)
                        q = 0
                        while q < loopcount:
                            if stepchain.Nodes[j].From[q] == trash:
                                del stepchain.Nodes[j].From[q]
                                loopcount -= 1
                            q += 1
                        q = 0
                        loopcount = len(stepchain.Nodes[j].To)
                        while q < loopcount:
                            if stepchain.Nodes[j].To[q] == trash:
                                del stepchain.Nodes[j].To[q]
                                loopcount -= 1
                            q += 1
            temp += 1

        #Вызываем МУН
        MeshMethod.mesh_method(stepchain)

        #Classes.Chain.output_chain(stepchain)
        #Заполняем матрицы результатов
        step_i = 0
        for i in range(0, chain.Elements_count):
            flag = 1
            for j in range(0, len(delete_elem)):
                if i == delete_elem[j]:
                    flag = 0
            if flag:
                step_currents[step][i] = stepchain.Elements[step_i].Amperage
                step_voltages[step][i] = stepchain.Elements[step_i].Voltage
                step_i += 1

        del stepchain
        del delete_elem
        del delete_node

    #print(step_currents)
    #print(step_voltages)

    #Находим сумму токов и напряжений на каждом шаге МН
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].Voltage == None:
            chain.Elements[i].Voltage = 0
        if chain.Elements[i].Amperage == None:
            chain.Elements[i].Amperage = 0

    for i in range(0, step_count):
        for j in range(0, chain.Elements_count):
            if chain.Elements[j].get_name() != 'V':
                chain.Elements[j].Voltage += step_voltages[i][j]
            chain.Elements[j].Amperage += step_currents[i][j]

    #Classes.Chain.output_chain(chain)
    #stepchain.output_chain()
    return chain