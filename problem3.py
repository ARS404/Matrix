from matrix import *


A = SquareMatrix(read_matrix('input3.txt').matrix)  # считываем матрицу A
print(A)
print()

print(A.characteristic_polynomial_to_latex('A'))  # находим характеристический многочлен A

x = (A**2 - 3*A + 2*A.identity_matrix())**2
print(x.to_latex())
print()
x = x.inverse_matrix()
print(x.to_latex())  # вычисляем заданную матрицу от A
print()
print(x.determinant())  # находим её определитель
