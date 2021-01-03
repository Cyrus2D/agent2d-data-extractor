import numpy as np
import pandas as pd
import sys
import matplotlib.pyplot as plt
np.set_printoptions(threshold=sys.maxsize)

unum = 9
df = pd.read_csv(f'/home/nader/data/fwm_fwm_unum/from_i/from_{unum}_200000.csv')
max_x = max([max(df[f'p_r_{u}_pos_x']) for u in range(1, 12)])
max_x = max(max_x, max([max(df[f'p_l_{u}_pos_x']) for u in range(1, 12)]))
max_y = max([max(df[f'p_r_{u}_pos_y']) for u in range(1, 12)])
max_y = max(max_y, max([max(df[f'p_l_{u}_pos_y']) for u in range(1, 12)]))
image_size = (51, 51)
image_count = df.count()[0]
images = np.zeros((image_count, image_size[0], image_size[1], 3))
label = np.zeros(image_count)

for i in range(image_count):
    d = df.loc[i]
    images[i][int(d['ball_pos_x'] * image_size[0])][int(d['ball_pos_y'] * image_size[1])][0] = 1
    for u in range(1, 12):
        images[i][int(d[f'p_l_{u}_pos_x'] / max_x * (image_size[0] - 1))][int(d[f'p_l_{u}_pos_y'] / max_y* (image_size[1] - 1))][1] = u / 12.0
    for u in range(1, 12):
        images[i][int(d[f'p_r_{u}_pos_x'] / max_x * (image_size[0] - 1))][int(d[f'p_r_{u}_pos_y'] /max_y* (image_size[1] - 1))][2] = 1
    label[i] = d['out_unum']

np.save(f'/home/nader/data/fwm_fwm_unum/from_i_image/from_{unum}_img.npy', images)
print(images.shape)
np.save(f'/home/nader/data/fwm_fwm_unum/from_i_image/from_{unum}_label.npy', label)

x = np.load(f'/home/nader/data/fwm_fwm_unum/from_i_image/from_{unum}_img.npy')
print(x.shape)