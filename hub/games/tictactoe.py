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

width,hieght=700,700
Board_x=150
Board_y=0
#screen=pg.display.set_mode(width,hieght), i did this mistake
#note-it takes only one input which is tuple, not two different number inputs
#I made a variable "screen" which refers to our display of width*hieght
pg.display.set_caption("Tic Tac Toe")
#wrote caption
#now lets set a background color 
sidex=55
sidey=54
row,colomn=10,10
font= pg.font.Font("Fonts and Audio/PressStart2P-Regular.ttf",24)
class tic_tac_toe(general):
    def __init__(self,player1,player2,screen):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn)) 
        self.screen=screen
        #did same mistake the "tuple one"...
        #initialized the board
    def draw_lines(self):
        #Drawing the background board
        BG_Image= pg.image.load('Images/TTT Board.png')    
        BG_Image=pg.transform.scale(BG_Image, (700,700))
        self.screen.blit(BG_Image,(Board_x,Board_y))
        Text= str(self.currentturnplayer()) +" Moves"
        Turn_surface=font.render(Text,True,(255,255,255))
        self.screen.blit(Turn_surface,(100+Board_x,20+Board_y))


    def draw_figures(self):
        #first lets define circle and cross color then its radius, dimensions , etc....
        x=pg.image.load('Images/X.png')
        o=pg.image.load('Images/O.png')
        x=pg.transform.scale(x,(sidex-10,sidey-10))
        o=pg.transform.scale(o,(sidex-10,sidey-10))
        for rows in range(row):
            for col in range(colomn):
                if self.board[rows][col] == 1:
                    #Insert O-
                    self.screen.blit(o,(int(72+Board_x+col * sidex + 10), int(89+Board_y+rows * sidey + 5)))
                elif self.board[rows][col] == 2:
                    #cross 
                    self.screen.blit(x,(int(72+Board_x+col * sidex + 10), int(89+Board_y+rows * sidey + 5)))
    
    def moveback(self,screen):
        font = pg.font.Font("Fonts and Audio/PressStart2P-Regular.ttf", 19)
        small_font = pg.font.Font("Fonts and Audio/PressStart2P-Regular.ttf", 16)
        BG_COLOR = (30, 30, 60)
        NORMAL_COLOR = (200, 200, 200)
        HOVER_COLOR = (255, 255, 255)
        OVERLAY_COLOR = (0, 0, 0, 150)

        # Box dimensions
        box_w, box_h = 500, 300
        box_x = (1000 - box_w) // 2  
        box_y = (700 - box_h) // 2   

        line1 = "Go back to the main menu?"
        # Buttons positioned relative to box
        continue_button = pg.Rect(box_x + 50, box_y + 180, 170, 50)
        quit_button = pg.Rect(box_x + 280, box_y + 180, 170, 50)

        clock = pg.time.Clock()

        while True:
            mouse_pos = pg.mouse.get_pos()
            hoveredc = continue_button.collidepoint(mouse_pos)
            hoveredq = quit_button.collidepoint(mouse_pos)
            if hoveredc:
                c_color=HOVER_COLOR
            else:
                c_color=NORMAL_COLOR
            if hoveredq:
                q_color=HOVER_COLOR
            else:
                q_color=NORMAL_COLOR

            # Draw overlay over the existing screen
            overlay = pg.Surface((1000, 700), pg.SRCALPHA)
            overlay.fill(OVERLAY_COLOR)
            screen.blit(overlay, (0, 0))

            # Draw the popup box
            pg.draw.rect(screen, BG_COLOR, (box_x, box_y, box_w, box_h), border_radius=12)
            pg.draw.rect(screen, NORMAL_COLOR, (box_x, box_y, box_w, box_h), 3, border_radius=12)

            # Draw text inside box
            text1 = font.render(line1, True, (255, 255, 255))
            screen.blit(text1, text1.get_rect(center=(box_x + box_w // 2, box_y + 80)))

            # Draw buttons
            pg.draw.rect(screen, c_color, continue_button, 3, border_radius=8)
            pg.draw.rect(screen, q_color, quit_button, 3, border_radius=8)

            cont_text = small_font.render("Continue", True, (255, 255, 255))
            quit_text = small_font.render("Quit", True, (255, 255, 255))
            screen.blit(cont_text, cont_text.get_rect(center=continue_button.center))
            screen.blit(quit_text, quit_text.get_rect(center=quit_button.center))

            pg.display.flip()
            clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    return 0
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if continue_button.collidepoint(event.pos):
                        screen.fill(BG_COLOR)
                        pg.display.update()
                        return 1
                    elif quit_button.collidepoint(event.pos):
                        return 0
                

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
        pg.mixer.music.load('Fonts and Audio/8-Bit-Indigestion.mp3')
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
            back_text="Back to menu"
            back_button = pg.Rect(570, 10, 300, 50)
            mouse_pos = pg.mouse.get_pos()
            hoveredb= back_button.collidepoint(mouse_pos)
            if hoveredb:
                pg.draw.rect(self.screen, (255, 0, 0), back_button,3)  
                Back_surface=font.render(back_text,True,(255,0,0))
                back_rect = Back_surface.get_rect(center=back_button.center)
                self.screen.blit(Back_surface, back_rect)
            else:
                pg.draw.rect(self.screen, (255, 255, 255), back_button,3)  
                Back_surface=font.render(back_text,True,(255,255,255))
                back_rect = Back_surface.get_rect(center=back_button.center)
                self.screen.blit(Back_surface, back_rect)
            self.draw_figures()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()
                    sys.exit()
                    #this part is handling the termination of the loop
                elif event.type == pg.MOUSEBUTTONDOWN and back_button.collidepoint(event.pos):
                    pg.mixer.music.stop()
                    if(self.moveback(self.screen)):
                        self.draw_lines()
                        self.draw_figures()
                        pg.mixer.init()
                        pg.mixer.music.load('Fonts and Audio/8-Bit-Indigestion.mp3')
                        pg.mixer.music.play(-1)
                    else:
                        return 0
                elif event.type == pg.MOUSEBUTTONDOWN and not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    #storing the co ordinates of the pixel where the mouse got clicked
                    clicked_row = int((mouseY-89-Board_y) // sidey)
                    clicked_col = int((mouseX-72-Board_x) // sidex)
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
                                pg.draw.line(self.screen,(128,128,128),(72+Board_x+stat[1][1]*sidex+sidex//2,89+Board_y+(stat[1][0]+stat[1][2])*sidey+sidey//2),(72+Board_x+(stat[1][1]+4)*sidex+sidex//2,89+Board_y+(stat[1][0]+stat[1][2])*sidey+sidey//2),width=3)
                            elif stat[2]==2:
                                pg.draw.line(self.screen,(128,128,128),(72+Board_x+(stat[1][1]+stat[1][2])*sidex+sidex//2,89+Board_y+stat[1][0]*sidey+sidey//2),(72+Board_x+(stat[1][1]+stat[1][2])*sidex+sidex//2,89+Board_y+(stat[1][0]+4)*sidey+sidey//2),width=3)
                            elif stat[2]==3:
                                pg.draw.line(self.screen,(128,128,128),(72+Board_x+stat[1][1]*sidex+sidex//2,89+Board_y+stat[1][0]*sidey+sidey//2),(72+Board_x+(stat[1][1]+4)*sidex+sidex//2,89+Board_y+(stat[1][0]+4)*sidey+sidey//2),width=3)
                            elif stat[2]==4:
                                pg.draw.line(self.screen,(128,128,128),(72+Board_x+stat[1][1]*sidex+sidex//2,89+Board_y+(stat[1][0]+4)*sidey+sidey//2),(72+Board_x+(stat[1][1]+4)*sidex+sidex//2,89+Board_y+stat[1][0]*sidey+sidey//2),width=3)
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
