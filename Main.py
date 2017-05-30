# Курсовая работа по Теоретическим Основам Электротехники
# Весенний семестр 2017 года
# Авторы: Петров И., Правиленко М., Клюкин А.

# Главный модуль программы
import Classes
import CreateChain
import MeshMethod
import OverlayMethod
import CopyChain
import copy

chain = CreateChain.default_chain2()
OverlayMethod.overlay_method(chain)
Classes.Chain.output_chain(chain)

__all__ = ['Classes', Classes.Element, Classes.I, Classes.V, Classes.R, Classes.L, Classes.C, Classes.SC, Classes.Chain,
           Classes.Node]

__all__ = ['CreateChain', 'MeshMethod', 'OverlayMethod', 'CopyChain']
