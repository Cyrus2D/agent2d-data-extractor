import os
import pandas as pd

read_path =      '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/data/'
save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/merged_data.csv'

header = ''

read_rows = []
file_counter = 0
files = os.listdir(read_path)

os.chdir(read_path)
dfs = [pd.read_csv(f) for f in os.listdir(os.getcwd()) if f.endswith('csv')]
for df in dfs:
    del df[df.columns[-1]]
print('end read')
df = pd.concat(dfs, axis=0, join='inner')
df = df.reset_index()
del df['index']
df.to_csv(save_file_path)
