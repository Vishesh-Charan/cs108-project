import pygame as pg
import numpy as np
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)
from game import general
pg.init() 
#initializing pygame

width,hieght=600,600
#screen=pg.display.set_mode(width,hieght), i did this mistake
#note-it takes only one input which is tuple, not two different number inputs
screen=pg.display.set_mode((width,hieght))
#I made a variable "screen" which refers to our display of width*hieght
pg.display.set_caption("Tic Tac Toe")
#wrote caption
#now lets set a background color 
bg_color=(28, 40, 51) #Dark Slate
screen.fill(bg_color)
sidex=48
sidey=46
# the side of each box = 600 pixels/10
row,colomn=10,10
font= pg.font.Font("PressStart2P-Regular.ttf",24)
class tic_tac_toe(general):
    def __init__(self,player1,player2):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn)) 
        #did same mistake the "tuple one"...
        #initialized the board
    def draw_lines(self):
        #Drawing the background board
        BG_Image= pg.image.load('TTT Board.png')    
        BG_Image=pg.transform.scale(BG_Image, (600,600))
        screen.blit(BG_Image,(0,0))
        Text= str(self.currentturnplayer()) +" Moves"
        Turn_surface=font.render(Text,True,(255,255,255))
        screen.blit(Turn_surface,(100,20))


    def draw_figures(self):
        #first lets define circle and cross color then its radius, dimensions , etc....
        x=pg.image.load('X.png')
        o=pg.image.load('O.png')
        x=pg.transform.scale(x,(sidex-10,sidey-10))
        o=pg.transform.scale(o,(sidex-10,sidey-10))
        for rows in range(row):
            for col in range(colomn):
                if self.board[rows][col] == 1:
                    #Insert O-
                    screen.blit(o,(int(61+col * sidex + 5), int(76+rows * sidey + 5)))
                elif self.board[rows][col] == 2:
                    #cross 
                    screen.blit(x,(int(61+col * sidex + 5), int(76+rows * sidey + 5)))

    def mark_square(self,row, col, player):
        #to update that the box is now marked
        self.board[row][col] = player

    def available_square(self,row, col):
        #to check status if the the box is empty or filled
        if row<10 and row>=0 and col>=0 and col<10:
            return self.board[row][col] == 0      

    def is_board_full(self):
        return not np.any(self.board == 0)
        #checks if board is full

    def check_win(self,player):

        set_of_subgrids=np.lib.stride_tricks.sliding_window_view(self.board, (5, 5))
        #it is a inbuilt function which gives a 4D array, its 10*10 grid whose each cell is 5*5 corresponding subsquare
        #set_of_subgrids is the variable representing all the possible 5*5 subsquares of the board
        anti_subgrids=np.flip(set_of_subgrids,axis=3)
        row_check=np.any(np.all(set_of_subgrids == player, axis=3))
        if(row_check):
            indices=np.argwhere(np.all(set_of_subgrids == player, axis=3))
            return [True,indices[0],1]
        col_check=np.any(np.all(set_of_subgrids == player, axis=2))
        if(col_check):
            indices=np.argwhere(np.all(set_of_subgrids == player, axis=2))
            return [True,indices[0],2]
        #axis represents the dimension we r considering in our 4D array
        #in this I am returning a list True or False ndicate win or not. The indices array indicate the position variables needed to mark the line, like 
        #the coordinates of the start of 5x5 subgrids and the row and col nos. in that subgrid by which I can make the lines later and also a no. from 1 to 4 indicating what kind
        #of win it is, row,column,diagonal or  anti-diagonal
         
        diag_check=np.any(np.all(np.diagonal(set_of_subgrids==player, axis1=2,axis2=3),axis=2))
        if(diag_check):
            indices=np.argwhere(np.all(np.diagonal(set_of_subgrids==player, axis1=2,axis2=3),axis=2))
            return [True,indices[0],3]
        antidiag_check=np.any(np.all(np.diagonal(anti_subgrids==player,axis1=2,axis2=3),axis=2))
        if(antidiag_check):
            indices=np.argwhere(np.all(np.diagonal(anti_subgrids==player, axis1=2,axis2=3),axis=2))
            return [True,indices[0],4]
        return [False,None,None]
        """
        #to check if the player wins
        #lined stack represents the number of X or O that should come in line to win
        lined_stack=5
        # Vertical win check
        for col in range(colomn):
            for rows in range(row-lined_stack):
                if np.all(self.board[rows:rows+lined_stack, col] == player):
                    return True
        # Horizontal win check
        for rows in range(row):
            for col in range(colomn - lined_stack):
                if np.all(self.board[rows, col:col+lined_stack] == player):
                    return True
        # Diagonal win checks
        for k in range(-lined_stack,1+lined_stack):
            for r in range(row-(lined_stack+abs(k)-1)):
                if np.all(np.diag(self.board,k)[r:r+lined_stack] == player) or np.all(np.diag(np.fliplr(self.board),k)[r:r+lined_stack] == player):
                    return True
        return False
        """
    """
    NOTE- python recognizes only True and False, not true false, etc
    the k denotes the kth diagonal above or below the main diagonal
    fliplr make antidiagonal as main diagonal
    I set the variables range by properly calculating thier thier spans
    np.all is true if all conditions inside are true, np.any is true if atleast one condition is true
    the diagonal win check part was so much interesting and fun to code :)
    """
    def run(self):
        #background music
        pg.mixer.init()
        pg.mixer.music.load('8-Bit-Indigestion.mp3')
        pg.mixer.music.play(-1)
        #initializing
        self.draw_lines()
        player = 1
        game_over = False

        """
        NOTE- there is so much inbuilt functions,etc i am using related to event handling
        pg.event.get() give me a list/queue of events and i run a for loop on it handling one by one the events
        """

        while True:
            self.draw_lines()
            self.draw_figures()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    #this part is handling the termination of the loop

                if event.type == pg.MOUSEBUTTONDOWN and not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    #storing the co ordinates of the pixel where the mouse got clicked
                    clicked_row = int((mouseY-76) // sidey)
                    clicked_col = int((mouseX-61) // sidex)
                    #found the corresponding row and colomn in 10*10 board

                    if self.available_square(clicked_row, clicked_col):
                        self.mark_square(clicked_row, clicked_col, player)
                        self.draw_figures()
                        pg.display.update()
                        pg.time.delay(500)
                        stat=self.check_win(player)
                        #Mark the tiles with a line to indicate Victory 
                        if stat[0]:
                            if stat[2]==1:
                                pg.draw.line(screen,(128,128,128),(61+stat[1][1]*sidex+sidex//2,76+(stat[1][0]+stat[1][2])*sidey+sidey//2),(61+(stat[1][1]+4)*sidex+sidex//2,76+(stat[1][0]+stat[1][2])*sidey+sidey//2),width=3)
                            elif stat[2]==2:
                                pg.draw.line(screen,(128,128,128),(61+(stat[1][1]+stat[1][2])*sidex+sidex//2,76+stat[1][0]*sidey+sidey//2),(61+(stat[1][1]+stat[1][2])*sidex+sidex//2,76+(stat[1][0]+4)*sidey+sidey//2),width=3)
                            elif stat[2]==3:
                                pg.draw.line(screen,(128,128,128),(61+stat[1][0]*sidex+sidex//2,76+stat[1][1]*sidey+sidey//2),(61+(stat[1][0]+4)*sidex+sidex//2,76+(stat[1][1]+4)*sidey+sidey//2),width=3)
                            elif stat[2]==4:
                                pg.draw.line(screen,(128,128,128),(61+stat[1][0]*sidex+sidex//2,76+(stat[1][1]+4)*sidey+sidey//2),(61+(stat[1][0]+4)*sidex+sidex//2,76+stat[1][1]*sidey+sidey//2),width=3)
                            game_over = True
                            print(f"Player {player} wins!")
                            winner=self.currentturnplayer()
                            pg.display.update()
                            pg.time.delay(1500)
                            return winner
                        elif self.is_board_full():
                            game_over = True
                            print("It's a draw!")
                            return None
                        #switch()
                        #player=player%2+1
                        self.changeturn()
                        player=self.current_turn
                        #this whole part handles the main gameplay using our functions, etc
            pg.display.update() 
            #as all happens in internal/memory/RAM whatever, we are updating it on display using this inbuilt function of pygame
            #tic tac toe finished finally ;)

#i did this mistake - tic_tac_toe.run()
#also remember to add self in inputs of functions and call functions as self.function
