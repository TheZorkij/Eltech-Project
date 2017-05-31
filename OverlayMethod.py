# Модуль, реализующий Метод Наложения (используется вместе с МУН)

import Classes
import MeshMethod
import CopyChain

def overlay_method(chain):
    step_count = 0
    v_index = []
    cap = []
    ind = []

    for i in range(0, chain.Elements_count):
        if chain.Elements[i].get_name() == 'C':
            cap.append(chain.Elements[i].Capacity)
            t = chain.Elements[i].To.Key
            f = chain.Elements[i].From.Key
            chain.Elements[i] = Classes.V("V", 5, i)
            chain.Elements[i].set_to(chain.Nodes[t - 1])
            chain.Elements[i].set_from(chain.Nodes[f - 1])
        if chain.Elements[i].get_name() == 'L':
            ind.append(chain.Elements[i].Inductance)
            t = chain.Elements[i].To.Key
            f = chain.Elements[i].From.Key
            chain.Elements[i] = Classes.I("I", 5, i)
            chain.Elements[i].set_to(chain.Nodes[t - 1])
            chain.Elements[i].set_from(chain.Nodes[f - 1])

    #Находим количество шагов МН
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].get_name() == "V" or chain.Elements[i].get_name() == "I" or chain.Elements[i].get_name() == "C" or chain.Elements[i].get_name() == "L":
            if chain.Elements[i].get_name() == "V" or chain.Elements[i].get_name() == "I":
                source = chain.Elements[i].Num
            v_index.append(i)
            #sc_elem.append(chain.Elements[i])
            step_count += 1
        i += 1

    #Матрицы результатов
    step_voltages = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]
    step_currents = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]

    MatrixA = [[0 for x in range(0, step_count-1)] for y in range(step_count-1)]
    MatrixB = [[0 for x in range(0, 1)] for y in range(step_count-1)]
    MatrixC = [[0 for x in range(0, step_count-1)] for y in range(step_count-1)]
    MatrixD = [[0 for x in range(0, 1)] for y in range(step_count-1)]

    #Метод наложения
    for step in range(0, step_count):
        delete_node = []
        delete_elem = []
        sc_from = []
        sc_to = []
        sc_elem = []
        stepchain = CopyChain.copy_chain(chain)

        # Определяем узлы, между которыми короткое замыкание
        for sc_i in range(0, step_count):
            if sc_i != step:
                sc_elem.append(stepchain.Elements[v_index[sc_i]])
                sc_from.append(stepchain.Elements[v_index[sc_i]].From)
                sc_to.append(stepchain.Elements[v_index[sc_i]].To)

        # Перестраиваем цепь, чтобы обесточенные элементы были подключены к одному узлу
        for re_i in range(0, len(sc_to)):
            for j in range(0, stepchain.Elements_count):
                if stepchain.Elements[j].From == sc_from[re_i] and stepchain.Elements[j].To == sc_to[re_i]:
                    stepchain.Elements[j].From = stepchain.Elements[j].To
                    for k in range(0, stepchain.Nodes_count):
                        if stepchain.Nodes[k] == sc_to[re_i]:
                            stepchain.Nodes[k].To.append(stepchain.Elements[j])
            for q in range(0, stepchain.Elements_count):
                if stepchain.Elements[q].To == sc_from[re_i]:
                    stepchain.Elements[q].To = sc_to[re_i]
                    for k in range(0, stepchain.Nodes_count):
                        if stepchain.Nodes[k] == sc_to[re_i]:
                            stepchain.Nodes[k].From.append(stepchain.Elements[q])
            for j in range(0, stepchain.Nodes_count):
                if stepchain.Nodes[j] == sc_from[re_i]:
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

        for i in range(0, len(sc_elem)):
            step_currents[step][sc_elem[i].Num] = step_currents[step][sc_elem[i].Num-1]
            MatrixA[step-1][i] = step_currents[step][sc_elem[i].Num] / cap[i]
            MatrixB[step-1][i] = step_currents[step][source] / cap[i]
            MatrixC[step-1][i] = step_currents[step][sc_elem[i].Num] / cap[i]
            MatrixD[step-1][i] = step_currents[step][source] / cap[i]

        del stepchain
        del delete_elem
        del delete_node
        del sc_to
        del sc_from
        del sc_elem

    print(step_currents)
    print(step_voltages)

    print(MatrixA)
    print(MatrixB)
    print(MatrixC)
    print(MatrixD)

    #Находим сумму токов и напряжений на каждом шаге МН
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].Voltage == None:
            chain.Elements[i].Voltage = 0
        if chain.Elements[i].Amperage == None:
            chain.Elements[i].Amperage = 0

    for i in range(0, step_count):
        for j in range(0, chain.Elements_count):
            if chain.Elements[j].get_name() != 'V' and chain.Elements[j].get_name() != 'I':
                chain.Elements[j].Voltage += step_voltages[i][j]
            chain.Elements[j].Amperage += step_currents[i][j]

    #Classes.Chain.output_chain(chain)
    #stepchain.output_chain()
    return chain