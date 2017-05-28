import Classes
import copy

def copy_chain(chain):
    n = chain.Nodes_count
    e = chain.Elements_count
    newchain = Classes.Chain(n, e)
    #print(id(newchain))
    #print(id(chain))
    #newchain.Nodes_count = chain.Nodes_count
    #print(id(newchain.Nodes_count))
    #print(id(chain.Nodes_count))
    i = 0
    while i < newchain.Nodes_count:
        newchain.Nodes.append(Classes.Node(i + 1))
        newchain.Nodes[i].To = []
        newchain.Nodes[i].From = []
        i += 1

    #newchain.Elements_count = copy.deepcopy(chain.Elements_count)
    for i in range(0, chain.Elements_count):
        if chain.Elements[i].Name == 'R':
            newchain.Elements.append(Classes.R('R', chain.Elements[i].Resistance, i))
        if chain.Elements[i].Name == 'V':
            newchain.Elements.append(Classes.V('V', copy.deepcopy(chain.Elements[i].Voltage), i))
        if chain.Elements[i].Name == 'I':
            newchain.Elements.append(Classes.I('I', copy.deepcopy(chain.Elements[i].Amperage)))
        #print(id(newchain.Elements[i]))
        #print(id(chain.Elements[i]))

    for i in range(0, chain.Nodes_count):
        for j in range(0, len(chain.Nodes[i].From)):
            f = chain.Nodes[i].From[j].Num
            newchain.Nodes[i].set_from(newchain.Elements[f])
        for j in range(0, len(chain.Nodes[i].To)):
            t = chain.Nodes[i].To[j].Num
            newchain.Nodes[i].set_to(newchain.Elements[t])

    for i in range(0, newchain.Elements_count):
        f = chain.Elements[i].From.Key
        t = chain.Elements[i].To.Key
        newchain.Elements[i].set_from(newchain.Nodes[f-1])
        newchain.Elements[i].set_to(newchain.Nodes[t-1])
    print(newchain.Nodes)

    return newchain