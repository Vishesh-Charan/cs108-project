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
Board_x=150
Board_y=0
offsetx=94+ Board_x
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
pg.display.set_caption("Connect 4")
class Connect4(general):
    def __init__(self,player1,player2,screen):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn))
        self.screen=screen 
    def draw_lines(self):
        self.screen.blit(BG_Image,(Board_x,Board_y))
        Text= str(self.currentturnplayer()) +" Moves"
        Turn_surface=font.render(Text,True,(255,255,255))
        self.screen.blit(Turn_surface,(220+Board_x,650))

        
            
    def draw_figures(self):
        for rows in range(row):
            for col in range(colomn):
                if self.board[rows][col] == 1:
                    self.screen.blit(red,(int(offsetx+col * sidex+3), int(offsety+rows*sidey+5)))
                elif self.board[rows][col] == 2:
                    self.screen.blit(yellow,(int(offsetx+col * sidex+3), int(offsety+rows*sidey+5)))
    
    def moveback(self,screen):
        font = pg.font.Font("PressStart2P-Regular.ttf", 19)
        small_font = pg.font.Font("PressStart2P-Regular.ttf", 16)
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
                

    def ball_animation(self,row,col,player):
        #making the ball falling animation
        speed=10
        i=offsety
        while i<int(offsety+row*sidey+5):
            i=min(i+speed,int(offsety+row*sidey+5))
            self.draw_lines()
            self.draw_figures()
            if player == 1:
                    self.screen.blit(red,(int(offsetx+col * sidex+3), i))
            elif player == 2:
                    self.screen.blit(yellow,(int(offsetx+col * sidex+3), i))
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
        pg.display.update()
        #initializing
        pg.mixer.init()
        pg.mixer.music.load('8-Bit-Indigestion.mp3')
        pg.mixer.music.play(-1)
        self.draw_lines()
        player = 1
        game_over = False


        while True:
            self.draw_lines()
            back_text="Back to menu"
            back_button = pg.Rect(540, 15, 300, 50)
            mouse_position=pg.mouse.get_pos()
            hoveredb= back_button.collidepoint(mouse_position)
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
            #Adding hover
            hovered_col = int((mouse_position[0]-offsetx) // sidex)
            if hovered_col>=0 and hovered_col<7:
                hover_surface = pg.Surface((sidex, row * sidey), pg.SRCALPHA)
                hover_surface.fill((200, 200, 200, 80))
                self.screen.blit(hover_surface,(offsetx + hovered_col * sidex+5, offsety+4))
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
                        pg.mixer.music.load('8-Bit-Indigestion.mp3')
                        pg.mixer.music.play(-1)
                    else:
                        return 0
                elif event.type == pg.MOUSEBUTTONDOWN and not game_over:
                    mouseX = event.pos[0]
                    mouseY = event.pos[1]
                    #storing the co ordinates of the pixel where the mouse got clicked
                    clicked_row = int((mouseY-offsety) // sidey)
                    clicked_col = int((mouseX-offsetx) // sidex)
                   
                    #events after the move is made(mouse click)
                    if clicked_col>=0 and clicked_col<7:
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
                        self.screen.blit(green,(int(offsetx+points[1]*sidex+3), int(offsety+points[0]*sidey+5)))
                        pg.display.update()
                        pg.time.delay(100)
                    pg.time.delay(500)
                    return winner
                else:
                    for points in stat[1]:
                        self.screen.blit(green,(int(offsetx+points[0]*sidex+3), int(offsety+points[1]*sidey+5)))
                        pg.display.update()
                        pg.time.delay(100)
                    pg.time.delay(500)
                    return winner
            pg.display.update() 


