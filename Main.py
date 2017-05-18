# Курсовая работа по Теоретическим Основам Электротехники
# Весенний семестр 2017 года
# Авторы: Петров И., Правиленко М., Клюкин А.

# Главный модуль программы
import Classes
import CreateChain
import MeshMethod
import OverlayMethod
import CopyChain

chain = CreateChain.default_chain()
chain2 = CopyChain.copy_chain(chain)
#chain = CreateChain.create_chain()
#MeshMethod.mesh_method(chain)
#MeshMethod.mesh_method(chain2)
#OverlayMethod.overlay_method(chain)
chain.output_chain()

__all__ = ['Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.SC, Classes.Chain,
           Classes.Node]

__all__ = ['CreateChain', 'MeshMethod', 'OverlayMethod', 'CopyChain']
