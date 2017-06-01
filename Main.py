# Курсовая работа по Теоретическим Основам Электротехники
# Весенний семестр 2017 года
# Авторы: Петров И., Правиленко М., Клюкин А.

# Главный модуль программы
import Classes
import CreateChain
import OverlayMethod
import CopyChain
import LaplaceTransformDomain as LTD
import sympy
import SignalProcessing as SP
import copy

#chaine = CreateChain.default_chain()
#chain = CopyChain.copy_chain(chaine)
chain = CreateChain.Petrov_10var()

#Заменяем реактивные элементы на источники
"""for i in range(0, chain.Elements_count):
    if chain.Elements[i].get_name() == 'C':
        #cap.append(chain.Elements[i].Capacity)
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
        #ind.append(chain.Elements[i].Inductance)
        t = chain.Elements[i].To.Key
        f = chain.Elements[i].From.Key
        chain.Elements[i] = Classes.I("I", 5, i)
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

for i in range(0, chain.Elements_count):
    if chain.Elements[i].get_name() == "V":
        source = chain.Elements[i].Num
        #v_index.append(chain.Elements[i].Num)
        #step_count += 1
    if chain.Elements[i].get_name() == "I":
        t = chain.Elements[i].To.Key
        f = chain.Elements[i].From.Key
        amp = chain.Elements[i].Amperage
        chain.Elements[i] = Classes.V("V", None, i)
        flag = 1
        for j in range(0, chain.Elements_count):
            if j != i:
                if (chain.Elements[j].From.Key == t and chain.Elements[j].To.Key == f) or (chain.Elements[j].From.Key == f and chain.Elements[j].To.Key == t):
                    if (chain.Elements[j].From.Key == f and chain.Elements[j].To.Key == t):
                        chain.Elements[j].set_from(chain.Nodes[t-1])
                        chain.Elements[j].set_to(chain.Nodes[f-1])
                        q = 0
                        while q < len(chain.Nodes[t-1].From):
                            if chain.Nodes[t-1].From[q].Num == chain.Elements[j].Num:
                                del chain.Nodes[t-1].From[q]
                            q += 1
                        q = 0
                        while q < len(chain.Nodes[f-1].To):
                            if chain.Nodes[f-1].To[q].Num == chain.Elements[j].Num:
                                del chain.Nodes[f-1].To[q]
                            q += 1
                        chain.Nodes[t-1].set_to(chain.Elements[j])
                        chain.Nodes[f-1].set_from(chain.Elements[j])
                    chain.Nodes.append(Classes.Node(chain.Nodes_count + 1))
                    chain.Elements[i].Voltage = amp * chain.Elements[j].Resistance
                    num = chain.Nodes_count
                    chain.Nodes_count += 1
                    chain.Nodes[num].To = []
                    chain.Nodes[num].From = []
                    chain.Elements[j].set_from(chain.Nodes[num])
                    chain.Nodes[num].set_to(chain.Elements[j])
                    #if chain.Elements[j].To.Key == f:
                    chain.Elements[i].set_from(chain.Nodes[t-1])
                    chain.Elements[i].set_to(chain.Nodes[num])
                    chain.Nodes[num].set_from(chain.Elements[i])
                    q = 0
                    while q < len(chain.Nodes[f - 1].To):
                    #for q in range(0, len(chain.Nodes[f - 1].To)):
                        if chain.Nodes[f - 1].To[q].Num == chain.Elements[i].Num:
                            del chain.Nodes[f - 1].To[q]
                        q += 1
                    q = 0
                    while q < len(chain.Nodes[t - 1].From):
                    #for q in range(0, len(chain.Nodes[t - 1].From)):
                        if chain.Nodes[t - 1].From[q].Num == chain.Elements[i].Num:
                            del chain.Nodes[t - 1].From[q]
                            chain.Nodes[t - 1].To.append(chain.Elements[i])
                        q += 1
                    q = 0
                    while q < len(chain.Nodes[t-1].To):
                        #for q in range(0, len(chain.Nodes[t - 1].To)):
                        if chain.Nodes[t - 1].To[q].Num == chain.Elements[j].Num:
                            del chain.Nodes[t - 1].To[q]
                        q += 1
                    flag = 0
                    break
        #разворачивает
        if not chain.Nodes[t-1].From:
            j = 0
            while j < len(chain.Nodes[t-1].To):
            #for j in range(0, len(chain.Nodes[t-1].To)):
                if j != i:
                    k = chain.Nodes[t-1].To[j].Num
                    #k_f = chain.Elements[k].From
                    k_t = chain.Elements[k].To.Key
                    chain.Nodes[t-1].set_from(chain.Elements[k])
                    chain.Elements[k].set_to(chain.Nodes[t-1])
                    chain.Elements[k].set_from(chain.Nodes[k_t-1])
                    del chain.Nodes[t - 1].To[j]
                    break
                j += 1
        #source = chain.Elements[i].Num
        #i_index.append(chain.Elements[i].Num)
        #step_count += 1"""

chain, A, B, C, D = OverlayMethod.overlay_method(chain)
# Classes.Chain.output_chain(chain)
HS_num, HS_den, H1S_den, H_num, H_den = LTD.HS_calc(A, B, C, D)
print('H(S) =', sympy.sympify('('+HS_num+')/('+HS_den+')'))
ht = LTD.S2t(sympy.sympify('('+HS_num+')/('+HS_den+')'))
print('h(t) =', ht)
h1t = LTD.S2t(sympy.sympify('('+HS_num+')/('+H1S_den+')'))
print('h1(t) =', h1t)
FR, PR = LTD.FRandPR(H_num, H_den)
signal = SP.Petrov_10var()
SP.AmpPhaseSingle(signal, FR, PR)
SP.AmpPhaseFourier(signal, H_num, H_den)
__all__ = ['Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.SC, Classes.Chain,
           Classes.Node]

__all__ = ['CreateChain', 'MeshMethod', 'OverlayMethod', 'CopyChain']
