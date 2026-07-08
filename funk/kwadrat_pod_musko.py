import pygame

from slice_spritesheet.slice_spritesheet import *


frame_fidal =  pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\gaming_assets\Ui_elements\fidel_sheet3.png').convert_alpha() 


frame_fidal = def_slice_spritesheet(frame_fidal, 32 , 32)

x_cell = 0 
y_cell = 0 

fidef_animed = frame_fidal

vrema_dla_cmenu = 15
tek = 0 
tek_anima = 0


def kw_pod_musko(surface  ,  x_pix , y_pix , dt  , x_cell , y_cell , tek , tek_anima):

    x_cell_new = x_pix // 16
    y_cell_new = y_pix // 16

    if x_cell_new == x_cell and y_cell_new ==  y_cell :
        tek += dt 

        if tek >= vrema_dla_cmenu:
            tek = 0

            if tek_anima >= 1:
                tek_anima = 2

            else:
                tek_anima += 1
     
    else:
        x_cell = x_cell_new
        y_cell  = y_cell_new
        tek_anima = 0   


    surface.blit(fidef_animed[tek_anima], (x_cell * 16 , y_cell * 16))

    return x_cell, y_cell, tek, tek_anima
