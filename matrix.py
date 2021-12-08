"""
Данный файл содержит файлы и функции, использованые для решения польшинства задач.

class Fraction - описывает рациональные числа и базовые операции над ними

class Matrix - описывает матрицы и операции над ними

class SquareMatrix - унаследован от Matrix, используется для работы с квадратными матрицами

def read_matrix - функция, которая на ввод получает имя файла, в котором записано некоторе число n и матрица с
    n строками, возвращает Matrix, который соответствует вводу.

def sign - функция, которая принимает число и возвращает его знак.


все классы, описанные в файле имеют 2 способа приведения к строке: стандартный , то есть str (его удобно выводить в консоль)
    и to_latex (возвращает текст для вставки в латех)
"""


import functools
import copy


class Fraction(object):
    
    def __init__(self, *args):
        if len(args) == 1:
            self.numerator = int(args[0])
            self.denominator = 1
        else:
            if args[1] == 0:
                raise FractionError(args[0], args[1])
            self.numerator = int(args[0])
            self.denominator = int(args[1])
    
    def __str__(self):
        if self.numerator == 0:
            return '0'
        if self.denominator == 1:
            return str(self.numerator)
        ret = '{}/{}'.format(self.numerator, self.denominator)
        return ret

    def __repr__(self):
        if self.numerator == 0:
            return '0'
        if self.denominator == 1:
            return str(self.numerator)
        ret = '{}/{}'.format(self.numerator, self.denominator)
        return ret
    
    def __add__(self, other):
        if Fraction in type(other).__mro__:
            numen = self.numerator * other.denominator + \
                    other.numerator * self.denominator
            denom = self.denominator * other.denominator
            ret = Fraction(numen, denom).reduced()
            if ret.numerator == 0:
                return Fraction(0)
            return ret
        else:
            return self + Fraction(other)

    def __sub__(self, other):
        if Fraction in type(other).__mro__:
            numen = self.numerator * other.denominator - \
                    other.numerator * self.denominator
            denom = self.denominator * other.denominator
            ret = Fraction(numen, denom).reduced()
            if ret.numerator == 0:
                return Fraction(0)
            return ret
        else:
            return self - Fraction(other)

    def __mul__(self, other):
        if Fraction in type(other).__mro__:
            numen = self.numerator * other.numerator
            denom = self.denominator * other.denominator
            ret = Fraction(numen, denom).reduced()
            if ret.numerator == 0:
                return Fraction(0)
            return ret
        else:
            return self * Fraction(other)

    __rmul__ = __mul__

    def __truediv__(self, other):
        if Fraction in type(other).__mro__:
            if other.numerator == 0:
                return Fraction(0)
            numen = self.numerator * other.denominator
            denom = self.denominator * other.numerator
            ret = Fraction(numen, denom).reduced()
            if ret.numerator == 0:
                return Fraction(0)
            return ret
        else:
            return self / Fraction(other)

    def __idiv__(self, other):
        self = self.__truediv__(other)
        return self

    def __idiv__(self, other):
        x = self.__truediv__(other)
        self.numerator, self.denominator = x.numerator, x.denominator
        return self

    def __eq__(self, other):
        if Fraction in type(other).__mro__:
            return self.numerator == other.numerator and \
                   self.denominator == other.denominator
        else:
            return self == Fraction(other)

    def reduced(self):
        a = abs(copy.deepcopy(self.numerator))
        b = abs(copy.deepcopy(self.denominator))
        while a != 0 and b != 0:
            a %= b
            a, b = b, a
        x = a + b
        self.numerator //= x
        self.denominator //= x
        if self.denominator < 0 and self.numerator < 0:
            self.numerator = abs(self.numerator)
            self.denominator = abs(self.denominator)
        elif self.numerator > 0 and self.denominator < 0:
            self.numerator *= -1
            self.denominator *= -1
        return self

    def to_latex(self):
        if self.numerator == 0:
            return '0'
        if self.denominator == 1:
            return str(self.numerator)
        ret = '\\frac{' + str(self.numerator) + '}{' + \
              str(self.denominator) + '}'
        return ret


