import sys
from collections import deque

input = sys.stdin.readline

N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]

turn = [[0] * M for _ in range(N)]  # 공격한 턴수를 기록(최근공격 체크)

def bfs(si, sj, ei, ej):
    q = deque()
    v = [[[] for _ in range(M)] for _ in range(N)]  # 경로를 표시하기 위한 visited

    q.append((si, sj))
    v[si][sj] = (si, sj)
    d = arr[si][sj]

    while q:
        ci, cj = q.popleft()
        if (ci, cj) == (ei, ej):    # 목적지 좌표 도달
            arr[ei][ej] = max(0, arr[ei][ej] - d)   # 목표를 d 만큼 타격
            while True:
                ci, cj = v[ci][cj]  # 직전 좌표
                if (ci, cj) == (si, sj):    # 시작(공격자)까지 되짚어 왔으면 종료
                    return True
                else:
                    arr[ci][cj] = max(0, arr[ci][cj] - d // 2)
                    fset.add((ci, cj))

        # 우선순위: 우/하/좌/상 (미방문, 조건 : 포탑있어야함)
        for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            ni, nj = (ci + di) % N, (cj + dj) % M # 반대편으로 이동
            if len(v[ni][nj]) == 0 and arr[ni][nj] > 0:
                q.append((ni, nj))
                v[ni][nj] = (ci, cj)

    # 목적지를 찾지 못함!!
    return False

def bomb(si, sj, ei, ej):
    d = arr[si][sj]
    arr[ei][ej] = max(0, arr[ei][ej])

    for di, dj in ((0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)):
        ni, nj = (ei + di) % N, (ej + dj) % M
        if (ni, nj) != (si, sj):
            arr[ni][nj] = max(0, arr[ni][nj] - d // 2)
            fset.add((ni, nj))

for T in range(1, K + 1):
    # [1] 공격자 선정 : 공격력 낮은 -> 가장 최근 공격자 -> 행 + 열(큰) -> 열(큰)
    mn, mx_turn, si, sj = 5001, 0, -1, -1
    for i in range(N):
        for j in range(M):
            if arr[i][j] <= 0: continue # 포탑이 아니면 스킵
            if mn > arr[i][j] or (mn == arr[i][j] and mx_turn < turn[i][j]) or \
                (mn == arr[i][j] and mx_turn == turn[i][j] and si + sj < i + j) or \
                (mn == arr[i][j] and mx_turn == turn[i][j] and si + sj == i + j and sj < j):
                mn, mx_turn, si, sj = arr[i][j], turn[i][j], i, j   # si, sj 공격자

    arr[si][sj] += (N + M) # 공격력 상승
    turn[si][sj] = T       # 이번 턴에 공격

    # [2] 공격(공격당할 포탑 선정) & 포탑부서짐
    # 2-1) 공격 당할 포탑 선정 : 공격력 높은 -> 가장 오래전 공격 -> 행 + 열(작은) -> 열(작은)

    mx, mn_turn, ei, ej = 0, T, N, M
    for i in range(N):
        for j in range(M):
            if arr[i][j] <= 0: continue # 포탑이 아니면 스킵
            if mx < arr[i][j] or (mn == arr[i][j] and mn_turn > turn[i][j]) or \
                (mx == arr[i][j] and mn_turn == turn[i][j] and ei + ej > i + j) or \
                (mx == arr[i][j] and mn_turn == turn[i][j] and ei + ej == i + j and ej > j):
                mx, mn_turn, ei, ej = arr[i][j], turn[i][j], i, j   # ei, ej 공격 대상자

    # 2-2) 레이저 공격 (우하좌상 순서로 최단거리이동 - BFS, %N, %M 처리 필요 (양끝연결))
    fset = set()
    fset.add((si, sj))
    fset.add((ei, ej))
    if bfs(si, sj, ei, ej) == False:    # 레이저 공격 실패

        # 2-3) 포탄공격 (레이저로 목적지 도달 목할 경우)
        bomb(si, sj, ei, ej)

    # [3] 포탑 정비 (공격에 상관 없었던 포탑들 + 1)
    for i in range(N):
        for j in range(M):
            if arr[i][j] != 0 and (i, j) not in fset:
                arr[i][j] += 1

print(max(map(max, arr)))