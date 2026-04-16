import pygame as pg
import numpy as np
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from game import general

"""
NOTE- its very much similar logic as of tic tac toe
i already wrote detailed comments of tic tac toe explanation
here i am just redoing similar things. Hence not much comments 
and explanations written here.

"""

pg.init() 
#initializing pygame
clock=pg.time.Clock()
width,hieght=700,700
screen=pg.display.set_mode((width,hieght))
pg.display.set_caption("Connect 4")
bg_color=(28, 40, 51)
screen.fill(bg_color)
offsetx=94
offsety=100
sidex=72
sidey=66
row,colomn=7,7
BG_Image= pg.image.load('Connect 4 board.png')    
BG_Image=pg.transform.scale(BG_Image, (700,700))
red=pg.image.load('Red ball.png')
yellow=pg.image.load('Yellow ball.png')
green=pg.image.load('green sphere.png')
red=pg.transform.scale(red,(sidex,sidey))
yellow=pg.transform.scale(yellow,(sidex,sidey+4))
green=pg.transform.scale(green,(sidex,sidey))
font= pg.font.Font("PressStart2P-Regular.ttf",24)
class Connect4(general):
    def __init__(self,player1,player2):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn)) 
    def draw_lines(self):
        screen.blit(BG_Image,(0,0))
        Text= str(self.currentturnplayer()) +" Moves"
        Turn_surface=font.render(Text,True,(255,255,255))
        screen.blit(Turn_surface,(180,30))

        
            
    def draw_figures(self):
        for rows in range(row):
            for col in range(colomn):
                if self.board[rows][col] == 1:
                    screen.blit(red,(int(offsetx+col * sidex+3), int(offsety+rows*sidey+5)))
                elif self.board[rows][col] == 2:
                    screen.blit(yellow,(int(offsetx+col * sidex+3), int(offsety+rows*sidey+5)))

    def ball_animation(self,row,col,player):
        #making the ball falling animation
        speed=10
        i=offsety
        while i<int(offsety+row*sidey+5):
            i=min(i+speed,int(offsety+row*sidey+5))
            self.draw_lines()
            self.draw_figures()
            if player == 1:
                    screen.blit(red,(int(offsetx+col * sidex+3), i))
            elif player == 2:
                    screen.blit(yellow,(int(offsetx+col * sidex+3), i))
            pg.display.update()
            clock.tick(60)
        

    def mark_square(self,row, col, player):
        #to update that the box is now marked
        self.board[row][col] = player

    def max_available_square(self, col):
        #to check status if the the box is empty or filled
        for row in range (6,-1,-1):
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
        if(row_check):
            indices=np.argwhere(np.all(set_of_subgrids == player, axis=3))
            coords=[[indices[0][1],indices[0][0]+indices[0][2]],[indices[0][1]+1,indices[0][0]+indices[0][2]],[indices[0][1]+2,indices[0][0]+indices[0][2]],[indices[0][1]+3,indices[0][0]+indices[0][2]]]
            return [True,coords,1]
        col_check=np.any(np.all(set_of_subgrids == player, axis=2))
        if(col_check):
            indices=np.argwhere(np.all(set_of_subgrids == player, axis=2))
            coords=[[indices[0][1]+indices[0][2],indices[0][0]],[indices[0][1]+indices[0][2],indices[0][0]+1],[indices[0][1]+indices[0][2],indices[0][0]+2],[indices[0][1]+indices[0][2],indices[0][0]+3]]
            return [True,coords,2]

        diag_check=np.any(np.all(np.diagonal(set_of_subgrids==player, axis1=2,axis2=3),axis=2))
        if(diag_check):
            indices=np.argwhere(np.all(np.diagonal(set_of_subgrids==player, axis1=2,axis2=3),axis=2))
            coords=[[indices[0][0],indices[0][1]],[indices[0][0]+1,indices[0][1]+1],[indices[0][0]+2,indices[0][1]+2],[indices[0][0]+3,indices[0][1]+3]]
            return [True,coords,3]
        antidiag_check=np.any(np.all(np.diagonal(anti_subgrids==player,axis1=2,axis2=3),axis=2))
        if(antidiag_check):
            indices=np.argwhere(np.all(np.diagonal(anti_subgrids==player, axis1=2,axis2=3),axis=2))
            coords=[[indices[0][0],indices[0][1]+3],[indices[0][0]+1,indices[0][1]+2],[indices[0][0]+2,indices[0][1]+1],[indices[0][0]+3,indices[0][1]]]
            return [True,coords,4]
        return [False,None]
  
    
    def run(self):

        #initializing
        self.draw_lines()
        player = 1
        game_over = False


        while True:
            self.draw_lines()
            self.draw_figures()
            #Adding hover
            mouse_position=pg.mouse.get_pos()
            hovered_col = int((mouse_position[0]-offsetx) // sidex)
            if hovered_col>=0 and hovered_col<7:
                hover_surface = pg.Surface((sidex, row * sidey), pg.SRCALPHA)
                hover_surface.fill((200, 200, 200, 80))
                screen.blit(hover_surface,(offsetx + hovered_col * sidex+5, offsety+4))
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    #this part is handling the termination of the loop
                if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    #storing the co ordinates of the pixel where the mouse got clicked
                    clicked_row = int((mouseY-offsety) // sidey)
                    clicked_col = int((mouseX-offsetx) // sidex)
                   
                    #events after the move is made(mouse click)
                    if (self.max_available_square(clicked_col)>=0):
                        self.ball_animation(self.max_available_square(clicked_col),clicked_col,player)
                        self.mark_square(self.max_available_square(clicked_col), clicked_col, player)
                        self.draw_figures()
                        pg.display.update()
                        pg.time.delay(100)
                        stat=self.check_win(player)
                        if stat[0]:
                            game_over = True
                            winnermade=True
                            print(f"Player {player} wins!")
                            winner=self.currentturnplayer()
                            break
                        elif self.is_board_full():
                            game_over = True
                            winnermade=False
                            print("It's a draw!")
                            return None
                        #switch()
                        #player=player%2+1
                        self.changeturn()
                        player=self.current_turn
                        #this whole part handles the main gameplay using our functions, etc
            if game_over and winnermade:
                if stat[2]==3 or stat[2]==4:
                    for points in stat[1]:
                        screen.blit(green,(int(offsetx+points[1]*sidex+3), int(offsety+points[0]*sidey+5)))
                        pg.display.update()
                        pg.time.delay(100)
                    pg.time.delay(500)
                    return winner
                else:
                    for points in stat[1]:
                        screen.blit(green,(int(offsetx+points[0]*sidex+3), int(offsety+points[1]*sidey+5)))
                        pg.display.update()
                        pg.time.delay(100)
                    pg.time.delay(500)
                    return winner
            pg.display.update() 


