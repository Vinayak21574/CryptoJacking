from typing import List
import pandas as pd

class BlockSeries:
    arr:List[int]=[]
    
    def __init__(self,path,THESHHOLD_INTERVAL=10):
        df=pd.read_csv(path, names=["Epoch","Height","Time"])
        # print(df.head())
        
        temp=df['Epoch'].to_list()
        prev=-1
        for curr in temp:
            if(curr-prev)>=THESHHOLD_INTERVAL:
                self.arr.append(curr)
            prev=curr

        # print(self.blocks)
        
# temp=BlockSeries("bitmonero\\block_create_time_total.csv")