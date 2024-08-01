import os
import pandas as pd
import re
import datetime
from tqdm import tqdm
import pytz

def log_dir_analysis():
    out_path = f'../bitmonero/total_res.log'
    out = open(out_path, "w")
    input_dir = "../bitmonero/logs_etc"
    for file_name in tqdm(os.listdir(input_dir)):
        input_path = f'{input_dir}/{file_name}'
        fp = open(input_path, "r")
        line = fp.readline()
        while line:
            # print(line)
            line = fp.readline()
            if 'Imported new chain segment' in line and 'ignored' not in line:
                # print(line)
                out.write(line)
    fp.close()
    out.flush()
    out.close()

log_dir_analysis()



def ist_to_unix(date_str):
    # Define the format of the input date string
    date_format = "[%m-%d|%H:%M:%S.%f]"
    
    # Parse the input date string to a naive datetime object
    naive_datetime = datetime.datetime.strptime(date_str, date_format)
    
    # Assuming the year is the current year
    current_year = datetime.datetime.now().year
    naive_datetime = naive_datetime.replace(year=current_year)
    
    # Define the IST timezone
    ist = pytz.timezone('Asia/Kolkata')
    
    # Localize the naive datetime object to IST
    ist_datetime = ist.localize(naive_datetime)
    
    # Convert the IST datetime to Unix time
    unix_time = int(ist_datetime.timestamp())
    utc_time=ist_datetime.astimezone(pytz.utc)
    
    return unix_time,utc_time


def block_analysis():
    input_path = f'../bitmonero/total_res.log'
    out_path = f'../bitmonero/block_create_time_etc.csv'

    data_df = pd.read_csv(input_path, sep='\t', on_bad_lines='skip')
    
    timestamp_list = []
    height_list = []
    time_str_list = []
    
    with open(f'../bitmonero/total_res.log',"r") as f:
        line=f.readline()
        while(line):
            temp=line.split()
            height=int(temp[6].split("=")[-1].replace(",",""))
            unix,utc=ist_to_unix(temp[1])
            
            timestamp_list.append(unix)
            height_list.append(height)
            time_str_list.append(utc)
            line=f.readline()
            
    res_df = pd.DataFrame(data={'timestamp': timestamp_list, 'height': height_list, 'utc_time': time_str_list})
    res_df.sort_values(by='height', ascending=True, inplace=True)
    res_df.reset_index(drop=True, inplace=True)
    res_df.to_csv(out_path, index=False, header=False)
        
    
    
block_analysis()
