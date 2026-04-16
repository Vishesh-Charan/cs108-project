import numpy as np
import sys, os, time, pygame, pathlib, subprocess
import matplotlib.pyplot as plt
from datetime import datetime

player1=sys.argv[1]
player2=sys.argv[2]

pygame.init()
class general:
    def __init__(self, player1, player2):
        self.players=["None",player1,player2]
        self.current_turn = 1
        self.board= None
    def changeturn(self):
        self.current_turn=self.current_turn%2+1
    def currentturnplayer(self):
        return self.players[self.current_turn]
    def check_win(self,player):
        raise NotImplementedError 

def getChosenGame(game_name, player1, player2):
    if game_name.lower()=="connect4":
        from Games.connect4 import Connect4
        return Connect4(player1, player2)
    elif game_name.lower()=="othello":
        from Games.othello import Othello_Reversi
    elif game_name.lower()=="tictactoe":
        from Games.tictactoe import tic_tac_toe as TicTacToe 
        return TicTacToe(player1, player2)
    
def showmenu(screen):
    # Setting up general things like importing images, taking up fonts and colours and positioning the elements
    font_general= pygame.font.Font("PressStart2P-Regular.ttf",44)
    font_games= pygame.font.Font("PressStart2P-Regular.ttf",28)
    font_player= pygame.font.Font("PressStart2P-Regular.ttf",12)
    games = ["Connect4", "Othello", "TicTacToe"]
    game_images=["Connect_4.png", "othello.png", "tic_tac_toe.png"]
    current_sel=0    
    BG_Image= pygame.image.load('Board.png')    
    BG_Image=pygame.transform.scale(BG_Image, (1000,700))
    NORMAL_COLOR = (200, 200, 200)   
    SELECT_COLOR = (255, 255, 255)   
    HIGHLIGHT = (100, 150, 255)
    WIDTH=1000
    HEIGHT=700
    bar_width = int(WIDTH * 0.7)
    bar_height = 80
    bar_x = (WIDTH - bar_width) // 2
    bar_y = 30
    heading_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)

    trophy_img = pygame.image.load("game-trophy.png")
    trophy_size = 50
    trophy_img = pygame.transform.scale(trophy_img, (trophy_size, trophy_size))

    player1_img = pygame.image.load("sprite 1.png")
    player2_img = pygame.image.load("sprite 2.png")
    sprite_size = 180
    player1_img = pygame.transform.scale(player1_img, (sprite_size, sprite_size))   
    player2_img = pygame.transform.scale(player2_img, (sprite_size+100, sprite_size))
    player1_name = player1
    player2_name = player2
    label_width = 160
    label_height = 40
    p1_x = 80
    p1_y = HEIGHT - sprite_size - 120
    p2_x = WIDTH - sprite_size - 120
    p2_y = HEIGHT - sprite_size - 120
    p1_label_rect = pygame.Rect(
        p1_x + sprite_size//2 - label_width//2,
        p1_y + sprite_size - 10,
        label_width,
        label_height
    )
    p2_label_rect = pygame.Rect(
        p2_x+50 + sprite_size//2 - label_width//2,
        p2_y + sprite_size - 10,
        label_width,
        label_height
    )
    # Displaying the menu
    while True:
        screen.blit(BG_Image,(0,0))
        pygame.draw.rect(screen, (60, 100, 180), heading_rect, border_radius=20)
        pygame.draw.rect(screen, (240,240,255), heading_rect, 2, border_radius=20)
        trophy_x = heading_rect.x + 20
        trophy_y = heading_rect.centery - trophy_size // 2
        screen.blit(trophy_img, (trophy_x, trophy_y))
        heading_text = font_general.render("MINI GAME HUB", True, (255,255,255))
        screen.blit(heading_text, (trophy_x + trophy_size + 15, heading_rect.centery - 20))

        screen.blit(player1_img, (p1_x, p1_y))
        screen.blit(player2_img, (p2_x, p2_y))
        pygame.draw.rect(screen, (60,120,200), p1_label_rect, border_radius=15)
        pygame.draw.rect(screen, (255,255,255), p1_label_rect, 2, border_radius=15)
        pygame.draw.rect(screen, (200,120,50), p2_label_rect, border_radius=15)
        pygame.draw.rect(screen, (255,255,255), p2_label_rect, 2, border_radius=15)
        p1_text = font_player.render(player1_name, True, (255,255,255))
        p2_text = font_player.render(player2_name, True, (255,255,255))
        screen.blit(p1_text, p1_text.get_rect(center=p1_label_rect.center))
        screen.blit(p2_text, p2_text.get_rect(center=p2_label_rect.center))


        for i in range(len(games)):
            x= 450
            y=250+i*100
            rect=pygame.Rect(0,0,450,80)
            rect.center=(x+50,y+20)
            pygame.draw.rect(screen,(40,40,70),rect,border_radius=20)
            pygame.draw.rect(screen,(240,240,255),rect,3,border_radius=20)
            game_image=pygame.image.load(game_images[i])
            game_image=pygame.transform.scale(game_image, (100,80))
            screen.blit(game_image, (x-150,y-20))
            if i==current_sel:
                 pygame.draw.rect(screen, HIGHLIGHT, (x - 20, y - 10, 260, 60), border_radius=10)
                 color=SELECT_COLOR
            else:
                color=NORMAL_COLOR
            text = font_games.render(games[i], True, color)
            screen.blit(text, (x, y))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type==pygame.KEYDOWN:
                if event.key==pygame.K_UP:
                    current_sel= (current_sel-1)%len(games)
                elif event.key==pygame.K_DOWN:
                    current_sel=(current_sel+1)%len(games)
                elif event.key==pygame.K_RETURN:
                    return games[current_sel]
                
