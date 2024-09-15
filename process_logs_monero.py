import os
import pandas as pd
import re
import datetime
from tqdm import tqdm

def log_dir_analysis():
    out_path = f'./total_res.log'
    out = open(out_path, "w")
    input_dir = "./logs/monero"
    for file_name in tqdm(os.listdir(input_dir)):
        input_path = f'{input_dir}/{file_name}'
        fp = open(input_path, "r")
        line = fp.readline()
        while line:
            # print(line)
            line = fp.readline()
            if 'NOTIFY_NEW_FLUFFY_BLOCK' in line:
                # print(line)
                out.write(line)
    fp.close()
    out.flush()
    out.close()

log_dir_analysis()

def time2timestamp(dt):
    timeArray = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S").replace(tzinfo=datetime.timezone.utc).timestamp()
    return int(timeArray)

def block_analysis():
    input_path = f'./total_res.log'
    out_path = f'./block_create_time_monero.csv'
    columns_name = ['time', 'node', 'log_type', 'msg_type', 'code_locate'
        , 'transfer_msg']
    data_df = pd.read_csv(input_path, sep='\t', on_bad_lines='skip', names=columns_name)
    
    timestamp_list = []
    height_list = []
    time_str_list = []
    
    for msg_name, msg_db in data_df.groupby(by=['transfer_msg']):
        msg_name=msg_name[0]
        m = re.search('\(.*,', msg_name)
        height = m.group(0)
        height = int(height.split(' ')[1][0:-1])
        time_str = msg_db.reset_index(drop=True).loc[0, 'time']
        timestamp = time2timestamp(time_str.split('.')[0])
        if height not in height_list:
            timestamp_list.append(timestamp)
            height_list.append(height)
            time_str_list.append(time_str.split('.')[0])
    res_df = pd.DataFrame(data={'timestamp': timestamp_list, 'height': height_list, 'utc_time': time_str_list})
    res_df.sort_values(by='height', ascending=True, inplace=True)
    res_df.reset_index(drop=True, inplace=True)
    res_df.to_csv(out_path, index=False, header=False)


block_analysis()




