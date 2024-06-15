N, M, K = map(int, input().split())
arr = [list(map(int, input().split())) for _ in range(N)]
for _ in range(M):
    i, j = map(lambda x : int(x) - 1, input().split())
    arr[i][j] -= 1  # 사람은 - 1 (같은 위치에 여러명 있을 수 있음)

ei, ej = map(lambda x : int(x) - 1, input().split())
arr[ei][ej] = -11

def find_square(arr):

    for l in range(2, N):

        for si in range(N - l):
            for sj in range(N - l):
                exit_flag = False
                people_flag = False
                for i in range(l):
                    for j in range(l):
                        if arr[si + i][sj + j] == -11:
                            exit_flag = True
                        elif arr[si + i][sj + j] < 0:
                            people_flag = True

                if exit_flag and people_flag:
                    return (si, sj, l)


def find_exit(arr):
    for i in range(N):
        for j in range(N):
            if arr[i][j] == -11:
                return (i, j)

# K 턴 또는 모두탈출까지 모든 사람의 이동거리 누적, 모두 탈출했으면 종료
ans = 0
cnt = M
for _ in range(K):
    # [1] 모든 참가자 (동시에) 한 칸 이동(출구 최단거리 방향 상/하 우선)
    # 출구에 도착하면 즉시 탈출
    narr = [x[:] for x in arr]
    for i in range(N):
        for j in range(N):
            if -11 < arr[i][j] < 0: # 사람인 경우
                dist = abs(ei - i) + abs(ej - j)
                # 네 방향 (상하우선), 범위내, 벽 아니고 <= 0, 거리가 dist보다 작으면
                for di, dj in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                    ni, nj = i + di, j + dj
                    if 0 <= ni < N and 0 <= nj < N and arr[ni][nj] <= 0 and dist > abs(ei-ni) + abs(ej-nj):
                        ans += arr[i][j]    # 현재 인원수가 누적
                        narr[i][j] -= arr[i][j] # 이동처리
                        if arr[ni][nj] == -11:
                            cnt += arr[i][j]
                        else:        # 일반 빈칸 또는 사람 있는곳이면
                            narr[ni][nj] += arr[i][j]   # 들어온 인원 추가
                        break
    arr = narr
    if cnt == 0:
        break
    # [2] 미로회전 (출구와 한 명이상 참가자를 포함하는 가장 작은 정사각형
    # 시계방향 90도 : 같은크기 -> 좌상단행열, 내구도 - 1
    si, sj, L = find_square(arr)

    narr = [x[:] for x in arr]
    for i in range(L):
        for j in range(L):
            narr[si + i][sj + j] = arr[si + L - 1 - j][sj + i]
            if narr[si + i][sj + j] > 0:    # 벽이면 회전시 1 감소
                narr[si + i][sj + j] -= 1

    arr = narr
    # 회전으로 달라졌으므로.. 비상구 위치 저장
    ei, ej = find_exit(arr)

print(-ans)
print(ei + 1, ej + 1)