import pygame
import numpy as np
import sys #for standard input/output/exit,etc tasks like standard library of cpp

class general :
    ROWS=0
    COLS=0
    def __init__ (self,row,col,p1,p2,t):
        self.ROWS=row
        self.COLS=col
        self.board = np.zeros((self.ROWS,self.COLS))
        self.Player1=p1
        self.Player2=p2
        self.turn=t

    def switch(self) :
        self.turn=(self.turn%2)+1  

