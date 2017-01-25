# array = []
# sumK = 0
# while True:
#     v = int(input())
#     array += [v]
#     v = v ** 2
#     sumK += v
#     if sum(array) == 0:
#         break
# print(array)
# print(sumK)

# n = int(input())
# k = 0
# for i in range(1, n+1):
#     for j in range(1, i+1):
#         print(i, end=' ')
#         k += 1
#         if k == n:
#             break
#     if k == n:
#         break

# list = [int(i) for i in input().split()]
# x = int(input())
# # print(list)
# # print(x)
# index = 0
# xIS = False
# for i in list:
#     if i == x:
#         print(index, end=' ')
#         xIS = True
#     index += 1
#
# if not xIS:
#     print('Отсутствует')

# array = []
# resultArray = []
# array.append([int(i) for i in input().split()])
# for i in range(len(array[0])):
#     k = [i for i in input().split()]
#     if k[0] != 'end':
#         array.append([int(i) for i in k])
# print(array)

s = int(input())
array = [[j for j in range(s)] for i in range(s)]

n = 1
k = -1
i = 0
j = -1
maxN = s ** 2
s += 1
while n <= maxN:
    j += 1
    s -= 1
    for dj in range(j, s, 1):
        array[i][dj] = n
        n += 1
        j = dj
        if n > maxN:
            break
    if n > maxN:
        break

    for di in range(i+1, s, 1):
        array[di][j] = n
        n += 1
        i = di
        if n > maxN:
            break
    if n > maxN:
        break

    for dj in range(j-1, k, -1):
        array[i][dj] = n
        n += 1
        j = dj
        if n > maxN:
            break
    if n > maxN:
        break

    k += 1
    for di in range(i-1, k, -1):
        array[di][j] = n
        n += 1
        i = di
        if n > maxN:
            break

for i in range(len(array)):
    for j in range(len(array)):
        print(array[i][j], end=' ')
    print()


