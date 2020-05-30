import math
import random
import platform
import time
import os
import numpy as np
import scipy
import scipy.signal


HUMAN= -1
COMP= 1
MAP={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8,"j":9,"k":10,"l":11,"m":12,"n":13,"o":14
,"p":15,"q":16,"r":17,"s":18,"t":19,"u":20,"v":21,"w":22,"x":23,"y":24,"z":25}
REVERSEMAP={0:"a",1:"b",2:"c",3:"d",4:"e",5:"f",6:"g",7:"h",8:"i",9:"j",10:"k",11:"l",12:"m",13:"n",14:"o"
,15:"p",16:"q",17:"r",18:"s",19:"t",20:"u",21:"v",22:"w",23:"x",24:"y",25:"z"}

class Gomoku:
    def __init__(self,size,depth):
        self.size=size
        self.board=np.zeros((size,size))
        self.depth=depth
    def wins(self,state,player):
        win_states=[]
        for i in range(self.size):
            for j in range(self.size):
                if(j+4<self.size):
                    win_states.append([state[i,j],state[i,j+1],state[i,j+2],state[i,j+3],state[i,j+4]])
                if(i+4<self.size):
                    win_states.append([state[i,j],state[i+1,j],state[i+2,j],state[i+3,j],state[i+4,j]])
                if(i+4<self.size and j+4<self.size):
                    win_states.append([state[i,j],state[i+1,j+1],state[i+2,j+2],state[i+3,j+3],state[i+4,j+4]])
                if(i-4>=0 and j+4<self.size):
                    win_states.append([state[i,j],state[i-1,j+1],state[i-2,j+2],state[i-3,j+3],state[i-4,j+4]])
        if([player]*5 in win_states):
            return True
        else:
            return False
    def threat_detect(self,state):

    def empty_cell(self,state):
        cells=[]
        for i in range(self.size):
            for j in range(self.size):
                if(state[i,j]==0):
                    cells.append([i,j])
        return cells
    def valid_move(self,x,y):
        if(self.board[x,y]!=0):
            return False
        else:
            return True
    def set_move(self,x,y,player):
        if(self.valid_move(x,y)):
            board[x][y]=player
            return True
        else:
            return False
    def game_over(self,state):
        return self.wins(state,HUMAN) or self.wins(state,COMP)
    def minmax(self,state,depth,player,alpha,beta):
        if(player==COMP):
            best=[-1,-1,-math.inf]
        else:
            best=[-1,-1,math.inf]
        if(depth==0 or self.game_over(state)):
            score=evaluate(state)
            return [-1,-1,score]
        for cell in self.empty_cells(state):
            x,y=cell[0],cell[1]
            state[x][y]=player
            score=minmax(state,depth-1,-player,alpha,beta)
            state[x][y]=0
            if(player==COMP):
                if(score[2]>best[2]):
                    best[2]=score[2]
                    best[0],best[1]=x,y
                if(score[2]>alpha):
                    alpha=score[2]
                if(score[2]>=beta):
                    return [x,y,score[2]]
            else:
                if(score[2]<best[2]):
                    best[2]=score[2]
                    best[0],best[1]=x,y
                if(score[2]<beta):
                    beta=score[2]
                if(score[2]<=alpha):
                    return [x,y,score[2]]
    def evaluate(self,state,player):
        score=0
        openSide=0
        step=1
        horizonViewed=[]
        verticalViewed=[]
        for i in range(self.size):
            for j in range(self.size):
                if(self.board[i,j]==player):
                    pattern=[player]
                    while(self.valid_move(i,j-step) and self.board[i,j-step]==player):
                        step-=1
                        pattern=[player]+pattern
                    if(self.valid_move(i,j-step) and self.board[i,j-step]==0):
                        pattern=[0]+pattern
                    else:
                        pattern=[-2]+pattern
                    step=1
                    while(self.valid_move(i,j+step) and self.board[i,j+step]==player):
                        step+=1
                        pattern+=pattern+[player]
                    if(self.valid_move(i,j+step) and self.board[i,j+step]==0):
                        pattern=pattern+[0]
                    else:
                        pattern=[-2]+pattern
                    
    # def evaluateImproved(self,state,player):
    #     score=0
    #     horizonPattern=np.ones((1,5))
    #     horizonCov=scipy.signal.convolve(state,horizonPattern,mode='valid')
    #     if(len(horizonCov[np.where(horizonCov==5)])>=1):
    #         return 2000000
    #     coordx,coordy=np.where(horizonCov==4)
    #     consecutive=4
    #     viewedNode=[]
    #     for i in range(len(coordx)):
    #         openSide=0
    #         if(self.valid_move([coordx[i],coordy[i]-1]) and self.board[coordx[i],coordy[i]-1]==0):
    #             openSide+=1
    #         if(self.valid_move([coordx[i],coordy[i]+5]) and self.board[coordx[i],coordy[i]+5]==0):
    #             openSide+=1
    #         if(openSide==2):
    #             return 200000
    #         viewedNode.append((coordx[i],coordy[i]+1))
    #         viewedNode.append((coordx[i],coordy[i]+2))
    #         viewedNode.append((coordx[i],coordy[i]+3))
    #         viewedNode.append((coordx[i],coordy[i]+4))
            
    #     verticalCov=scipy.signal.convolve(state,)





if __name__=="__main__":
