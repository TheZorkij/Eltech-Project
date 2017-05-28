# Модуль, реализующий Метод Наложения (используется вместе с МУН)

import Classes
import MeshMethod
import copy
import CopyChain

def overlay_method(chain):
    step_count = 0
    v_index = []
    delete_node = []
    delete_elem = []
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].get_name() == "V":
            v_index.append(i)
            step_count += 1
        i += 1

    step_voltages = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]
    step_currents = [[0 for x in range(0, chain.Elements_count)] for y in range(step_count)]

    #newchain = chain
    #for step in range(0, step_count):
    """stepchain = Classes.Chain(chain.Nodes_count, chain.Elements_count)
    stepchain.Nodes = chain.Nodes[:]
    stepchain.Elements = chain.Elements[:]
    for i in range(0, chain.Nodes_count):
        stepchain.Nodes[i].From = chain.Nodes[i].From[:]
        stepchain.Nodes[i].To = chain.Nodes[i].To[:]
    stepchain.Elements = chain.Elements[:]
    #stepchain.Elements_count = chain.Elements_count
    #stepchain.Nodes_count = chain.Nodes_count
    #print(stepchain.Elements[0].To)"""
    stepchain = CopyChain.copy_chain(chain)
    #print(chain.Nodes[1].To)
    #Classes.Chain.output_chain(stepchain)

    sc_from = stepchain.Elements[v_index[0]].From
    sc_to = stepchain.Elements[v_index[0]].To
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

    for i in range(sc_to.Key, stepchain.Nodes_count):
        stepchain.Nodes[i].Key -= 1

    temp = 0
    offset = 0
    while temp < stepchain.Elements_count:
        if stepchain.Elements[temp].From == stepchain.Elements[temp].To:
            delete_elem.append(temp + offset)
            trash = stepchain.Elements[temp]
            trashnode = stepchain.Elements[temp].From
            del stepchain.Elements[temp]
            stepchain.Elements_count -= 1
            print(chain.Elements_count)
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

    MeshMethod.mesh_method(stepchain)
    """for i in range(0, chain.Elements_count):
        flag = 1
        for j in range(0, len(delete_elem)):
            if i == delete_elem[j]:
                flag = 0
        if flag:
            print(1)
            step_currents[0][i] = stepchain.Elements[i].Amperage
            step_voltages[0][i] = stepchain.Elements[i].Voltage
    print(step_currents)
    print(step_voltages)"""

    #print(stepchain.Nodes[2].From)
    Classes.Chain.output_chain(stepchain)
    print()
    Classes.Chain.output_chain(chain)
    #stepchain.output_chain()