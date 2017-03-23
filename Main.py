# Курсовая работа по Теоретическим Основам Электротехники
# Весенний семестр 2017 года
# Авторы: Петров И., Правиленко М., Клюкин А.

# Главный модуль программы
import Classes
import CreateChain
import MeshMethod

chain = CreateChain.defaultchain()
#chain = CreateChain.create_chain()
MeshMethod.mesh_method(chain)
chain.output_chain()

__all__ = ['Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.Chain,
           Classes.Node]

__all__ = ['CreateChain', 'MeshMethod']