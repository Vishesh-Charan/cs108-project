import numpy as np
import sys, os, time, pygame, pathlib
from datetime import datetime

pygame.init()
class general:
    def __init__(self, player1, player2):
        self.players=["None",player1,player2]
        self.current_turn = 1
        self.area= None
    def changeturn(self):
        self.current_turn=self.current_turn%2 + 1
    def currentturnplayer(self):
        return self.players[self.current_turn]
    def check_win(self):
        raise NotImplementedError 