class FractionError(BaseException):

    def __init__(self, numerator, denominator):
        self.numerator = numerator
        self.denominator = denominator


class Matrix(object):

    def __init__(self, matrix):
        self.matrix = copy.deepcopy(matrix)

    def __str__(self):
        string_list = list()
        for i in range(len(self.matrix)):
            string_list.append(' '.join(map(str, self.matrix[i])))
        ret = '\n'.join(string_list)
        return ret

    def to_latex(self):
        ret_list = []
        for line in self.matrix:
            ret_list.append(' & '.join(map(lambda x: x.to_latex(), line)))
        ret = '\\\\\n'.join(ret_list)
        return ret

    def to_wolfram(self):
        ret = '('
        for s in self.matrix:
            ret += '(' + ', '.join(map(str, s)) + '), '
        ret = ret[:-2]
        ret += ')'
        return ret

    def size(self):
        return len(self.matrix), len(self.matrix[0])

    def validate(func):
        @functools.wraps(func)
        def wrapper(self, other):

            if func == self.__add__.__wrapped__:
                if self.size() != other.size():
                    raise MatrixError(self, other)
                return func(self, other)

            if func == self.__sub__.__wrapped__:
                if self.size() != other.size():
                    raise MatrixError(self, other)
                return func(self, other)

            if func == self.__mul__.__wrapped__ \
                    or func == self.__rmul__.__wrapped__:
                if type(other) == Matrix:
                    if self.size()[1] != other.size()[0]:
                        raise MatrixError(self, other)
                return func(self, other)
        return wrapper

    @validate
    def __add__(self, other):
        ret = list()
        n, m = self.size()
        for i in range(n):
            ret.append(list())
            for j in range(m):
                ret[-1].append(self.matrix[i][j] + other.matrix[i][j])
        return Matrix(ret)

    @validate
    def __sub__(self, other):
        ret = list()
        n, m = self.size()
        for i in range(n):
            ret.append(list())
            for j in range(m):
                ret[-1].append(self.matrix[i][j] - other.matrix[i][j])
        return Matrix(ret)

    @validate
    def __mul__(self, other):
        if Matrix in type(other).__mro__:
            ret = list()
            n, a = self.size()
            b, m = other.size()
            for i in range(n):
                ret.append(list())
                for k in range(m):
                    ret[-1].append(Fraction(0))
                    for j in range(a):
                        ret[-1][-1] += self.matrix[i][j] * other.matrix[j][k]
            return Matrix(ret)

        else:
            ret = list()
            for string in self.matrix:
                ret.append(list())
                for number in string:
                    ret[-1].append(number * other)
            return Matrix(ret)

    __rmul__ = __mul__

    @staticmethod
    def transposed(matrix):
        n, m = matrix.size()
        ret = list()
        for i in range(m):
            ret.append(list([None]) * n)
        for i in range(n):
            for k in range(m):
                ret[k][i] = matrix.matrix[i][k]
        return Matrix(ret)

    def transpose(self):
        self.matrix = Matrix.transposed(self).matrix
        return self


