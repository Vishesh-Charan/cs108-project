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

width,hieght=800,800
side=100
row,colomn=8,8
pg.display.set_caption("Othello(Reversi)")
font= pg.font.Font("Fonts and Audio/PressStart2P-Regular.ttf",24)
class Othello_Reversi(general):
    def __init__(self,player1,player2,screen):
        super().__init__(player1,player2)
        self.board=np.zeros((row,colomn)) 
        self.board[3,3],self.board[4,4]=1,1
        self.board[3,4],self.board[4,3]=2,2
        self.screen=screen
        self.screen=pg.display.set_mode((1000,800))
    def draw_board(self):
        BG_Image= pg.image.load('Images/Othello board.png')    
        BG_Image=pg.transform.scale(BG_Image, (800,800))
        self.screen.blit(BG_Image,(100,0))
        Text= str(self.currentturnplayer()) +" Moves"
        Turn_surface=font.render(Text,True,(255,255,255))
        self.screen.blit(Turn_surface,(180,30))

    def draw_figures(self):

        whitepiece= pg.image.load('Images/White Othello.png')
        blackpiece=pg.image.load('Images/Black othello.png')
        circle_color1,circle_color2=(241, 196, 15),(1,1,1) 
        radius,side,offset=25,72,55
        whitepiece=pg.transform.scale(whitepiece,(3*radius+15,3*radius+25))
        blackpiece=pg.transform.scale(blackpiece,(3*radius+15,3*radius+25))
        for rows in range(row):
            for col in range(colomn):
                if self.board[rows][col] == 1:
                    self.screen.blit(whitepiece, (int(offset+100 + col * side + side//2+7), int(offset + rows * side + side//2)))

                elif self.board[rows][col] == 2:
                    self.screen.blit(blackpiece, (int(offset + 100 + col * side + side//2+10), int(offset + rows * side + side//2)))

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
                        opponentfound=False
                        while 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == (player%2)+1:
                            r += dr
                            c += dc
                            opponentfound=True
                        if opponentfound and 0 <= r < 8 and 0 <= c < 8 and self.board[r][c] == player:
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
        #background music
        pg.mixer.init()
        pg.mixer.music.load('Fonts and Audio/8-Bit-Indigestion.mp3')
        pg.mixer.music.play(-1)
        #initializing
        self.draw_board()
        player = 1
        game_over = False


        while True:
            self.draw_board()
            back_text="Back to menu"
            back_button = pg.Rect(570, 15, 300, 50)
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
                        self.draw_board()
                        self.draw_figures()
                        pg.mixer.init()
                        pg.mixer.music.load('Fonts and Audio/8-Bit-Indigestion.mp3')
                        pg.mixer.music.play(-1)
                    else:
                        return 0

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
                    offset = 95 #As the board doesn't fill the entire screen
                    tile = 75

                    # check if click is inside board
                    if offset <= mouseX <= offset + 8 * tile and offset <= mouseY <= offset + 8 * tile:
                        clicked_col = int((mouseX - offset-100) // tile)
                        clicked_row = int((mouseY - offset) // tile)
                        if(self.valid_move_and_update(clicked_row,clicked_col,player)):
                            #switch()
                            #player=player%2+1
                            self.changeturn()
                            player=self.current_turn
                            #this whole part handles the main gameplay using our functions, etc
                self.draw_figures()
            pg.display.update() 


