from stream import PcapReader
from blocks import BlockSeries
from similarity import Flow,SimScore

from collections import defaultdict
from typing import List
from copy import deepcopy as cpy
from tqdm import tqdm

TYPE="monero"
# TYPE="etc"


blocks=BlockSeries(f'block_create_time_{TYPE}.csv')
# captures=PcapReader("..\\data_capture\\traffic\\capture-2024-06-27_17-49-07.pcap")
captures=PcapReader("..\\GatewayTraffic\\capture-2024-07-30_00-05-14.pcap")


START_TIME=captures.start_time
INTERVAL=25*60

LEN_THRESHHOLD=66

curr_block=-1
flow=defaultdict(Flow)
max_blocks=len(blocks.arr)

def interval_process(start,end):
    global flow
    for f in flow.keys():
        flow[f].evaluate(start,end)
        

import pandas as pd

with open(f"RESULTS_{TYPE}.csv","w") as f:
    pass

def result():
    arr=[]
    
    for f in flow.keys():
        arr.append((flow[f].global_score,str(f)))
    arr.sort(reverse=True)
    
    temp={
        'score':[i[0] for i in arr],
        'srcIP':[i[1].split("_")[0] for i in arr],
        'dstIP':[i[1].split("_")[1] for i in arr],
        # 'block_count':[res[i[1]].block_count for i in arr],
        'max_local':[flow[i[1]].max_local for i in arr],
        'min_local':[flow[i[1]].min_local for i in arr],
    }
    
    df=pd.DataFrame(temp)
    
    with open(f"RESULTS_{TYPE}.csv", 'a') as f:
        df.to_csv(f, header=True, index=True)  

    

for pkt in tqdm(captures.stream_reader()):    
    if(curr_block==-1):
        for i in range(len(blocks.arr)):
            curr_block=i+1
            if(blocks.arr[i]>pkt.timestamp):
                curr_block=i-1
                break
            elif(blocks.arr[i]==pkt.timestamp):
                curr_block=i
                break
            
    if(curr_block==max_blocks):
        break
    
    if(pkt.length<LEN_THRESHHOLD):
        continue

    
    if(pkt.timestamp>=START_TIME+INTERVAL):
        result()
        flow.clear()
        flow=defaultdict(Flow)
        START_TIME+=INTERVAL  
        print("Detection Scope Ended") 
        
        
    
    if(pkt.timestamp>=blocks.arr[curr_block+1]):
        # print("Next Interval")
        interval_process(blocks.arr[curr_block],blocks.arr[curr_block+1])
        curr_block+=1
        
    flow[pkt.id].arr.append(pkt.timestamp)
    
    
# flow={}
interval_process(blocks.arr[curr_block],blocks.arr[curr_block+1])
result()

print("Compiling Results...")


