# Курсовая работа по Теоретическим Основам Электротехники
# Весенний семестр 2017 года
# Авторы: Петров И., Правиленко М., Клюкин А.

# Главный модуль программы
import Classes
import CreateChain
import MeshMethod
import LaplaceTransformDomain as LTD
import sympy
import numpy

# Модуль 1: t-область
# chain = CreateChain.default_chain()
# chain = CreateChain.create_chain()
# MeshMethod.mesh_method(chain)
# chain.output_chain()
# Модуль 2: S-область
HS_num, HS_den, H1S_den, H_num, H_den = LTD.HS_calc([[-2, -1], [1, 0]], [[1], [0]], [[1, 2]], 1)
print('H(S) =', sympy.sympify('('+HS_num+')/('+HS_den+')'))
print('H1(S) =', sympy.sympify('('+HS_num+')/('+H1S_den+')'))
ht = LTD.S2t(sympy.sympify('('+HS_num+')/('+HS_den+')'))
print('h(t) =', ht)
h1t = LTD.S2t(sympy.sympify('('+HS_num+')/('+H1S_den+')'))
print('h1(t) =', h1t)
FR, PR = LTD.FRandPR(H_num, H_den)
print('АЧХ =', FR)
print('ФЧХ =', PR)

__all__ = ['Classes', 'sympy', 'CreateChain', 'MeshMethod']
