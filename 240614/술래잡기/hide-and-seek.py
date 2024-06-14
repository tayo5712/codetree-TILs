N, MM, H, K = map(int, input().split())
# 방향 상 우 하 좌

# 도망자 좌표 입력
arr = []
for _ in range(MM):
    arr.append(list(map(int, input().split())))

# 나무 좌표 입력
tree = set()
for _ in range(H):
    i, j = map(int, input().split())
    tree.add((i, j))

# 0(좌) 1(우) 2(하) 3(상)

di = [0, 0, 1, -1]
dj = [-1, 1, 0, 0]
opp = {0:1, 1:0, 2:3, 3:2}  # 반대 방향향

# 방향 상 우 하 좌    tagger(술래)방향 (바깥으로 돌 때 방향)
tdi = [-1, 0, 1, 0]
tdj = [0, 1, 0, -1]

mx_cnt, cnt, flag, val =  1, 0, 0, 1
M = (N + 1) // 2
ti, tj, td = M, M, 0

ans = 0
for k in range(1, K + 1):   # k턴만큼 게임 진행
    # [1] 도망자의 이동(arr)
    for i in range(len(arr)):
        if abs(arr[i][0] - ti) + abs(arr[i][1] - tj) <= 3:  # 술래와 거리 3이하인 경우 이동
            ni, nj = arr[i][0] + di[arr[i][2]], arr[i][1] + dj[arr[i][2]]
            if 1 <= ni <= N and 1 <= nj <= N:   # 범위 내면 술래체크
                if (ni, nj) != (ti, tj):
                    arr[i][0], arr[i][1] = ni, nj
            else:   # 범위 밖 => 방향 반대
                nd = opp[arr[i][2]] # 방향 전환
                ni, nj = arr[i][0] + di[nd], arr[i][1] + dj[nd]
                if (ni, nj) != (ti, tj):
                    arr[i] = [ni, nj, nd]
                else:
                    arr[i][2] = nd

    # [2] 술래의 이동
    cnt += 1
    ti, tj = ti + tdi[td], tj + tdj[td]
    if (ti, tj) == (1, 1):
        mx_cnt, cnt, flag, val = N, 1, 1, -1
        td = 2  # 초기 방향은 아래로 (하)
    elif (ti, tj) == (M, M):    # 좌표가 중앙이면 바깥으로 동작
        mx_cnt, cnt, flag, val = 1, 0, 0, 1
        td = 0
    else:
        if cnt == mx_cnt:   # 방향 변경
            cnt = 0
            td = (td + val) % 4
            if flag == 0:
                flag = 1
            else:
                flag = 0    # 두 분에 한번씩 길이 증가
                mx_cnt += 1

    # [3] 도망자 잡기(술래자리포함 3칸 : 나무가 없는 도망자면 잡기)
    tset = set(((ti, tj), (ti + tdi[td], tj + tdj[td]), (ti + tdi[td] * 2, tj + tdj[td] * 2)))
    for i in range(len(arr) - 1, -1, -1):
        if (arr[i][0], arr[i][1]) in tset and (arr[i][0], arr[i][1]) not in tree:
            arr.pop()
            ans += k

    # 도망자가 없다면 더이상 점수도 없음
    if len(arr) < 1:
        break

print(ans)