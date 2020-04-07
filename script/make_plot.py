data = {'simple': {
            'left': [64.56, 27.34, 7.09, 0.51, 0.51, 0, 0, 0, 0, 0, 0],
            'right': [9.62, 22.53, 32.66, 20.76, 10.38, 3.54, 0.25, 0.25, 0, 0, 0],
            'diff': [0, 0, 0, 0.25, 0.0, 3.29, 6.84, 14.94, 30.89, 23.29, 13.42, 6.33, 0.76, 0, 0, 0, 0, 0, 0, 0, 0],
            'win': [7.09, 8.19],
            'goal': [0.45, 2.13]},
        'full': {
            'left': [6.03, 13.79, 26.15, 26.15, 17.82, 6.32, 2.3, 0.57, 0.86, 0, 0],
            'right': [27.59, 37.36, 26.15, 6.32, 2.59, 0, 0, 0, 0, 0, 0],
            'diff': [0, 0, 0, 0, 0, 0, 0, 0.86, 2.87, 8.33, 15.23, 21.84, 21.55, 17.82, 7.47, 3.16, 0.29, 0.57, 0, 0, 0],
            'win': [72.7, 85.76],
            'goal': [2.72, 1.19]},
        'chain': {
            'left': [20.63, 35.53, 24.36, 12.61, 4.3, 2.29, 0.29, 0, 0, 0, 0],
            'right': [10.89, 28.08, 26.07, 18.91, 10.32, 5.73, 0, 0, 0, 0, 0],
            'diff': [0, 0, 0, 0, 0.29, 0.86, 4.3, 8.02, 18.05, 17.48, 26.36, 13.18, 6.3, 2.01, 2.87, 0.29, 0, 0, 0, 0, 0],
            'win': [24.64, 33.46],
            'goal': [1.59, 2.09]}
        }

from matplotlib import pyplot as plt

f, axs = plt.subplots(1, 3, figsize=(10, 3))

axs[0].plot(range(0, 11), data['simple']['left'], range(0, 11), data['chain']['left'], range(0, 11), data['full']['left'])
axs[0].set_ylim(0, 70)
axs[0].set_ylabel('Percent')
axs[0].set_xlabel('Left Team Goal Distribution')
axs[1].plot(range(-10, 11), data['simple']['diff'], range(-10, 11), data['chain']['diff'], range(-10, 11), data['full']['diff'])
axs[1].set_ylim(0, 40)
axs[1].set_xlabel('Diff Goal Distribution')
axs[2].plot(range(0, 11), data['simple']['right'], range(0, 11), data['chain']['right'], range(0, 11), data['full']['right'])
axs[2].set_ylim(0, 40)
axs[2].legend(['Normal', 'ChainActionFullState', 'FullState'])
axs[2].set_xlabel('Right Team Goal Distribution')
plt.show()

import math
a = [0.0199, 0.0198, 0.0211, 0.0194, 0.0204, 0.0197, 0.0227, 0.0196, 0.0187, 0.0211]
for d in a:
    x = d * 105
    y = d * 64
    diff = math.sqrt(x * x + y * y)
    print(diff)

a = [143, 181, 145, 183, 185,203,142,149,204,143]
for r in a:
    d = r / 10000
    ang = d * 360
    # print(ang)
    dist = d * 3
    print(dist)