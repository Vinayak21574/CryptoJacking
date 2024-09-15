import os
import pandas as pd
import re
import datetime
from tqdm import tqdm
import pytz

def log_dir_analysis():
    out_path = f'./total_res.log'
    out = open(out_path, "w")
    input_dir = "./logs/zcash"
    for file_name in tqdm(os.listdir(input_dir)):
        input_path = f'{input_dir}/{file_name}'
        fp = open(input_path, "r")
        line = fp.readline()
        while line:
            # print(line)
            line = fp.readline()
            if 'ProcessNewBlock' in line and 'new' in line:
                # print(line)
                out.write(line)
    fp.close()
    out.flush()
    out.close()

log_dir_analysis()


def utc_to_unix(date_str):
    utc_datetime=datetime.datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
    
    timeArray = int(utc_datetime.replace(tzinfo=datetime.timezone.utc).timestamp())
    
    utc_datetime = utc_datetime.astimezone(datetime.timezone.utc).replace(tzinfo=None,microsecond=0)
    
    return timeArray, utc_datetime



def block_analysis():
    input_path = f'./total_res.log'
    out_path = f'./block_create_time_zcash.csv'
    
    timestamp_list = []
    height_list = []
    time_str_list = []
    
    with open(input_path,"r") as f:
        line=f.readline()
        while(line):
            temp=line.split()
            # print(temp)
            
            height=int(temp[8].split("=")[-1])
            unix,utc=utc_to_unix(temp[0])
            
            timestamp_list.append(unix)
            height_list.append(height)
            time_str_list.append(utc)
            line=f.readline()
   
    res_df = pd.DataFrame(data={'timestamp': timestamp_list, 'height': height_list, 'utc_time': time_str_list})
    res_df.sort_values(by='height', ascending=True, inplace=True)
    res_df.reset_index(drop=True, inplace=True)
    res_df.to_csv(out_path, index=False, header=False)
        

block_analysis()

