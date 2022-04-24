from matrix import *


A = read_matrix('input.txt')
A = SquareMatrix(A.matrix)
print(A.rank())
