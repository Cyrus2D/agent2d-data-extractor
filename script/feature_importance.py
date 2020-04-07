import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sklearn.ensemble as xx
import seaborn as sns

other = ['cycle', 'ofside_count']

data = pd.read_csv("/home/aref/Documents/data/aref.csv")
# data = data.iloc[:50, :]
X = data.iloc[:, :-9]  # independent columns

for i in [-9, -6, -5, -2]:
    print(f'{i}...')
    y = data.iloc[:, i]  # target column i.e price range

    model = xx.RandomForestClassifier()
    model.fit(X, y)

    importance = pd.Series(model.feature_importances_, index=X.columns)
    importance.to_csv(f"/home/aref/Documents/data/features_importance/random_forest|{data.keys()[i]}.csv")

# y = data.iloc[:, -2]  # target column i.e price range
#
# model = xx.RandomForestClassifier()
# model.fit(X, y)
#
# data = pd.Series(model.feature_importances_, index=X.columns)
# # importance = {}
#
# data.to_csv("/home/aref/Documents/data/features_importance")
#
# for key in other:
#     importance[key] = float(data[key])
#
# for j in range(2):
#     for i in range(1, 12):
#         start_key = f"p_" \
#                     f"{'l' if j == 0 else 'r'}_" \
#                     f"{i}_"
#         keys = [key for key in data.keys() if key.strip(' ').startswith(start_key)]
#         if keys == []:
#             continue
#
#         for key in keys:
#             if importance.get('p' + key[len(start_key):]) is None:
#                 importance['p' + key[len(start_key):]] = 0
#             else:
#                 importance['p' + key[len(start_key):]] += float(data[key])
#
# start_key = 'ball'
# ball_keys = [key for key in data.keys() if key.strip(' ').startswith(start_key)]
# for key in ball_keys:
#     importance[key] = float(data[key])
#
# other_keys = [key for key in data.keys() if key.strip(' ').startswith('drible_angle')]
# for key in other_keys:
#     if importance.get(key) is None:
#         importance[key[:len(other_keys)]] = float(data[key])
#     else:
#         importance[key[:len(other_keys)]] += float(data[key])
#
# key = []
# value = []
# for k, v in importance.items():
#     key.append(k)
#     value.append(v)

# fig1, ax1 = plt.subplots()
# ax1.pie(value, labels=key, autopct='%1.1f%%',
#         shadow=True, startangle=90)
# plt.show()
#
# importance = pd.Series(value, index=key)
# importance.nlargest(100).plot(kind='barh')
# plt.show()
