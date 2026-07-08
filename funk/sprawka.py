import pygame
from Screen_controller_funk_draw.ScreenController import *

def sprawka(x , y , screen , igrowoe_okrugenie_dla_wzaideistwia, font , controller , pokraska = None , klik = None , spis_atribut_klas = None , plear = None , wuborka_ydal = None , leg_predmetu = None , ): # 
    square_surf = pygame.Surface((200, 200), pygame.SRCALPHA) 
    pygame.draw.rect(square_surf, (30, 30, 30, 150), (0, 0, 200, 200))
    pygame.draw.rect(screen , (0 , 0 , 0) , (x , y , 200 , 200) ,width=1)
    screen.blit(square_surf, (x , y))

    izb_teks_spr_spis = []
    dobawka = 0
    wx, wy = controller.screen_to_world(x , y)

    spr_aktiw = True

    if pokraska:
        square_surf2 = pygame.Surface((pokraska.width, pokraska.height), pygame.SRCALPHA) 
        pygame.draw.rect(square_surf2, (250, 230, 250, 150), (0, 0, pokraska.width, pokraska.height))

    for i in igrowoe_okrugenie_dla_wzaideistwia:
        if hasattr(i, "xit_boks") :
            if i.xit_boks.collidepoint(wx, wy):

                if pokraska:
                    screen.blit(square_surf2, (pokraska.x , pokraska.y))

                for sl_text_funk in i.sprawka_text: 
                    izb_teks_spr = pygame.draw.rect(screen , (0 , 0 , 0) , (x , y + dobawka , 200 , 30) ,width=1)
                    text_surf = font.render(sl_text_funk["text"], True, (255, 255, 255))
                    screen.blit(text_surf, (x + 15 , y + 8 + dobawka))
                    dobawka += 30
                    if klik and izb_teks_spr.collidepoint(klik.x , klik.y):
                        method_name = sl_text_funk["funk"]      
                        method = getattr(i, method_name) 
                        if spis_atribut_klas:  
                            for rect, obj in spis_atribut_klas:
                                if i == obj:  
                                    method(rect , i) # method(rect)
                                    break
                                else:
                                    print("ошбыка 1")

                        spr_aktiw = False                                


                    izb_teks_spr_spis.append(izb_teks_spr) 

        elif hasattr(i, "podswetka"):
            if i.check_click((wx, wy)):
                if pokraska:
                    screen.blit(square_surf2, (pokraska.x , pokraska.y))

                for sl_text_funk in i.sprawka_text: 
                    izb_teks_spr = pygame.draw.rect(screen , (0 , 0 , 0) , (x , y + dobawka , 200 , 30) ,width=1)
                    text_surf = font.render(sl_text_funk["text"], True, (255, 255, 255))
                    screen.blit(text_surf, (x + 15 , y + 8 + dobawka))
                    dobawka += 30
                    if klik and izb_teks_spr.collidepoint(klik.x , klik.y):
                        method_name = sl_text_funk["funk"]      
                        method = getattr(i, method_name) 
                        if leg_predmetu:  
                            for obj in leg_predmetu:
                                #print(i , "|||" , obj)
                                if i == obj:  
                                    method(plear)
                                    break
                                else:
                                    print("ошбыка 2" )

                        spr_aktiw = False                                


                    izb_teks_spr_spis.append(izb_teks_spr) 
            
        else:
            if i[0].collidepoint(x , y): 
                if pokraska:
                    screen.blit(square_surf2, (pokraska.x , pokraska.y))

                for sl_text_funk in i[1].sprawka_text: 
                    izb_teks_spr = pygame.draw.rect(screen , (0 , 0 , 0) , (x , y + dobawka , 200 , 30) ,width=1)
                    text_surf = font.render(sl_text_funk["text"], True, (255, 255, 255))
                    screen.blit(text_surf, (x + 15 , y + 8 + dobawka))
                    dobawka += 30
                    if klik and izb_teks_spr.collidepoint(klik.x , klik.y):
                        method_name = sl_text_funk["funk"]      
                        method = getattr(i[1], method_name) 
                        if spis_atribut_klas:   
                            method(plear , (x , y) , wuborka_ydal)

                        spr_aktiw = False                                


                    izb_teks_spr_spis.append(izb_teks_spr)


    return izb_teks_spr_spis , spr_aktiw

            