def leaderboard_data(screen,winner):
    screen = pygame.display.set_mode((1000, 900))
    font= pygame.font.Font("PressStart2P-Regular.ttf",48)
    fontsmall= pygame.font.Font("PressStart2P-Regular.ttf",24)
    BG_COLOR = (30, 30, 60)          
    #Top Text showing name of winner and the end text
    if winner=="Draw":
        text ="It's a Draw!" 
    else:
        text =f"{winner} Won!"
    end_text="Press 'Enter' to continue"
    #Setting up a side menu with options of metrics to sort the leaderboard
    menu_font = pygame.font.Font("PressStart2P-Regular.ttf", 14)
    menu_width = 200
    menu_item_height = 35
    menu_x = 630
    menu_y = 70
    items = ["Sort By: Win", "Sort By: Loss", "Sort By: W/L Ratio ", "Sort By: Name(Ascending)", "Sort By: Name(Descending)"]
    selected_index = 0
    last_index = -1
    #Setting Up Charts(I would Read history.csv for the data)
    wins= {}
    gamePlayed= {}
    with open("history.csv") as f:
        for line in f:
            line=line.strip('\n')
            if not line:
                continue
            line=line.split(',')
            winner=line[0]
            game=line[3]
            if winner in wins:
                wins[winner] += 1
            else:
                wins[winner] = 1
            if game in gamePlayed:
                gamePlayed[game] += 1
            else:
                gamePlayed[game] = 1
    sorted_win= dict(sorted(wins.items(), key=lambda x: x[1], reverse=True))
    sorted_gamePlayed= dict(sorted(gamePlayed.items(), key=lambda x: x[1], reverse=True))
    # Making Charts
    n=min(5, len(sorted_win))
    topwins= dict(list(sorted_win.items())[:n])
    names= list(topwins.keys())
    number=list(topwins.values())
    #If less then 5 players then remaining spaces will be empty but chart will have 5 spaces in any case
    if n<5:
        diff=5-n
        for i in range(diff):
            names.append("")
            number.append(0)
    fig1, ax = plt.subplots()
    ax.bar(names,number)
    ax.set_title("Top 5 players by Wins")
    ax.set_ylabel("No. of Wins")
    ax.set_xlabel("Player")
    fig1.savefig("bar_graph.png")

    labels=list(sorted_gamePlayed.keys())
    values=list(sorted_gamePlayed.values())
    total=sum(values)
    fig2,ax1= plt.subplots()
    ax1.pie(values, labels=labels, autopct=lambda p: str(int(round(p*total/100))))
    ax1.set_title("Top Games Played")
    fig2.savefig("pie_chart.png")

    bar_graph= pygame.image.load("bar_graph.png")
    pie_chart=pygame.image.load("pie_chart.png")

    bar_graph = pygame.transform.scale(bar_graph, (550, 350))
    pie_chart = pygame.transform.scale(pie_chart, (550, 360))
    #Displaying Everything
    while True:
        screen.fill(BG_COLOR)
        text_surface = font.render(text, True, (230, 230, 255))
        rect = text_surface.get_rect(center=(600//2, 40))
        endtext_surface=fontsmall.render(end_text,True, (230,230,255))
        end_rect=endtext_surface.get_rect(center=(500,885))
        screen.blit(text_surface, rect)
        screen.blit(bar_graph, (50, 90))
        screen.blit(pie_chart, (50, 470))
        screen.blit(endtext_surface, end_rect)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for i in range(len(items)):
                    rect = pygame.Rect(menu_x, menu_y + i * menu_item_height,
                                        menu_width, menu_item_height)
                    if rect.collidepoint(mouse_pos):
                        selected_index = i
        if selected_index!=last_index:
            last_index=selected_index
            if selected_index==0:
                subprocess.run(["sh", "leaderboard.sh", "wins"])
            elif selected_index==1:
                subprocess.run(["sh", "leaderboard.sh", "losses"])
            elif selected_index==2:
                subprocess.run(["sh", "leaderboard.sh", "w/lratio"])
            elif selected_index==3:
                subprocess.run(["sh", "leaderboard.sh", "namea"])
            elif selected_index==4:
                subprocess.run(["sh", "leaderboard.sh", "named"])
        menu_height = len(items) * menu_item_height
        menu_surface = pygame.Surface((menu_width, menu_height), pygame.SRCALPHA)
        menu_surface.fill((55, 55, 95, 220))
        screen.blit(menu_surface, (menu_x, menu_y))

        for i, texty in enumerate(items):
            y = menu_y + i * menu_item_height
            txt = menu_font.render(texty, True, (230, 230, 255))
            screen.blit(txt, (menu_x + 15, y + 9))

            if i == selected_index:
                tick = menu_font.render("✔", True, (120, 255, 160))
                screen.blit(tick, (menu_x - 10, y + 9))
        pygame.display.flip()

def postgame(screen,winner):
    screen = pygame.display.set_mode((1000, 700))
    font= pygame.font.Font("PressStart2P-Regular.ttf",24)
    BG_COLOR = (30, 30, 60)          
    NORMAL_COLOR = (200, 200, 200)   
    HOVER_COLOR = (255, 255, 255)
    # Showing the winner and giving the player options to Continur or Quit, Continue opens the menu and Quit quits the game
    if winner=="Draw":
        text ="It's a Draw!\n Wanna Play Again!!" 
    else:
        text =f"{winner} Won!\n Wanna Play Again!!"
    text_surface = font.render(text, True, (255, 255, 255))  
    continue_button = pygame.Rect(350, 260, 200, 60)
    quit_button = pygame.Rect(350, 340, 200, 60)
    # Load firework frames
    frames = []
    folder = "firework_frames"

    for file in sorted(os.listdir(folder)):
        if file.endswith(".png"):
            img = pygame.image.load(os.path.join(folder, file)).convert_alpha()
            img = pygame.transform.scale(img, (120, 120))
            frames.append(img)

    # Store active fireworks
    fireworks = []  # [x, y, frame_index]

    clock = pygame.time.Clock()

    while True:
        screen.fill(BG_COLOR)
        mouse_pos = pygame.mouse.get_pos()
        hoveredc = continue_button.collidepoint(mouse_pos)
        hoveredq= quit_button.collidepoint(mouse_pos)
        if hoveredc:
            c_color=HOVER_COLOR
        else:
            c_color=NORMAL_COLOR
        if hoveredq:
            q_color=HOVER_COLOR
        else:
            q_color=NORMAL_COLOR
        # Randomly spawn fireworks
        if np.random.rand() < 0.03:
            x = np.random.randint(50, 950)
            y = np.random.randint(50, 650)
            fireworks.append([x, y, 0])

        # Draw & update fireworks
        dt = clock.tick(60) / 1000  # time in seconds
        for fw in fireworks:
            x, y, frame_idx = fw
            if frame_idx < len(frames):
                screen.blit(frames[int(frame_idx)], (x, y))
                fw[2]+=8*dt

        # remove finished ones
        fireworks = [fw for fw in fireworks if fw[2] < len(frames)]
        
        screen.blit(text_surface,(300,150))
        pygame.draw.rect(screen,c_color,continue_button,3)
        pygame.draw.rect(screen,q_color,quit_button,3)
        cont_text = font.render("Continue", True, (255, 255, 255))
        quit_text = font.render("Quit", True, (255, 255, 255))

        cont_rect = cont_text.get_rect(center=continue_button.center)
        quit_rect = quit_text.get_rect(center=quit_button.center)

        screen.blit(cont_text, cont_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 0
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if continue_button.collidepoint(event.pos):
                    return 1
                elif quit_button.collidepoint(event.pos):
                    return 0

def UpdateHistory(winner,loser,game_name):
    with open("history.csv", "a") as f:
        date = datetime.now().strftime("%Y-%m-%d")
        f.write(f"\n{winner},{loser},{date},{game_name}")

def main():
    player1=sys.argv[1]
    player2=sys.argv[2]

    while True:
        screen = pygame.display.set_mode((1000, 700))
        pygame.display.set_caption("Mini Game Hub")
        screen.fill((28, 40, 51))
        pygame.display.update()
        game_name=showmenu(screen)
        game=getChosenGame(game_name,player1,player2)
        if game is None:
            continue
        else:
            winner=game.run()
        if winner:
            print(f"{winner} Won, Congrats!")
            if winner==player1:
                loser=player2
            else:
                loser=player1
            UpdateHistory(winner,loser,game_name)

        else:
            winner="Draw"
        screen.fill((28, 40, 51))
        pygame.display.update()
        leaderboard_data(screen,winner)
        next=postgame(screen,winner)
        if next==0:
            break
        else:
            continue
        
    pygame.quit()
    exit()
    
if __name__ == "__main__":
    main()            
                

