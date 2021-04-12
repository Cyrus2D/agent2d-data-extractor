import os
import pandas as pd
import psutil


def merger_all_to_unum_small(read_path, save_path, i):
    dfs = []
    for f in os.listdir(read_path):
        if f.find(f'_{i}__') == -1:
            continue
        dfs.append(pd.read_csv(os.path.join(read_path, f)))
    print('end read')
    dfs = pd.concat(dfs, axis=0, join='inner')
    dfs = dfs[dfs['out_category'] == 2]
    if dfs.columns[-1] != 'out_desc':
        del dfs[dfs.columns[-1]]
    dfs = dfs.reset_index()
    del dfs['index']
    try:
        del dfs['Unnamed: 0']
    except:
        pass
    print(dfs.count())
    dfs.dropna(inplace=True)
    dfs.to_csv(save_path)
    print(dfs.count())


def merger_all_to_unum_big(read_path, save_path, i, x):
    dfs = []
    xx = 0
    file_read = False
    for f in os.listdir(read_path):
        if f.find(f'_{i}__') == -1:
            continue
        xx += 1
        if xx < x * 1000:
            continue
        if xx >= (x + 1) * 1000:
            break
        file_read = True
        dfs.append(pd.read_csv(os.path.join(read_path, f)))
    if not file_read:
        return
    print('end read')
    dfs = pd.concat(dfs, axis=0, join='inner')
    dfs = dfs[dfs['out_category'] == 2]
    if dfs.columns[-1] != 'out_desc':
        del dfs[dfs.columns[-1]]
    dfs = dfs.reset_index()
    del dfs['index']
    try:
        del dfs['Unnamed: 0']
    except:
        pass
    print(dfs.count())
    dfs.dropna(inplace=True)
    dfs.to_csv(save_path)
    print(dfs.count())


def merger_from_to(read_path, save_path, f):
    org_df = pd.read_csv(read_path)
    print('org', org_df.count()[0])
    for t in range(1, 12):
        df = org_df[org_df[f'out_unum'] == t]
        print('df', t, df.count()[0])
        if df.columns[-1] != 'out_desc':
            del df[df.columns[-1]]
        df.dropna(inplace=True)
        df = df.reset_index()
        del df['index']
        try:
            del df['Unnamed: 0']
        except:
            pass
        df.to_csv(save_path + f'to_{t}_from_{f}.csv')
        print('merged', f, t)


def merger(read_path, save_path):
    dfs = None
    for f in os.listdir(read_path):
        print('read' + f)
        df = pd.read_csv(os.path.join(read_path, f))#.iloc[:20000]
        # df = df[df[f'out_unum'] == i]
        df = df[df['out_category'] == 2]
        if dfs is None:
            dfs = df
        else:
            dfs = dfs.append([df])
        del df
        # if psutil.Process(os.getpid()).memory_info().rss / 1024 ** 2 > 15000:
        #     break
    # for df in dfs:
    if dfs.columns[-1] != 'out_desc':
        del dfs[dfs.columns[-1]]
    dfs.dropna(inplace=True)
    dfs = dfs.reset_index()
    del dfs['index']
    try:
        del dfs['Unnamed: 0']
    except:
        pass
    dfs.to_csv(save_path)

def merger_multiprocess():

merger('/home/nader/data/robo_data/other_team/', '/home/nader/data/robo_data/other.csv')
# read_path =      '/home/nader/data/robo_data/all_data/'
# save_file_path = f'/home/nader/data/robo_data/from_i/from_{i}.csv'
# merger_all_to_unum_small(read_path, save_file_path, i)

# for i in range(1, 9):
#     read_path =      '/home/nader/data/robo_data/all_data/'
#     save_file_path = f'/home/nader/data/robo_data/from_i/from_{i}.csv'
#     merger_all_to_unum_small(read_path, save_file_path, i)

# for i in range(1, 12):
#     read_path =      '/home/nader/data/robo_data/all_data/'
#     for x in range(0, 7):
#         save_file_path = f'/home/nader/data/robo_data/from_i/from_{i}_{x}.csv'
#         merger_all_to_unum_big(read_path, save_file_path, i, x)

# for i in range(5):
#     merger(read_path + str(i), save_file_path + 'all_' + str(i) + '.csv')

# for f in range(1, 12):
#     merger_from_to(f'/home/nader/data/robo_data/from_i/from_{f}_0.csv', f'/home/nader/data/robo_data/to_i/', f)
