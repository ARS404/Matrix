from matrix import *


A = read_matrix('input5_A.txt')  # считываем матрицу A
B = read_matrix('input5_B.txt')  # считываем матрицу B

x = SquareMatrix((A*B).matrix)

print(x.to_latex())
print()

print(x.characteristic_polynomial_to_latex('AB'))
