import os


read_path =      '/home/aref/Documents/data/'
save_file_path = '/home/aref/Documents/data/merged_data.csv'

header = ''

read_rows = []
file_counter = 0
files = os.listdir(read_path)
for file in files:
    file_counter += 1
    print(file_counter / len(files) * 100)
    open_file = open(read_path + file, 'r')
    lines = open_file.readlines()
    if header == '':
        header = lines[0].rstrip('\n')
    for line in lines[1:]:
        read_rows.append(line.rstrip('\n'))
    open_file.close()

if not os.path.exists(save_file_path):
    header = [header]
    read_rows = header + read_rows

out_file = open(save_file_path, 'a')
out_file.write('\n'.join(read_rows))
out_file.close()
