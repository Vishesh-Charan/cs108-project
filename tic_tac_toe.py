import pygame as pg
import numpy as np
import sys

pg.init() 
#initializing pygame

width,hieght=
screen=pg.display.set_mode(width,hieght)
#I made a variable "screen" which refers to our display of width*hieght
pg.display.set_caption("Tic Tac Toe")
#wrote caption
#now lets set a background color 
bg-color=
screen.fill(bg-color)

row,colomn=10,10
area=np.zeros(row,colomn)
#initialized the area

def draw_lines():
    #making the arena lines :)
    #lets initialize the variables first 
    color,border_size,side=
    #its line's color,width and side lenth of square
    # horizontal
    for i in range(1, row):
        pg.draw.line(screen,color, (0, i * side), (width, i * side), border_size)
    # vertical
    for i in range(1, colomn):
        pg.draw.line(screen,color, (i * side, 0), (i * side, hieght), border_size)
        
