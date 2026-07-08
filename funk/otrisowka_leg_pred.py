import pygame


def otrisowka_leg_predmetow(skrean , spisok_predmetow , igrowoe_okrugenie_personag):
    for i in spisok_predmetow:
        skrean.blit(i.image, i.rect)

        if i.podswetka == True:
            i.draw_outline(skrean)
        
        if i.prudmet == None:
            i.ybrat_iz_spiskow((spisok_predmetow , igrowoe_okrugenie_personag))

