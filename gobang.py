import math
import random
import platform
import time
import os
import numpy as np
import scipy
import scipy.signal
import sys

HUMAN= -1
COMP= 1
MAP={"a":1,"b":2,"c":3,"d":4,"e":5,"f":6,"g":7,"h":8,"i":9,"j":10,"k":11,"l":12,"m":13,"n":14,"o":15
,"p":16,"q":17,"r":18,"s":19,"t":20,"u":21,"v":22,"w":23,"x":24,"y":25,"z":26}
REVERSEMAP={1:"a",2:"b",3:"c",4:"d",5:"e",6:"f",7:"g",8:"h",9:"i",10:"j",11:"k",12:"l",13:"m",14:"n",15:"o"
,16:"p",17:"q",18:"r",19:"s",20:"t",21:"u",22:"v",23:"w",24:"x",25:"y",26:"z"}

class Gomoku:
    def __init__(self,size,depth):
        self.size=size
        self.board=np.zeros((size,size))
        self.depth=depth
        self.evaluation={"0111110":10000000,"x11111x":10000000,"011111x":10000000,"x111110":10000000,
        "011110":1000000,"01111x":300000,"x11110":300000,"x1111x":1,"0110110":300000,"011011x":300000,"x110110":300000,"x11011x":300000,"0101110":300000,"010111x":300000,"x101110":300000,"x10111x":300000,"0111010":300000,"011101x":300000,"x111010":300000,"x11101x":300000
        ,"01110":100000,"0111x":10000,"x1110":10000,"x111x":1,"011010":100000,"01101x":10000,"x11010":10000,"x1101x":1,"010110":100000,"01011x":10000,"x10110":10000,"x1011x":1,
        "0110":5000,'011x':1000,'x110':1000,"x11x":1,"01010":2000,"0101x":1000,"x1010":1000,"x101x":1,
        "010":500,"01x":50,"x10":50,"x1x":1}
        self.threatStates=set(["0-1-1-1-10","0-1-1-1-1x","x-1-1-1-10","0-1-1-10"])
        self.specialThreaten=set(["0-1-10-1-10","x-1-10-1-10","0-1-10-1-1x","x-1-10-1-1x","0-10-1-1-10","x-10-1-1-10","x-10-1-1-1x","0-10-1-1-1x","0-1-1-10-10"
        ,"x-1-1-10-10","0-1-1-10-1x","x-1-1-10-1x","0-1-10-10","0-10-1-10"])
        self.ownMovesX=[]
        self.ownMovesY=[]
        self.opponentMovesX=[]
        self.opponentMovesY=[]
        self.ownMean=None
        self.opponentMean=None

    def threat_detect(self):
        horizonViewed=set([])
        verticalViewed=set([])
        leftDiagonalViewed=set([])
        rightDiagonalViewed=set([])
        x,y=None,None
        for i in range(self.size):
            for j in range(self.size):
                if(self.board[i,j]==HUMAN):
                    #horizontal
                    if((i,j)not in horizonViewed):
                        pattern,viewed=self.evaluate_direction(self.board,(i,j),0,1,HUMAN)
                        print("horizontal ",pattern," position",i,j)
                        if(pattern in self.threatStates):
                            x,y=i,j-1
                            if(pattern[0]=="0"):
                                return (x,y)
                            elif(len(pattern)%2==0):
                                consecutive=int((len(pattern)-2)/2)
                                return (x,y+consecutive+1)
                            # else:
                            #     x,y=i,j+1
                            #     while(self.board[x,y]!=0):
                            #         y+=1
                            #     return (x,y)
                        elif(pattern in self.specialThreaten):
                            x,y=i,j+1
                            while(self.board[x,y]!=0):
                                y+=1
                            return (x,y)
                        horizonViewed.update(viewed)
                    #vertical
                    if((i,j)not in verticalViewed):
                        pattern,viewed=self.evaluate_direction(self.board,(i,j),1,0,HUMAN)
                        print("vertical",pattern)
                        if(pattern in self.threatStates):
                            x,y=i-1,j
                            if(pattern[0]=="0"):
                                return (x,y)
                            elif(len(pattern)%2==0):
                                consecutive=int((len(pattern)-2)/2)
                                return (x+consecutive+1,y)
                        elif(pattern in self.specialThreaten):
                            x,y=i+1,j
                            while(self.board[x,y]!=0):
                                x+=1
                            return (x,y)
                        verticalViewed.update(viewed)
                    #rightDiagonal
                    if((i,j)not in rightDiagonalViewed):
                        pattern,viewed=self.evaluate_direction(self.board,(i,j),1,1,HUMAN)
                        print("rightdiagonal",pattern)
                        if(pattern in self.threatStates):
                            x,y=i-1,j-1
                            if(pattern[0]=="0"):
                                return (x,y)
                            elif(len(pattern)%2==0):
                                consecutive=int((len(pattern)-2)/2)
                                return (x+consecutive+1,y+consecutive+1)
                        elif(pattern in self.specialThreaten):
                            x,y=i+1,j+1
                            while(self.board[x,y]!=0):
                                x,y=x+1,y+1
                            return (x,y)
                        rightDiagonalViewed.update(viewed)
                    #leftDiagonal
                    if((i,j)not in leftDiagonalViewed):
                        print("leftDiagonal",pattern)
                        pattern,viewed=self.evaluate_direction(self.board,(i,j),1,-1,HUMAN)
                        if(pattern in self.threatStates):
                            x,y=i-1,j+1
                            if(pattern[0]=="0"):
                                return (x,y)
                            elif(len(pattern)%2==0):
                                consecutive=int((len(pattern)-2)/2)
                                return (x+consecutive+1,y-consecutive-1)
                        elif(pattern in self.specialThreaten):
                            x,y=i+1,j-1
                            while(self.board[x,y]!=0):
                                x,y=x+1,y-1
                            return(x,y)
                        leftDiagonalViewed.update(viewed)
        return (None,None)

    def empty_cell(self,state):
        cells=[]
        for i in range(self.size):
            for j in range(self.size):
                if(state[i,j]==0):
                    cells.append([i,j])
        return cells
    def allowed_move(self,x,y):
        if(x<0 or y<0 or x>=self.size or y>=self.size):
            return False
        return True
    def valid_move(self,state,x,y):
        if(x<0 or y<0 or x>=self.size or y>=self.size):
            return False
        if(state[x,y]!=0):
            return False
        else:
            return True

    def set_move(self,x,y,player):
        if(self.valid_move(self.board,x,y)):
            self.board[x][y]=player
            return True
        else:
            return False

    def searching_space(self,state):
        cells=[]
        for i in range(self.size):
            for j in range(self.size):
                if(state[i,j]==0):
                    cells.append([[i,j],math.sqrt((i-self.ownMean[0])**2+(j-self.ownMean[1])**2)])
        cells.sort(key=lambda x:x[1])
        return cells

    def minmax(self,state,depth,player,alpha,beta):
        if(player==COMP):
            best=[-1,-1,-math.inf]
        else:
            best=[-1,-1,math.inf]
        if(depth==0 or len(state==0)==0):
            currScore=self.evaluate(state)
            return [-1,-1,currScore]
        for cell in self.searching_space(state):
            x,y=cell[0][0],cell[0][1]
            state[x][y]=player
            score=self.minmax(state,depth-1,-player,alpha,beta)
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
        return best

    def evaluate_direction(self,state,point,row,col,player):
        gap=0
        viewed=set([])
        i,j=point
        viewed.add((i,j))
        step=1
        pattern=str(player)
        gap=0
        if(self.allowed_move(i-row,j-col) and state[i-row,j-col]==0):
            pattern="0"+pattern
        else:
            pattern="x"+pattern
        i,j=i+row,j+col
        while(self.allowed_move(i,j) and state[i,j]!=-player and step<=5 and gap<2):
            if(state[i,j]==0 and gap>=1 ):
                break
            elif(state[i,j]==player and gap<=1):
                viewed.add((i,j))
                pattern=pattern+str(player)
            elif (state[i,j]==0 and gap==0):
                gap+=1
                pattern=pattern+str(0)
            i=i+row
            j=j+col
            step+=1
        if(pattern[-1]!="0"):
            if(self.allowed_move(i,j) and state[i,j]==0):
                pattern=pattern+"0"
            else:
                pattern=pattern+"x"
        return (pattern,viewed)
        
    def evaluate(self,state):
        score=0
        horizonViewed=set([])
        verticalViewed=set([])
        leftDiagonalViewed=set([])
        rightDiagonalViewed=set([])

        for i in range(self.size):
            for j in range(self.size):
                if(state[i,j]==COMP):
                    #horizontal
                    if((i,j)not in horizonViewed):
                        pattern,viewed=self.evaluate_direction(state,(i,j),0,1,COMP)
                        score+=self.get_score(pattern)
                        horizonViewed.update(viewed)
                    #vertical
                    if((i,j)not in verticalViewed):
                        pattern,viewed=self.evaluate_direction(state,(i,j),1,0,COMP)
                        score+=self.get_score(pattern)
                        verticalViewed.update(viewed)
                    #rightDiagonal
                    if((i,j)not in rightDiagonalViewed):
                        pattern,viewed=self.evaluate_direction(state,(i,j),1,1,COMP)
                        score+=self.get_score(pattern)
                        rightDiagonalViewed.update(viewed)
                    #leftDiagonal
                    if((i,j)not in leftDiagonalViewed):
                        pattern,viewed=self.evaluate_direction(state,(i,j),1,-1,COMP)
                        score+=self.get_score(pattern)
                        leftDiagonalViewed.update(viewed)
        return score

    def get_score(self,pattern):
        return self.evaluation.get(pattern,1)

    def ai_turn(self):
        cellsLeft=self.empty_cell(self.board)
        if(len(cellsLeft)==0):
            return
        if(len(cellsLeft)==self.size*self.size):
            x=self.size//2
            y=self.size//2
        else:
            x,y=self.threat_detect()
            if(x==None):
                self.ownMean=(np.mean(np.array(self.ownMovesX)),np.mean(np.array(self.ownMovesY)))
                self.opponentMean=(np.mean(np.array(self.opponentMovesX)),np.mean(np.array(self.opponentMovesY)))
                move=self.minmax(self.board.copy(),self.depth,COMP,-math.inf,math.inf)
                x,y=move[0],move[1]
        x=int(x)
        y=int(y)
        self.set_move(x,y,COMP)
        self.ownMovesX.append(x)
        self.ownMovesY.append(y)
        x,y=x+1,REVERSEMAP.get(y+1)
        print("Move played: "+y+str(x))
    def human_turn(self):
        cellsLeft=self.empty_cell(self.board)
        if(len(cellsLeft)==0):
            return
        move=input()
        print("Move played: "+move)
        col,row=MAP.get(move[0])-1,int(move[1:])-1
        if(self.set_move(row,col,HUMAN)):
            self.opponentMovesX.append(row)
            self.opponentMovesY.append(col)
            return
        else:
            print("invalid position, please enter a new position");
            move=input()
            print("Move played: "+move)
            col,row=MAP.get(move[0])-1,int(move[1:])-1
            if(not self.set_move(row,col,HUMAN)):
                exit()
            self.opponentMovesX.append(row)
            self.opponentMovesY.append(col)
            return
def main():
    if(len(sys.argv)<=2):
        print("need more argument")
        exit()
    else:
        boardSize=int(sys.argv[2])
        print(boardSize)
        gomoku=Gomoku(boardSize,2)
        if(len(sys.argv)==4):
            compFirst=True
        else:
            compFirst=False
    while(True):
        if(compFirst):
            gomoku.ai_turn()
            compFirst=False
        gomoku.human_turn()
        gomoku.ai_turn()

if __name__=="__main__":
    main()