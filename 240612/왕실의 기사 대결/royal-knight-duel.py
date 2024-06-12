from collections import deque

# 방향 : 상 우 하 좌

di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]

N, M, Q = map(int, input().split())
arr = [[2] * (N + 2)] + [[2] + list(map(int, input().split())) + [2] for _ in range(N)] + [[2] * (N + 2)] # 벽으로 둘러싸기
units = {}

v = [[0] * (N + 2) for _ in range(N + 2)]
init_k = [0] * (M + 1) # 초기 체력 저장용
for m in range(1, M + 1):
    si, sj, h, w, k = map(int, input().split())
    units[m] = [si, sj, h, w, k]
    init_k[m] = k
    for i in range(si, sj + h):
        v[i][sj:sj + w] = [m] * w

def push_unit(start, dr):   # start를 밀고 연쇄처리
    q = deque()             # push 후보를 저장
    pset = set()            # 이동 기사 번호 저장
    damage = [0] * (M + 1)  # 각 유닛 별 데미지

    q.append(start)         # 초기 데이터
    pset.add(start)

    while q:
        cur = q.popleft()               # q에서 데이터 한 개 꺼냄
        ci, cj, h, w, k = units[cur]

        # 명령 받은 방향, 벽이 아니면, 겹치는 다른조각이면 -> 큐
        ni, nj = ci + di[dr], cj + dj[dr]
        for i in range(ni, ni + h):
            for j in range(nj, nj + w):
                if arr[i][j] == 2:      # 벽인 경우 리턴
                    return
                if arr[i][j] == 1:      # 함정인 경우 데미지 누적
                    damage[cur] += 1

        # 겹치는 다른 유닛 있는 경우 큐에 추가 (모든 유닛 체크)
        for idx in units:
            if idx in pset: continue    # 이미 움직일 대상이면 x
            ti, tj, th, tw, tk = units[idx]

            # 겹치는 경우
            if ni <= ti + th - 1 and ni + h - 1 >= ti and tj <= nj + w - 1 and nj <= tj + tw - 1:
                q.append(idx)
                pset.add(idx)

    # 명령 받은 기사는 데미지 입지 않음
    damage[start] = 0
    # 이동, 데미지가 체력이상이면 삭제처리
    for idx in pset:
        si, sj, h, w, k = units[idx]
        if k <= damage[idx]:
            units.pop(idx)
        else:
            ni, nj = si + di[dr], sj + dj[dr]
            units[idx] = [ni, nj, h, w, k - damage[idx]]


for _ in range(Q): # 명령 입력받고 처리 ( 있는 유닛만 처리 )
    idx, dr = map(int, input().split())
    if idx in units:
        push_unit(idx, dr) # 명령 받은 기사(연쇄적으로 밀기 -> 벽이 없는 경우)


ans = 0
for idx in units:
    ans += init_k[idx] - units[idx][4]
    
print(ans)