from matplotlib import pyplot as plt
import numpy as np
import re
# f = open('extra_trees_out_category.csv', 'r').readlines()[1:]
# f = open('random_forest_out_category.csv', 'r').readlines()[1:]
# f = open('extra_trees_out_unum.csv', 'r').readlines()[1:]
files = [
        'f_f_pass_unum_history_full_l4_randomf_10.csv',
         'f_f_pass_unum_history_full_l4_randomf_20.csv',
         'f_f_pass_unum_history_full_l4_randomf_30.csv',
         'f_f_pass_unum_history_full_l4.csv',
         'f_f_pass_unum_history_full_l4_2.csv'
         ]
files_sum = []
lines = []
weights = []
selected_features = [
{'code': 'p_l_[1-5]', 'sum': []},
{'code': 'p_l_([6-9]|1[0-1])', 'sum': []},
{'code': 'p_r_[1-5]', 'sum': []},
{'code': 'p_r_([6-9]|1[0-1])', 'sum': []},
]
selected_features = [
{'code': 'p.*pos_x', 'sum': []},
{'code': 'p.*pos_y', 'sum': []},
{'code': 'p.*kicker_x', 'sum': []},
{'code': 'p.*kicker_y', 'sum': []},
]
for i in range(len(files)):
    files_sum.append(0)
    l = open(files[i]).readlines()
    min_w = 0
    sum_w = 0
    weights.append({})
    for row in l:
        r = row.split(',')
        weights[-1][r[0]] = float(r[1]) if float(r[1]) > 0 else 0
        sum_w += weights[-1][r[0]]
        if float(r[1]) < min_w:
            min_w = float(r[1])
        # for d in dic.keys():
        #     weights[-1][r[0]] += (-min_w)
    files_sum[-1] = sum_w
    for f in selected_features:
        f['sum'].append(0)
        f['fields'] = []
        for d in weights[i].keys():
            if re.search(f['code'], d):
                f['fields'].append(d)
                f['sum'][i] += weights[i][d]
for f in selected_features:
    f['fields'].sort()
    print(f)

fig, ax = plt.subplots(len(files), 2, figsize=(10, 3*len(files)), subplot_kw=dict(aspect="equal"))
for i in range(len(files)):
    names = [f['code'] for f in selected_features]
    data = [f['sum'][i] for f in selected_features]
    data_percent = np.array(data)
    data_percent *= 100
    if sum(data_percent) == 0:
        data_percent = 0
    else:
        data_percent /= sum(data_percent)
    def func(pct, allvals):
        absolute = int(pct/100.*np.sum(allvals))
        return "{:.1f}%".format(pct, absolute)


    print(sum(data))
    print(files_sum[i])
    print([sum(data) / files_sum[i] * 100.0, (files_sum[i] - sum(data)) / files_sum[i] * 100.0])
    # try:
    ax[i][0].pie([sum(data) / files_sum[i] * 100.0, (files_sum[i] - sum(data)) / files_sum[i] * 100.0], colors=['red', 'black'])
    wedges, texts, autotexts = ax[i][1].pie(data_percent, autopct=lambda pct: func(pct, data_percent), textprops=dict(color="w"))
    ax[i][1].legend(wedges, names,
              title=files[i],
              loc="center left",
              bbox_to_anchor=(1, 0, 0.5, 1))
    # except:
    #     pass
    # plt.setp(autotexts, size=8, weight="bold")
plt.show()