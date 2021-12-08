from matrix import *


A = SquareMatrix(read_matrix('input2_A.txt').matrix)  # считываем матрицу A
B = SquareMatrix(read_matrix('input2_B.txt').matrix)  # считываем матрицу B
C = SquareMatrix(read_matrix('input2_C.txt').matrix)  # считываем матрицу C
D = SquareMatrix(read_matrix('input2_D.txt').matrix)  # считываем матрицу D

y = A.inverse_matrix() * D * C.inverse_matrix()
print(y.to_latex())
print()

y = y.inverse_matrix()
print(y.to_latex())
print()

x = y - B
print(x.to_latex())
