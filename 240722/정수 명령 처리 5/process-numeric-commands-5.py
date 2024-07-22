n = int(input())
lst = []
for _ in range(n):
    order = input().split()
    if order[0] == 'push_back':
        lst.append(int(order[1]))
    elif order[0] == 'pop_back':
        lst.pop()
    elif order[0] == 'size':
        print(len(lst))
    else:
        print(lst[int(order[1])-1])