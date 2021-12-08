"""
этот файл содержит код для решения 4 задачи.

"""


def main():
    # считываем матрицу и записваем в список списков
    matrix = []
    with open('input4.txt', 'r') as f:
        n = int(f.readline())
        for _ in range(n):
            matrix.append(list(f.readline().replace('в€’', '-').split()))
    ans = [0 for _ in range(n+1)]  # тут в i-той ячейке храним коэфицент при x^i

    def create_permutations(cur_per):
        # перебор возможных перестановок и подсчёт степени вхождения в них x
        def sign():
            # определение знака перестановк
            per = cur_per
            s = 0
            for j in range(n):
                for k in range(j+1, n):
                    if per[j] > per[k]:
                        s += 1
            s %= 2
            if s:
                return -1
            return 1

        if len(cur_per) == n:
            deg_x = 0
            prod = 1
            for i in range(n):
                try:
                    nb = int(matrix[i][cur_per[i]])
                    prod *= nb
                except:
                    deg_x += 1
            prod *= sign()
            ans[deg_x] += prod  # изменяем соответствующий коэфицент
            return
        for i in range(n):
            if i not in cur_per:
                cur_per.append(i)
                create_permutations(cur_per)
                cur_per.pop()
        return
    
    create_permutations([])
    print(ans)
    print(ans[5])


if __name__ == '__main__':
    main()
