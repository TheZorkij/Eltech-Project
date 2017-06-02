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


#chaine = CreateChain.default_chain()
#chain = CopyChain.copy_chain(chaine)
chain = CreateChain.Petrov_10var()
#chain = CreateChain.Pravilenko_11var()
#chain = CreateChain.default_chain2()
#Classes.Chain.output_chain(chain)
chain, A, B, C, D = OverlayMethod.overlay_method(chain)
Classes.Chain.output_chain(chain)
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
