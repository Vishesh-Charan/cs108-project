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

width,hieght=800,800
screen=pg.display.set_mode((width,hieght))
pg.display.set_caption("Othello(Reversi)")
bg_color=(28, 40, 51)
screen.fill(bg_color)
side=100
row,colomn=8,8
player1=sys.argv[1]
player2=sys.argv[2]


class Othello_Reversi(general):
    def __init__(self):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn)) 
        self.board[3,3],self.board[4,4]=1,1
        self.board[3,4],self.board[4,3]=2,2

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


    def valid_move_and_update(self,row,col,player):
        #to check status if the the box is empty or filled
        #if the box is valid, this function also updates the flippings,etc
        if(self.board[row][col] != 0):
            return False
        
       
        directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1),(1, -1),  (1, 0),  (1, 1)]
        #i will check if there exists a same color coin in any these 8 direction vectors
        #if in a direction, we got the same color coin, just flip all the ones in path
        
        pieces_to_flip = []
        isvalid=False
        for dr, dc in directions:
            temp_flip_list = []
            r,c=row+dr,col+dc
            # Walk in the current direction
            while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == (player%2)+1:
                temp_flip_list.append((r, c))
                r += dr
                c += dc
            
            if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player and len(temp_flip_list)>0:
                #we r doing piece fliping only if we got the same color and 
                #rejecting the possibility that r,c got out of board without getting the same color coin
                #or there was no other color between two same color
                #this is handled by the if's conditions
                pieces_to_flip.extend(temp_flip_list)
                isvalid=True

        # Execute the flips
        for r, c in pieces_to_flip:
            self.board[r][c] = player
            
        # Also set the starting piece itself
        if(isvalid):
            self.board[row][col] = player
        
        return isvalid
            

    def valid_move_doesnt_exist(self,player):
        notvalid=True
        for row in range(8):
            for col in range(8):
                if(self.board[row][col] == 0):
                
                    directions = [(-1, -1), (-1, 0), (-1, 1),(0, -1), (0, 1),(1, -1),  (1, 0),  (1, 1)]

                    for dr, dc in directions:
                        r,c=row+dr,col+dc
                        
                        while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == (player%2)+1:
                            r += dr
                            c += dc
                            
                        if 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
                            notvalid=False
        return notvalid

    def check_win(self):

        #i created the board into a boolean array and summed which gives no. of player's coins
        player1=(self.board==1).sum() 
        player2=(self.board==2).sum()
        if(player1>player2):
            return 1
        elif(player2>player1):
            return 2
        return 0
        

  
    
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


                otherguy=(player%2)+1
                if(self.valid_move_doesnt_exist(player) and self.valid_move_doesnt_exist(otherguy)):
                    game_over=True
                    winner_number=self.check_win()

                    if(winner_number==0):
                        print("It's a draw!")
                        return None
                    
                    print(f"Player {winner_number} wins!")
                    self.current_turn=winner_number
                    winner=self.currentturnplayer()
                    return winner
                    #here, to use currentturnplayer function to set the winner, i first changed the currentturn to winner_number
                

                if(self.valid_move_doesnt_exist(player)):
                    self.changeturn()
                    player=self.current_turn

                if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    #storing the co ordinates of the pixel where the mouse got clicked
                    clicked_row = int(mouseY // side)
                    clicked_col = int(mouseX // side)
  
                    if(self.valid_move_and_update(clicked_row,clicked_col,player)):
                        #switch()
                        #player=player%2+1
                        self.changeturn()
                        player=self.current_turn
                        #this whole part handles the main gameplay using our functions, etc
                self.draw_figures()
            pg.display.update() 

game=Othello_Reversi()
game.run()
