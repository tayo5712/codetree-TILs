import sys

R, C, K = map(int, input().split())
score = 0
m = [[-1] * C for _ in range(R)]
gArr = [None] * K
di = [-1, 0, 1, 0]
dj = [0, 1, 0, -1]
v = [False] * K

def drop(idx, ci, cj, e):
    global score, rMax
    while True:  # move until available
        if ci == R - 2:  # exit at bottom
            break

        # go down
        if ((ci == -2 and m[ci + 2][cj] == -1) or
            (m[ci + 2][cj] == -1 and m[ci + 1][cj - 1] == -1 and m[ci + 1][cj + 1] == -1)):
            ci += 1
            continue

        # go left
        if cj >= 2:
            if ((ci == -2 and m[ci + 2][cj - 1] == -1) or
                ((ci == -1) and m[ci + 2][cj - 1] == -1 and m[ci + 1][cj - 1] == -1 and m[ci + 1][cj - 2] == -1) or
                (m[ci + 2][cj - 1] == -1 and m[ci + 1][cj - 1] == -1 and m[ci + 1][cj - 2] == -1 and m[ci][cj - 2] == -1)):
                ci += 1
                cj -= 1
                e = (e + 3) % 4
                continue

        # go right
        if cj < C - 2:
            if ((ci == -2 and m[ci + 2][cj + 1] == -1) or
                ((ci == -1) and m[ci + 2][cj + 1] == -1 and m[ci + 1][cj + 1] == -1 and m[ci + 1][cj + 2] == -1) or
                (m[ci + 2][cj + 1] == -1 and m[ci + 1][cj + 1] == -1 and m[ci + 1][cj + 2] == -1 and m[ci][cj + 2] == -1)):
                ci += 1
                cj += 1
                e = (e + 1) % 4
                continue

        # exit when cannot go anymore
        break

    # reset if golem located outside of the map
    if ci <= 0:
        initMap()
        return

    # mark golem on map
    m[ci][cj] = m[ci - 1][cj] = m[ci][cj + 1] = m[ci + 1][cj] = m[ci][cj - 1] = idx
    gArr[idx] = [ci, cj, e]

    moveGolem(idx)
    score += rMax

def moveGolem(idx):
    global rMax
    v[idx] = True  # visited

    # update rMax with the bottom of current golem
    ri = gArr[idx][0] + 2
    rMax = max(ri, rMax)

    # exit coord of current golem
    e = gArr[idx][2]
    ri = gArr[idx][0] + di[e]
    rj = gArr[idx][1] + dj[e]

    # find next golem close to current golem's exit
    for d in range(4):
        ni = ri + di[d]
        nj = rj + dj[d]

        if ni < 0 or ni >= R or nj < 0 or nj >= C:
            continue
        if m[ni][nj] == -1 or v[m[ni][nj]]:
            continue

        moveGolem(m[ni][nj])

def initMap():
    global m
    m = [[-1] * C for _ in range(R)]

for _ in range(K):
    c, e = map(int, input().split())
    c -= 1  # adjust column index
    rMax = 0
    v = [False] * K
    drop(_, -2, c, e)

print(score)