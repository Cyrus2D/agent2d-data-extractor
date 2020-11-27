import pandas as pd

file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/base_data_4.csv'
# file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/test.csv'
save_file_path = '/media/nader/8cf88936-ff21-4a0a-a07a-1dbec4247478/robo_data/base_data_pass_4.csv'
model = 'model.h5'
df = pd.read_csv(file_path, dtype=float)
just_test = False
new_date = df[df['out_category'] == 2]
del df
try:
    del new_date['Unnamed: 0']
except:
    pass
# print(new_date.columns)
new_date.to_csv(save_file_path)