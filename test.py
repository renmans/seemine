import numpy as np

z = np.array([[i for i in range(5)] for _ in range(5)])
i = j = 0
for y in [a for a in [i-1, i, i+1] if a >= 0 and a <= len(z)-1]:
    for x in [j for j in [j-1, j, j+1] if j >= 0 and j <= len(z)-1]:
        if x == j and y == i:
            continue
        else:
            print(z[y][x])
            print(y, x)
print(z)