class SquareMatrix(Matrix):

    def __init__(self, matrix):
        Matrix.__init__(self, matrix)

    def __add__(self, other):
        u = Matrix(self.matrix)
        v = Matrix(other.matrix)
        return SquareMatrix((u+v).matrix)

    def __sub__(self, other):
        u = Matrix(self.matrix)
        v = Matrix(other.matrix)
        return SquareMatrix((u-v).matrix)

    def __mul__(self, other):
        u = Matrix(self.matrix)
        if Matrix in type(other).__mro__:
            v = Matrix(other.matrix)
            return SquareMatrix((u*v).matrix)
        else:
            return SquareMatrix((u*other).matrix)

    __rmul__ = __mul__

    def __pow__(self, power, modulo=None):
        if power == 0:
            return self.identity_matrix()
        if power == 1:
            return self
        ret = self.__pow__(power // 2)
        ret = ret * ret
        if power % 2:
            ret *= self
        return ret

    def identity_matrix(self):
        n = self.size()[0]
        ret = list()
        for i in range(n):
            ret.append(list())
            for k in range(n):
                if i == k:
                    ret[-1].append(1)
                else:
                    ret[-1].append(0)
        return SquareMatrix(ret)

    def determinant(self):
        deg_of_minus1 = 0
        data = copy.deepcopy(self.matrix)
        n = self.size()[0]
        if n == 1:
            return data[0][0]
        for curent_line in range(n):
            new_line = curent_line
            while new_line < n and data[new_line][curent_line] == 0:
                new_line += 1
            if new_line == n:
                return Fraction(0)
            if curent_line != new_line:
                data[curent_line], data[new_line] = \
                    data[new_line], data[curent_line]
                deg_of_minus1 += 1
            for line in range(curent_line+1, n):
                if data[line][curent_line] == 0:
                    continue
                delta = data[line][curent_line] / \
                    data[curent_line][curent_line]
                for ind in range(curent_line, n):
                    data[line][ind] -= data[curent_line][ind] * delta
        ret = (-1) ** deg_of_minus1
        for i in range(n):
            ret *= data[i][i]
        return ret

    def R(self, inds):
        data = self.matrix
        ret = []
        for line in range(len(data)):
            if line in inds:
                continue
            new_line = [data[line][i] for i in range(len(data)) if i not in inds]
            ret.append(new_line)
        return SquareMatrix(ret)

    def R_generator(self, m, ret, ind, ans):
        if len(ret) == m:
            ans.append(copy.deepcopy(ret))
            return ans
        if ind == self.size()[0]:
            return ans
        ret.append(copy.deepcopy(ind))
        ans = self.R_generator(m, ret, ind+1, ans)
        ret.pop()
        ans = self.R_generator(m, ret, ind+1, ans)
        return ans

    def characteristic_polynomial(self):
        polynomial = [Fraction(1)]
        n = self.size()[0]
        for k in range(n-1, 0, -1):
            R_sum = Fraction(0)
            inds_k = self.R_generator(k, [], 0, [])
            for inds in inds_k:
                R_sum += self.R(inds).determinant()
            R_sum *= (-1)**(n-k)
            polynomial.append(R_sum)
        polynomial.append(self.determinant())
        return polynomial

    def characteristic_polynomial_to_latex(self, name):
        n = self.size()[0]
        polynomial = self.characteristic_polynomial()
        ret = '\\chi_{' + name + '}(\\lambda) = \\lambda^{' + str(n) + '}'
        for k in range(1, n):
            ret += ' + ({})\\lambda^{}'.format(polynomial[k], n-k)
        ret += ' + ({})'.format(polynomial[-1])
        return ret

    def algebraic_complement(self, line, column):
        data = copy.deepcopy(self.matrix)
        ret_data = [[]]
        n = self.size()[0]
        for i in range(n):
            if i == line:
                continue
            for k in range(n):
                if k == column:
                    continue
                ret_data[-1].append(data[i][k])
            ret_data.append(list())
        ret_data.pop()
        return SquareMatrix(ret_data).determinant() * (-1)**(line+column)

    def inverse_matrix(self):
        det = self.determinant()
        if det == 0:
            print('Матрица необратима!')
            return
        ret_data = [[]]
        n = self.size()[0]
        for line in range(n):
            for column in range(n):
                ret_data[-1].append(self.algebraic_complement(line, column))
            ret_data.append(list())
        ret_data.pop()
        for i in range(n):
            for j in range(n):
                ret_data[i][j] /= det
        ret = SquareMatrix(ret_data)
        ret.transpose()
        return ret


class MatrixError(BaseException):

    def __init__(self, matrix1, matrix2):
        self.matrix1 = matrix1
        self.matrix2 = matrix2


class InvalidSolution(BaseException):

    def __init__(self, matrix, res):
        self.matrix = matrix
        self.free_column = res


def read_matrix(filename):
    with open(filename, 'r') as f:
        n = int(f.readline())
        data = []
        for _ in range(n):
            s = list(map(Fraction, f.readline().replace('в€’', '-').
                         replace('\n', '').split()))
            data.append(s)
    return Matrix(data)


def sign(x):
    if x == 0:
        return 0
    return x // abs(x)
