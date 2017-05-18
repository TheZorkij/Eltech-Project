import Classes
import copy

def copy_chain(chain):
    newchain = Classes.Chain
    #print(id(newchain))
    #print(id(chain))
    newchain.Nodes_count = chain.Nodes_count
    print(id(newchain.Nodes_count))
    print(id(chain.Nodes_count))
    i = 0
    while i < newchain.Nodes_count:
        newchain.Nodes.append(Classes.Node(i + 1))
        newchain.Nodes[i].To = []
        newchain.Nodes[i].From = []
        i += 1

    newchain.Elements_count = copy.deepcopy(chain.Elements_count)
    for i in range(0, newchain.Elements_count):
        if chain.Elements[i].Name == 'R':
            newchain.Elements.append(Classes.R('R', copy.deepcopy(chain.Elements[i].Resistance)))
        if chain.Elements[i].Name == 'V':
            newchain.Elements.append(Classes.V('V', copy.deepcopy(chain.Elements[i].Voltage)))
        if chain.Elements[i].Name == 'I':
            newchain.Elements.append(Classes.I('I', copy.deepcopy(chain.Elements[i].Amperage)))
        #print(id(newchain.Elements[i]))
        #print(id(chain.Elements[i]))

    for i in range(0, chain.Nodes_count):
        for j in range(0, len(chain.Nodes[i].From)):
            newchain.Nodes[i].set_from(copy.deepcopy(chain.Nodes[i].From[j]))
        for j in range(0, len(chain.Nodes[i].To)):
            newchain.Nodes[i].set_to(copy.deepcopy(chain.Nodes[i].To[j]))

    for i in range(0, chain.Elements_count):
        newchain.Elements[i].set_from(copy.deepcopy(chain.Elements[i].From))
        newchain.Elements[i].set_to(copy.deepcopy(chain.Elements[i].To))

    return newchain