import copy
from collections import deque

def bfs(i, j, now_board, visited):
    tmp_lst = [(i, j)]
    visited[i][j] = 1
    cnt = 1
    q = deque()
    q.append((i, j))
    score = 0
    while q:
        r, c = q.popleft()
        for dr, dc in ((0, 1), (1, 0), (-1, 0), (0, -1)):
            nr = r + dr
            nc = c + dc
            if 0 <= nr < 5 and 0 <= nc < 5 and not visited[nr][nc] and now_board[nr][nc] == now_board[i][j]:
                q.append((nr, nc))
                visited[nr][nc] = 1
                tmp_lst.append((nr, nc))
                cnt += 1

    if cnt >= 3:
        score += cnt
        for a, b in tmp_lst:
            now_board[a][b] = 0
        return cnt
    else:
        return 0
def play(now_board):
    delete_num = 0
    visited = [[0 for _ in range(5)] for _ in range(5)]
    for i in range(5):
        for j in range(5):
            if not visited[i][j]:
                delete_num += bfs(i, j, now_board, visited)

    return (delete_num, now_board)

def rotate(ci, cj, angle):
    now_board = copy.deepcopy(board)
    if angle == 90:
        now_board[ci - 1][cj + 1] = board[ci - 1][cj - 1] # 우상
        now_board[ci][cj + 1] = board[ci - 1][cj] # 우
        now_board[ci + 1][cj + 1] = board[ci - 1][cj + 1] # 우하

        now_board[ci + 1][cj + 1] = board[ci - 1][cj + 1] # 하우
        now_board[ci + 1][cj] = board[ci][cj + 1] # 하
        now_board[ci + 1][cj - 1] = board[ci + 1][cj + 1] # 하좌

        now_board[ci + 1][cj - 1] = board[ci + 1][cj + 1] # 좌하
        now_board[ci][cj - 1] = board[ci + 1][cj] # 좌
        now_board[ci - 1][cj - 1] = board[ci + 1][cj - 1] # 좌상

        now_board[ci - 1][cj - 1] = board[ci + 1][cj - 1] # 상좌
        now_board[ci - 1][cj] = board[ci][cj - 1] # 상
        now_board[ci - 1][cj + 1] = board[ci - 1][cj - 1] # 상우

    elif angle == 180:
        now_board[ci - 1][cj + 1] = board[ci + 1][cj - 1] # 우상
        now_board[ci][cj + 1] = board[ci][cj - 1] # 우
        now_board[ci + 1][cj + 1] = board[ci - 1][cj - 1] # 우하

        now_board[ci + 1][cj + 1] = board[ci - 1][cj - 1] # 하우
        now_board[ci + 1][cj] = board[ci - 1][cj] # 하
        now_board[ci + 1][cj - 1] = board[ci - 1][cj + 1] # 하좌

        now_board[ci + 1][cj - 1] = board[ci - 1][cj + 1] # 좌하
        now_board[ci][cj - 1] = board[ci][cj + 1] # 좌
        now_board[ci - 1][cj - 1] = board[ci + 1][cj + 1] # 좌상

        now_board[ci - 1][cj - 1] = board[ci + 1][cj + 1] # 상좌
        now_board[ci - 1][cj] = board[ci + 1][cj] # 상
        now_board[ci - 1][cj + 1] = board[ci + 1][cj - 1] # 상우

    else:
        now_board[ci - 1][cj + 1] = board[ci + 1][cj + 1]  # 우상
        now_board[ci][cj + 1] = board[ci + 1][cj]  # 우
        now_board[ci + 1][cj + 1] = board[ci + 1][cj - 1]  # 우하

        now_board[ci + 1][cj + 1] = board[ci + 1][cj - 1]  # 하우
        now_board[ci + 1][cj] = board[ci][cj - 1]  # 하
        now_board[ci + 1][cj - 1] = board[ci - 1][cj - 1]  # 하좌

        now_board[ci + 1][cj - 1] = board[ci - 1][cj - 1] # 좌하
        now_board[ci][cj - 1] = board[ci - 1][cj] # 좌
        now_board[ci - 1][cj - 1] = board[ci - 1][cj + 1] # 좌상

        now_board[ci - 1][cj - 1] = board[ci - 1][cj + 1] # 상좌
        now_board[ci - 1][cj] = board[ci][cj + 1] # 상
        now_board[ci - 1][cj + 1] = board[ci + 1][cj + 1] # 상우

    return now_board

k, m = map(int, input().split())
board = [list(map(int, input().split())) for _ in range(5)]
artifact = list(map(int, input().split()))
artifact_idx = 0

for _ in range(k): # k턴 진행
    max_score = 0
    min_angle = 360
    max_board = []
    for i in range(1, 4):
        for j in range(1, 4): # 중심 좌표 회전
            for r in (90, 180, 270):
                new_board = rotate(i, j, r)
                played_score, played_board = play(new_board)
                if max_score < played_score and min_angle > r:
                    max_score = played_score
                    min_angle = r
                    max_board = played_board

    board = max_board
    while max_board != []:
        for j in range(5):
            for i in range(4, -1, -1):
                if max_board[i][j] == 0:
                    max_board[i][j] = artifact[artifact_idx]
                    artifact_idx += 1
        played_score, played_board = play(board)
        if played_score:
            max_score += played_score
            board = played_board
        else:
            break

    if max_score:
        print(max_score, end=' ')