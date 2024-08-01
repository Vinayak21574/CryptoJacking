import numpy as np
from typing import List

class SimScore:
    def __init__(self,flow,timelen,start_time):
        flow=[int(i-start_time) for i in flow]
        self.delta=flow[0]
        self.dx=1
        self.X=np.arange(0,flow[-1]+1,1)
        
        self.num_pcks=len(flow)
        self.time=int(timelen)
        
        self.Y=np.array([self.func(i) for i in self.X])
        self.Y /= (self.dx * self.Y).sum()
        
        self.cdf=1-np.cumsum(self.Y * self.dx)
        
    def func(self,n):
        return ((self.time-(n))/self.time)**self.num_pcks-((self.time-(n+1))/self.time)**self.num_pcks
        # try:
        #     temp= ((self.time-(n))/self.time)**self.num_pcks-((self.time-(n+1))/self.time)**self.num_pcks
        #     return temp
        # except OverflowError:
        #     print(self.time,n,self.num_pcks)
        #     raise
    
    def score(self):
        return max(self.cdf[self.delta]*(1-(self.delta/self.time)),0)
    

class Flow:
    def __init__(self):
        self.arr:List[int]=[]
        self.score=0
        self.global_score=0
        self.block_count=0
        self.max_local=None
        self.min_local=None
        
    def evaluate(self,start,end):
        if(len(self.arr)==0):
            temp=0
        else:
            temp=SimScore(self.arr,end-start,start)
            temp=temp.score()
            
        self.score+=temp
        
        self.arr:List[int]=[]
        
        if(self.max_local):
            self.max_local=max(self.max_local,temp)
        else:
            self.max_local=temp
        
        if(temp!=-1):
            if(self.min_local):
                self.min_local=min(self.min_local,temp)
            else:
                self.min_local=temp

        self.block_count+=1
        self.global_score=self.score/self.block_count
        return 
    


