from collections import deque

linked_list = deque()

N = int(input())
for _ in range(N):
    order = input().split()
    if order[0] == 'push_front':
        linked_list.appendleft(int(order[1]))
    elif order[0] == 'push_back':
        linked_list.append(int(order[1]))
    elif order[0] == 'pop_front':
        print(linked_list.popleft())
    elif order[0] == 'pop_back':
        print(linked_list.pop())
    elif order[0] == 'size':
        print(len(linked_list))
    elif order[0] == 'empty':
        if len(linked_list):
            print(0)
        else:
            print(1)
    elif order[0] == 'front':
        print(linked_list[0])
    else:
        print(linked_list[-1])