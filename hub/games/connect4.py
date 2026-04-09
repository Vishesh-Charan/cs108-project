import pygame as pg
import numpy as np
import sys
from general import general

"""
NOTE- its very much similar logic as of tic tac toe
i already wrote detailed comments of tic tac toe explanation
here i am just redoing similar things. Hence not much comments 
and explanations written here.

"""

pg.init() 
#initializing pygame

width,hieght=700,700
screen=pg.display.set_mode((width,hieght))
pg.display.set_caption("Connect 4")
bg_color=(28, 40, 51)
screen.fill(bg_color)
side=100
row,colomn=7,7
player1=sys.argv[1]
player2=sys.argv[2]


class Connect4(general):
    def __init__(self):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn)) 
    def draw_lines(self):
        
        color,border_size,side=(52, 73, 94),5,100
        #horizental
        for i in range(1, row):
            pg.draw.line(screen,color, (0, i * side), (width, i * side), border_size)
        # vertical
        for i in range(1, colomn):
            pg.draw.line(screen,color, (i * side, 0), (i * side, hieght), border_size)
            
    def draw_figures(self):

        circle_color1,circle_color2=(241, 196, 15),(1,1,1) 
        radius,side=40,100

        for rows in range(row):
            for col in range(colomn):
                if self.board[rows][col] == 1:
                    pg.draw.circle(screen,circle_color1, (int(col * side + side//2), int(rows * side + side//2)), radius)

                elif self.board[rows][col] == 2:
                    pg.draw.circle(screen,circle_color2, (int(col * side + side//2), int(rows * side + side//2)), radius)

                
    def mark_square(self,row, col, player):
        #to update that the box is now marked
        self.board[row][col] = player

    def max_available_square(self, col):
        #to check status if the the box is empty or filled
        for row in range (6,0,-1):
            if(self.board[row][col] == 0):
                return row
            
        return -1     

    def is_board_full(self):
        return not np.any(self.board == 0)
        #checks if board is full

    def check_win(self,player):

        set_of_subgrids=np.lib.stride_tricks.sliding_window_view(self.board, (4, 4))
        anti_subgrids=np.flip(set_of_subgrids,axis=3)
        row_check=np.any(np.all(set_of_subgrids == player, axis=3))
        col_check=np.any(np.all(set_of_subgrids == player, axis=2))

        diag_check=np.any(np.all(np.diagonal(set_of_subgrids==player, axis1=2,axis2=3),axis=2))
        antidiag_check=np.any(np.all(np.diagonal(anti_subgrids==player,axis1=2,axis2=3),axis=2))
        if(row_check or col_check or diag_check or antidiag_check):
            return True
        return False
  
    
    def run(self):

        #initializing
        self.draw_lines()
        player = 1
        game_over = False


        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    #this part is handling the termination of the loop

                if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    #storing the co ordinates of the pixel where the mouse got clicked
                    clicked_row = int(mouseY // side)
                    clicked_col = int(mouseX // side)
                   

                    if (self.max_available_square(clicked_col)>=0):
                        self.mark_square(self.max_available_square(clicked_col), clicked_col, player)
                        if self.check_win(player):
                            game_over = True
                            print(f"Player {player} wins!")
                            winner=self.currentturnplayer()
                            return winner
                        elif self.is_board_full():
                            game_over = True
                            print("It's a draw!")
                            return None
                        #switch()
                        #player=player%2+1
                        self.changeturn()
                        player=self.current_turn
                        self.draw_figures()
                        #this whole part handles the main gameplay using our functions, etc

            pg.display.update() 

game=Connect4()
game.run()
