from matrix import *


A = read_matrix('input.txt')
A = SquareMatrix(A.matrix)
print(A)
print()
print(A.characteristic_polynomial())
print()
print(A.integer_characteristic_polynomial_to_latex('A'))
print()
X = ((A * A - A*3) + (A.identity_matrix()*2))**2
print(X)
print()
print(X.inverse_matrix())
print()
print(X.determinant())
