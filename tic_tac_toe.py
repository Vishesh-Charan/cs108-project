import pygame as pg
import numpy as np
import sys
from general import general


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
side=60 
# the side of each box = 600 pixels/10
row,colomn=10,10
player1=sys.argv[1]
player2=sys.argv[2]


class tic_tac_toe(general):
    def __init__(self):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn)) 
        #did same mistake the "tuple one"...
        #initialized the board
    def draw_lines(self):
        #making the arena lines :)
        #lets initialize the variables first 
        color,border_size,side=(52, 73, 94),5,60
        #its line's color,width and side lenth of square
        # horizontal
        for i in range(1, row):
            pg.draw.line(screen,color, (0, i * side), (width, i * side), border_size)
        # vertical
        for i in range(1, colomn):
            pg.draw.line(screen,color, (i * side, 0), (i * side, hieght), border_size)
            
    def draw_figures(self):
        #first lets define circle and cross color then its radius, dimensions , etc....

        circle_color,cross_color=(241, 196, 15),(231, 76, 60) #Gold,Corral Red 
        circle_width,cross_width,=8,10
        radius,side=20,60
        for rows in range(row):
            for col in range(colomn):
                if self.board[rows][col] == 1:
                    #there is a inbuilt function to draw circle-
                    pg.draw.circle(screen,circle_color, (int(col * side + side//2), int(rows * side + side//2)), radius, circle_width)
                elif self.board[rows][col] == 2:
                    #cross using two diagonals
                    pg.draw.line(screen, cross_color, (col * side + side//4, rows *side + (3*side)//4), (col * side + (3*side)//4, rows * side + side//4), cross_width)
                    pg.draw.line(screen, cross_color, (col * side + side//4, rows * side + side//4), (col * side + (3*side)//4, rows * side + (3*side)//4), cross_width)

    def mark_square(self,row, col, player):
        #to update that the box is now marked
        self.board[row][col] = player

    def available_square(self,row, col):
        #to check status if the the box is empty or filled
        return self.board[row][col] == 0      

    def is_board_full(self):
        return not np.any(self.board == 0)
        #checks if board is full

    def check_win(self,player):
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
    NOTE- python recognizes only True and False, not true false, etc
    the k denotes the kth diagonal above or below the main diagonal
    fliplr make antidiagonal as main diagonal
    I set the variables range by properly calculating thier thier spans
    np.all is true if all conditions inside are true, np.any is true if atleast one condition is true
    the diagonal win check part was so much interesting and fun to code :)
    """
    def restart(self):
        screen.fill(bg_color)
        self.draw_lines()
        self.board[:][:]=0
        #the restart function
    def run(self):

        #initializing
        self.draw_lines()
        player = 1
        game_over = False

        """
        NOTE- there is so much inbuilt functions,etc i am using related to event handling
        pg.event.get() give me a list/queue of events and i run a for loop on it handling one by one the events
        """

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
                    #found the corresponding row and colomn in 10*10 board

                    if self.available_square(clicked_row, clicked_col):
                        self.mark_square(clicked_row, clicked_col, player)
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

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_r:
                        #if user pressed 'r' on keyboard, we will restart 
                        self.restart()
                        player = 1
                        game_over = False

            pg.display.update() 
            #as all happens in internal/memory/RAM whatever, we are updating it on display using this inbuilt function of pygame
            #tic tac toe finished finally ;)

#i did this mistake - tic_tac_toe.run()
#also remember to add self in inputs of functions and call functions as self.function
game=tic_tac_toe()
game.run()
