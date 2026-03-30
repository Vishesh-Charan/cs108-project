import numpy as np
import sys, os, time, pygame, pathlib, matplotlib
from datetime import datetime
from Games.connect4 import Connect4
from Games.othello import Othello
from Games.tictactoe import TicTacToe
player1=sys.argv[1]
player2=sys.argv[2]

pygame.init()
class BaseSetup:
    def __init__(self, player1, player2):
        self.players=[player1,player2]
        self.current_turn = 0
        self.board= None
    def changeturn(self):
        self.current_turn=1-self.current_turn
    def currentturnplayer(self):
        return self.players[self.current_turn]
    def check_win(self):
        raise NotImplementedError 
