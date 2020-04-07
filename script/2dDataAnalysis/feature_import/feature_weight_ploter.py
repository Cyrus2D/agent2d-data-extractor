from matplotlib import pyplot as plt
import numpy as np
f = open('extra_trees_out_category.csv', 'r').readlines()[1:]
f = open('random_forest_out_category.csv', 'r').readlines()[1:]
# f = open('extra_trees_out_unum.csv', 'r').readlines()[1:]
# f = open('nn_out_desc.csv').readlines()
dic = {}

for row in f:
    r = row.split(',')
    dic[r[0]] = float(r[1])

selected_features = {}
for d in dic.keys():
    if d.find('p_l') >= 0 and d.find('player_type') < 0:
        new_name = d[d.find('p_l') + 4:]
        new_name = new_name[new_name.find('_') + 1:]
        print(new_name)
        if not new_name in ['passangle', 'dpassdist', 'nearoppdist', 'openGAngle_openGAngle', 'stamina', 'in_ofside']:
            continue
        if new_name in selected_features.keys():
            selected_features[new_name] += dic[d]
        else:
            selected_features[new_name] = dic[d]

name = selected_features.keys()
data = list(selected_features.values())
data = np.array(data)
data *= 100
data /= sum(data)


fig, ax = plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))


def func(pct, allvals):
    absolute = int(pct/100.*np.sum(allvals))
    return "{:.1f}%".format(pct, absolute)


wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data), textprops=dict(color="w"))
ax.legend(wedges, name,
          title="Ingredients",
          loc="center left",
          bbox_to_anchor=(1, 0, 0.5, 1))
plt.setp(autotexts, size=8, weight="bold")

plt.show()