# Модуль, реализующий Метод Наложения (используется вместе с МУН)

import Classes
import MeshMethod
import CopyChain

def overlay_method(chain):
    step_count = 0
    v_index = []
    reaction = 0  # 0 - реакция ток, 1 - реакция напряжение
    cap = []
    ind = []
    react_elem = []
    h_elem = None
    source_num = 0
    #Заменяем реактивные элементы на источники
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].get_name() == 'H':
            h_elem = chain.Elements[i].Num
        if chain.Elements[i].get_name() == 'C':
            cap.append(chain.Elements[i].Capacity)
            react_elem.append(chain.Elements[i])
            t = chain.Elements[i].To.Key
            f = chain.Elements[i].From.Key
            chain.Elements[i] = Classes.V("V", 5, i)
            chain.Elements[i].set_to(chain.Nodes[t - 1])
            chain.Elements[i].set_from(chain.Nodes[f - 1])
            for q in range(0, len(chain.Nodes[f - 1].To)):
                if chain.Nodes[f - 1].To[q].get_name() == 'C':
                    del chain.Nodes[f - 1].To[q]
                    chain.Nodes[f - 1].To.append(chain.Elements[i])
            for q in range(0, len(chain.Nodes[t - 1].From)):
                if chain.Nodes[t - 1].From[q].get_name() == 'C':
                    del chain.Nodes[t - 1].From[q]
                    chain.Nodes[t - 1].From.append(chain.Elements[i])
            # v_index.append(chain.Elements[i].Num)
            # step_count += 1
        if chain.Elements[i].get_name() == 'L':
            ind.append(chain.Elements[i].Inductance)
            react_elem.append(chain.Elements[i])
            t = chain.Elements[i].To.Key
            f = chain.Elements[i].From.Key
            chain.Elements[i] = Classes.I("I", 0.005, i)
            chain.Elements[i].set_to(chain.Nodes[t - 1])
            chain.Elements[i].set_from(chain.Nodes[f - 1])
            for q in range(0, len(chain.Nodes[f - 1].To)):
                if chain.Nodes[f - 1].To[q].get_name() == 'L':
                    del chain.Nodes[f - 1].To[q]
                    chain.Nodes[f - 1].To.append(chain.Elements[i])
            for q in range(0, len(chain.Nodes[t - 1].From)):
                if chain.Nodes[t - 1].From[q].get_name() == 'L':
                    del chain.Nodes[t - 1].From[q]
                    chain.Nodes[t - 1].From.append(chain.Elements[i])
            # i_index.append(chain.Elements[i].Num)
            # step_count += 1

    #Находим количество шагов МН и заменяем все ИТ на ИН
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].get_name() == "V":
            #source = chain.Elements[i].Num
            if i == 0:
                reaction = 0
            v_index.append(chain.Elements[i].Num)
            step_count += 1
        if chain.Elements[i].get_name() == "I":
            if i == 0:
                reaction = 1
            t = chain.Elements[i].To.Key
            f = chain.Elements[i].From.Key
            amp = chain.Elements[i].Amperage
            chain.Elements[i] = Classes.V("V", None, i)
            for j in range(0, chain.Elements_count):
                if j != i:
                    if (chain.Elements[j].From.Key == t and chain.Elements[j].To.Key == f) or (
                            chain.Elements[j].From.Key == f and chain.Elements[j].To.Key == t):
                        if (chain.Elements[j].From.Key == f and chain.Elements[j].To.Key == t):
                            chain.Elements[j].set_from(chain.Nodes[t - 1])
                            chain.Elements[j].set_to(chain.Nodes[f - 1])
                            q = 0
                            while q < len(chain.Nodes[t - 1].From):
                                if chain.Nodes[t - 1].From[q].Num == chain.Elements[j].Num:
                                    del chain.Nodes[t - 1].From[q]
                                q += 1
                            q = 0
                            while q < len(chain.Nodes[f - 1].To):
                                if chain.Nodes[f - 1].To[q].Num == chain.Elements[j].Num:
                                    del chain.Nodes[f - 1].To[q]
                                q += 1
                            chain.Nodes[t - 1].set_to(chain.Elements[j])
                            chain.Nodes[f - 1].set_from(chain.Elements[j])
                        chain.Nodes.append(Classes.Node(chain.Nodes_count + 1))
                        chain.Elements[i].Voltage = amp * chain.Elements[j].Resistance
                        num = chain.Nodes_count
                        chain.Nodes_count += 1
                        chain.Nodes[num].To = []
                        chain.Nodes[num].From = []
                        chain.Elements[j].set_from(chain.Nodes[num])
                        chain.Nodes[num].set_to(chain.Elements[j])
                        # if chain.Elements[j].To.Key == f:
                        chain.Elements[i].set_from(chain.Nodes[t - 1])
                        chain.Elements[i].set_to(chain.Nodes[num])
                        chain.Nodes[num].set_from(chain.Elements[i])
                        q = 0
                        while q < len(chain.Nodes[f - 1].To):
                            # for q in range(0, len(chain.Nodes[f - 1].To)):
                            if chain.Nodes[f - 1].To[q].Num == chain.Elements[i].Num:
                                del chain.Nodes[f - 1].To[q]
                            q += 1
                        q = 0
                        while q < len(chain.Nodes[t - 1].From):
                            # for q in range(0, len(chain.Nodes[t - 1].From)):
                            if chain.Nodes[t - 1].From[q].Num == chain.Elements[i].Num:
                                del chain.Nodes[t - 1].From[q]
                                chain.Nodes[t - 1].To.append(chain.Elements[i])
                            q += 1
                        q = 0
                        while q < len(chain.Nodes[t - 1].To):
                            # for q in range(0, len(chain.Nodes[t - 1].To)):
                            if chain.Nodes[t - 1].To[q].Num == chain.Elements[j].Num:
                                del chain.Nodes[t - 1].To[q]
                            q += 1
                        break
            # разворачивает R
            if not chain.Nodes[t - 1].From:
                j = 0
                while j < len(chain.Nodes[t - 1].To):
                    # for j in range(0, len(chain.Nodes[t-1].To)):
                    if j != i:
                        k = chain.Nodes[t - 1].To[j].Num
                        # k_f = chain.Elements[k].From
                        k_t = chain.Elements[k].To.Key
                        chain.Nodes[t - 1].set_from(chain.Elements[k])
                        chain.Elements[k].set_to(chain.Nodes[t - 1])
                        chain.Elements[k].set_from(chain.Nodes[k_t - 1])
                        del chain.Nodes[t - 1].To[j]
                        break
                    j += 1
                    # source = chain.Elements[i].Num
            v_index.append(chain.Elements[i].Num)
            step_count += 1

    #Матрицы результатов
    step_voltages = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]
    step_currents = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]

    MatrixA = [[0 for x in range(0, step_count-1)] for y in range(step_count-1)]
    MatrixB = [[0 for x in range(0, 1)] for y in range(step_count-1)]
    MatrixC = [0 for x in range(0, step_count-1)]
    MatrixD = None

    #Метод наложения
    for step in range(0, step_count):
        delete_node = []
        delete_elem = []
        sc_from = []
        sc_to = []
        sc_elem = []
        sc_value = []
        stepchain = CopyChain.copy_chain(chain)
        #Classes.Chain.output_chain(stepchain)
        # Определяем узлы, между которыми короткое замыкание
        for sc_i in range(0, len(v_index)):
            if sc_i != step:
                sc_elem.append(stepchain.Elements[v_index[sc_i]])
                sc_from.append(stepchain.Elements[v_index[sc_i]].From)
                sc_to.append(stepchain.Elements[v_index[sc_i]].To)

        # Перестраиваем цепь, чтобы обесточенные элементы были подключены к одному узлу
        for re_i in range(0, len(sc_to)):
            del_i = 0
            for j in range(0, stepchain.Elements_count):
                if stepchain.Elements[j].From == sc_from[re_i] and stepchain.Elements[j].To == sc_to[re_i]:
                    stepchain.Elements[j].From = stepchain.Elements[j].To
                    for k in range(0, stepchain.Nodes_count):
                        if stepchain.Nodes[k] == sc_to[re_i]:
                            stepchain.Nodes[k].To.append(stepchain.Elements[j])
            for q in range(0, stepchain.Elements_count):
                if stepchain.Elements[q].To == sc_from[re_i] and stepchain.Elements[q].From != sc_to[re_i] and stepchain.Elements[q].From != sc_from[re_i] and stepchain.Elements[q].get_name() == 'R'\
                        or stepchain.Elements[q].From == sc_to[re_i] and stepchain.Elements[q].To != sc_to[re_i] and stepchain.Elements[q].To != sc_from[re_i] and stepchain.Elements[q].get_name() == 'R':
                    sc_value.append(stepchain.Elements[q].Num)
                    break
            for q in range(0, stepchain.Elements_count):
                if stepchain.Elements[q].To == sc_from[re_i]:
                    stepchain.Elements[q].To = sc_to[re_i]
                    for k in range(0, stepchain.Nodes_count):
                        if stepchain.Nodes[k] == sc_to[re_i]:
                            stepchain.Nodes[k].From.append(stepchain.Elements[q])
            for j in range(0, stepchain.Nodes_count):
                if stepchain.Nodes[j] == sc_from[re_i]:
                    delete_node.append(j)
            for j in range(0, stepchain.Elements_count):
                if stepchain.Elements[j].From == stepchain.Nodes[delete_node[del_i]]:
                    for k in range(0, stepchain.Nodes_count):
                        if stepchain.Nodes[k] == sc_to[re_i]:
                            stepchain.Elements[j].set_from(stepchain.Nodes[k])
                            stepchain.Nodes[k].From.append(stepchain.Elements[j])
            for j in delete_node:
                del stepchain.Nodes[j]
                stepchain.Nodes_count -= 1
            del_i += 1
        #Classes.Chain.output_chain(stepchain)

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
        #Classes.Chain.output_chain(stepchain)
        #Вызываем МУН
        MeshMethod.mesh_method(stepchain)
        Classes.Chain.output_chain(stepchain)

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
        if sc_value:
            for i in range(0, len(sc_elem)):
                step_currents[step][sc_elem[i].Num] = step_currents[step][sc_value[i]]

        del stepchain
        del delete_elem
        del delete_node
        del sc_to
        del sc_from
        del sc_elem
        del sc_value

    print(step_currents)
    print(step_voltages)

    #Заполняем матрицу А
    for i in range(1, step_count):
        for j in range(0, step_count - 1):
            if reaction == 0:
                if react_elem[i-1].get_name() == 'C':
                    MatrixA[i-1][j] = (step_currents[i][react_elem[j].Num] / cap[j])
                    if step_voltages[i][react_elem[j].Num] != 0:
                        MatrixA[i-1][j] = MatrixA[i-1][j]/step_voltages[i][react_elem[j].Num]
                else:
                    MatrixA[i - 1][j] = (step_currents[i][react_elem[j].Num] / ind[j])
                    if step_voltages[i][react_elem[j].Num] != 0:
                        MatrixA[i-1][j] = MatrixA[i-1][j]/step_voltages[i][react_elem[j].Num]
            else:
                if react_elem[i-1].get_name() == 'C':
                    MatrixA[i-1][j] = (step_voltages[i][react_elem[j].Num] / cap[j])
                    if step_currents[i][react_elem[j].Num] != 0:
                        MatrixA[i - 1][j] = MatrixA[i - 1][j] / step_currents[i][react_elem[j].Num]
                else:
                    MatrixA[i-1][j] = (step_voltages[i][react_elem[j].Num] / ind[j])
                    if step_currents[i][react_elem[j].Num] != 0:
                        MatrixA[i - 1][j] = MatrixA[i - 1][j] / step_currents[i][react_elem[j].Num]

    # Заполняем матрицу B
    for i in range(0, step_count-1):
        if reaction == 0:
            if react_elem[i].get_name() == 'C':
                MatrixB[i][0] = (step_currents[i][0] / cap[i])
                if step_voltages[i][0] != 0:
                    MatrixB[i][0] = MatrixB[i][0] / step_voltages[i][0]
            else:
                MatrixB[i][0] = (step_currents[i][0] / ind[i])
                if step_voltages[i][0] != 0:
                    MatrixB[i][0] = MatrixB[i][0] / step_voltages[i][0]
        else:
            if react_elem[i].get_name() == 'C':
                MatrixB[i][0] = (step_voltages[i][0] / cap[i])
                if step_currents[i][0] != 0:
                    MatrixB[i][0] = MatrixB[i][0] / step_currents[i][0]
            else:
                MatrixB[i][0] = (step_voltages[i][0] / ind[i])
                if step_currents[i][0] != 0:
                    MatrixB[i][0] = MatrixB[i][0] / step_currents[i][0]

    #Заполняем матрицу С
    if h_elem is not None:
        for i in range(1, step_count):
            if reaction == 0:
                if react_elem[i - 1].get_name() == 'C':
                    MatrixC[i - 1] = (step_currents[i][h_elem] / cap[i-1])
                    if step_voltages[i][h_elem] != 0:
                        MatrixC[i - 1] = MatrixC[i - 1] / step_voltages[i][h_elem]
                else:
                    MatrixC[i - 1] = (step_currents[i][h_elem] / ind[j])
                    if step_voltages[i][h_elem] != 0:
                        MatrixC[i - 1] = MatrixC[i - 1] / step_voltages[i][h_elem]
            else:
                if react_elem[i - 1].get_name() == 'C':
                    MatrixC[i - 1] = (step_voltages[i][h_elem] / cap[j])
                    if step_currents[i][h_elem] != 0:
                        MatrixC[i - 1] = MatrixC[i - 1] / step_currents[i][h_elem]
                else:
                    MatrixC[i - 1] = (step_voltages[i][h_elem] / ind[j])
                    if step_currents[i][h_elem] != 0:
                        MatrixC[i - 1] = MatrixC[i - 1] / step_currents[i][h_elem]

    #Заполняем матрицу D
    if h_elem is not None:
        if reaction == 0:
            MatrixD = step_currents[0][h_elem]
            if step_voltages[0][h_elem] != 0:
                MatrixD = MatrixD / step_voltages[0][h_elem]
        else:
            MatrixD = step_voltages[0][h_elem]
            if step_currents[0][h_elem] != 0:
                MatrixD = MatrixD / step_currents[0][h_elem]

    print("Матрица А: ", end=' ')
    print(MatrixA)
    print("Матрица B: ", end=' ')
    print(MatrixB)
    print("Матрица C: ", end=' ')
    print(MatrixC)
    print("Матрица D: ", end=' ')
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