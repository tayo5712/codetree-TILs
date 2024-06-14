'''
4 3 3
0 0 1 0
0 0 1 0
1 1 0 1
0 0 2 0
1 2 2 1 5
2 1 2 1 1
3 2 1 2 3
1 2
2 1
3 3

anwer 3
'''

from collections import deque

def move(idx, dir):
    damage = [0] * (N + 1)
    q = deque()
    q.append(idx)
    move_knights = set()
    move_knights.add(idx)
    while q:
        cur = q.popleft()
        ci, cj, ch, cw, ck = knights[cur]
        ni, nj = ci + di[dir], cj + dj[dir]
        for i in range(ni, ni + ch):
            for j in range(nj, nj + cw):
                if board[i][j] == 1:
                    damage[cur] += 1
                elif board[i][j] == 2:
                    return

        # 겹치는지 확인
        for k in knights:
            if k in move_knights: continue
            oi, oj, oh, ow, ok = knights[k]
            if (ni <= oi + oh - 1) and (oi <= ni + ch - 1) and (nj <= oj + ow - 1) and (oj <= nj + cw - 1):
                q.append(k)
                move_knights.add(k)

    damage[idx] = 0 # 시작한 사람은 데미지를 입지 않음
    for knight in move_knights:
        r, c, h, w, k = knights[knight]
        if k - damage[knight] <= 0:
            knights.pop(knight)
        else:
            knights[knight] = [r + di[dir], c + dj[dir], h, w, k - damage[knight]]

# 상 우 하 좌
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

L, N, Q = map(int, input().split())
board =  [[2] * (L + 2)]+ [[2] + list(map(int, input().split())) + [2] for _ in range(L)] + [[2] * (L + 2)]
knights = {}
init_health = [0] * (N + 1)
for i in range(1, N + 1):
    r, c, h, w, k = map(int, input().split())
    knights[i] = [r, c, h, w, k]
    init_health[i] = k

for _ in range(Q):
    idx, dir = map(int, input().split())
    if idx in knights:
        move(idx, dir)

ans = 0
for k in knights:
    ans += init_health[k] - knights[k][4]

print(ans)