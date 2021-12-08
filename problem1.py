import copy
'''
Данный файл использован для решения первой задачи.
В нём содержится класс Permutation, который использется для операция с 
перестановками (композиция, которая обозначена как умножение)
'''


class Permutation(object):

    def __init__(self, data):
        new_data = copy.deepcopy(data)
        new_data.insert(0, None)
        self.size = len(new_data)-1
        self.data = new_data

    def __str__(self):
        ret = '\ '.join(map(str, self.data[1:]))
        ret = '(' + ret + ')'
        return ret

    def __eq__(self, other):
        if self.size != other.size:
            return False
        for i in range(self.size):
            if self.data[i] != other.data[i]:
                return False
        return True

    def __mul__(self, other):
        if self.size != other.size:
            print('Перестановку можно умножать только на другую перестанвку '
                  'такого же размера')
            raise TypeError
        ret = []
        for i in range(1, self.size+1):
            ret.append(self.data[other.data[i]])
        return Permutation(ret)


def main():
    a = Permutation([6,7,3,1,4,2,5,8])  # левая скобка при подсчёте t после преобразований
    b = Permutation([3,8,5,1,2,7,6,4])  # правая скобка при подсчёте t после пеобразований
    s = a*b
    x = Permutation([1, 2, 3, 4, 5, 6, 7, 8])
    for i in range(161):  # вычисление t
        x = x * s
    n = x.size
    phi = Permutation([7, 1, 8, 6, 4, 3, 5, 2])

    def create_permutations(cur_per):  # полный перебор вариантов для \sigma
        if len(cur_per) == n:
            sigma = Permutation(cur_per)
            if sigma * (phi * sigma) == x:
                print(sigma)
            return
        for i in range(1, n+1):
            if i not in cur_per:
                cur_per.append(i)
                create_permutations(cur_per)
                cur_per.pop()
        return

    create_permutations([])


if __name__ == '__main__':
    main()
