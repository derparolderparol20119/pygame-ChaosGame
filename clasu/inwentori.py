import pygame
from clasu.brona import *
from funk.bar_poloski_spr import *
from clasu.sumki import * 

from data.game_items.armor.creation_armor import *
from data.game_items.weapons.weapons_sozdanie import *

from data.game_items.bags.bags_load import *

class Ikonki_draw():
    def __init__(self , name , x , y  , osn_kwadrat , fontsize , polna_ikona , iasheki , pokaz_nadetosti ):
        self.name = name
        self.x = x
        self.y = y
        self.osn_kwadrat = osn_kwadrat
        self.fontsize = fontsize
        self.zakruta = False
        self.del_ikonka = pygame.Rect(self.x + 3, self.y + 2, 12, 12)
        self.polna_ikona = polna_ikona
        self.font = []
        self.iasheki = iasheki
        self.massa = 0
        self.max_massa = 0 
        
        self.scroll_y = 0
        self.scroll_speed = 25
        self.target_scroll_y = 0
        self.pokaz_nadetosti = pokaz_nadetosti
        self.wuborka = None
        self.spis_pridm_spr = None

        self.priwazka_inwentara = None



    def init_font(self):
        if not self.font:
            for size in self.fontsize:
                    font = pygame.font.Font(None, size)
                    self.font.append(font)



    def ikona_print(self , screen , otrisowka_podswetki , wuborka , wuzow_sprawki , selected_items):
        spis_pridm_spr = []
        ikona_wsa = None

        if not self.zakruta:
            self.del_ikonka.topleft = (self.x + 3 , self.y + 2)

            wind_iKonka = pygame.draw.rect(screen,(60, 60, 60),(self.x, self.y, self.osn_kwadrat[0][0], self.osn_kwadrat[0][1]))
            del_ikona = pygame.draw.rect(screen , (200, 200, 200) , self.del_ikonka , width=2 )
            pygame.draw.rect(screen, (10, 10, 10) , (self.x , self.y , self.osn_kwadrat[0][0] , self.osn_kwadrat[0][1] ) , width= 2)

            text_surf = self.font[0].render(self.name, True, (255, 255, 255))
            screen.blit(text_surf, (self.x + 20 , self.y))
            spisok_iasheki = None

            tek_massa = 0
            tek_massa_max = 0 

            if self.wuborka:
                tek_massa = sum(p.masa for p in self.wuborka.pridmetu)
                tek_massa_max = self.wuborka.masa_max
            else:
                tek_massa = 0
                tek_massa_max = 0

            
            tek_massa = str(tek_massa) + " / " + str(tek_massa_max)
            text_surf2 = self.font[2].render(tek_massa  ,  True, (255, 255, 255))
            screen.blit(text_surf2, (self.x + 420 , self.y + 2))


            if self.polna_ikona:
                pol_snurf = pygame.Surface((self.osn_kwadrat[1][0], self.osn_kwadrat[1][1]), pygame.SRCALPHA) 
                pygame.draw.rect(pol_snurf,(40, 40, 40, 150),(0, 0, self.osn_kwadrat[1][0], self.osn_kwadrat[1][1]))
                screen.blit(pol_snurf, (self.x, self.y + self.osn_kwadrat[0][1]))

                pol_snurf2 = pygame.Surface((self.osn_kwadrat[0][1] + 16, self.osn_kwadrat[1][1] ), pygame.SRCALPHA) 
                pygame.draw.rect(pol_snurf2,(20, 20, 20, 200),( 0 , 0 , self.osn_kwadrat[0][1] + 16, self.osn_kwadrat[1][1] ))
                screen.blit(pol_snurf2, (self.x, self.y + self.osn_kwadrat[0][1]))

                
                pol_snurf3 = pygame.Surface((self.osn_kwadrat[0][1] + 7, self.osn_kwadrat[1][1] ), pygame.SRCALPHA) 
                pygame.draw.rect(pol_snurf3,(20, 20, 20, 200),( 0 , 0 , self.osn_kwadrat[0][1] + 7, self.osn_kwadrat[1][1] ))

                screen.blit(pol_snurf3, (self.x + 477 , self.y + self.osn_kwadrat[0][1]))

                spisok_iasheki , spis_pridm_spr = self.slot_print(screen , otrisowka_podswetki , wuborka , wuzow_sprawki , selected_items )

                ikona_wsa = pygame.draw.rect(screen, (10, 10, 10) , (self.x , self.y , self.osn_kwadrat[1][0] , self.osn_kwadrat[1][1] + self.osn_kwadrat[0][1] ) , width= 1)


            self.spis_pridm_spr = spis_pridm_spr
            return  wind_iKonka , self , spisok_iasheki , spis_pridm_spr , ikona_wsa
        
        else:
            return  None , None , None , None , None



    def slot_print(self, screen , otrisowka_podswetki , wuborka , wuzow_sprawki , selected_items ):
        iaseka_ta = False

        if self.wuborka is None:
            self.wuborka = self.iasheki[0]
        
        wuborka = self.wuborka

        if self.pokaz_nadetosti != None:
            wse_shasti_nadetoi_broni = self.wuwod_wseh_shat_bron()

        view_height = self.osn_kwadrat[1][1]
        slot_height = self.osn_kwadrat[0][1] + 14  # ← в 2 раза выше
        slot_width = self.osn_kwadrat[0][0] - 54




        if wuborka != self.iasheki[0]:
            content_height = len(wuborka.pridmetu) * slot_height + 3
        elif self.pokaz_nadetosti is not None:
            content_height = (len(wuborka.pridmetu) * slot_height +5 +len(wse_shasti_nadetoi_broni) * slot_height +3)
        else:
            content_height = len(wuborka.pridmetu) * slot_height + 3

        bar_height = max(20,view_height * view_height / content_height)



        slot_y = self.y + self.osn_kwadrat[0][1] + self.scroll_y # под заголовком
        shet = 2
        slot_y2 = slot_y

        spisok_iasheki = []
        spis_pridm_spr = []

        view_top = self.y + self.osn_kwadrat[0][1]

        if wuborka is None:
            wuborka = self.iasheki[0]

        max_scroll = max(0, content_height - view_height)

        for iashek in self.iasheki:
            if otrisowka_podswetki:
                if otrisowka_podswetki[0] == True:
                    if otrisowka_podswetki[3].name_iaseki == iashek.name_iaseki:

                        pol_snurf1 = pygame.Surface((20 , 20), pygame.SRCALPHA) 
                        pygame.draw.rect(pol_snurf1,(75, 75, 75, 195),(0, 0, 20, 20))
                        screen.blit(pol_snurf1, (self.x + 478 , slot_y2 - self.scroll_y ))

            if wuborka != None: #!

                if wuborka.name_iaseki == iashek.name_iaseki:
                    
                    pol_snurf2 = pygame.Surface((20 , 20), pygame.SRCALPHA) 
                    pygame.draw.rect(pol_snurf2,(95, 95, 95, 215),(0, 0, 20, 20))
                    screen.blit(pol_snurf2, (self.x + 478 , slot_y2 - self.scroll_y))


            screen.blit(iashek.izb, (self.x + 478 , slot_y2 - self.scroll_y))
            iashek.boks_iaseki.topleft = (self.x + 478 , slot_y2 - self.scroll_y)

            spisok_iasheki.append(iashek)

            slot_y2 += 20

        if wuborka != None:
            clip_rect = pygame.Rect(self.x,self.y + self.osn_kwadrat[0][1],self.osn_kwadrat[1][0],self.osn_kwadrat[1][1])
            screen.set_clip(clip_rect)

            if selected_items: # выделение 
                pol_snurf3 = pygame.Surface((slot_width, slot_height), pygame.SRCALPHA)
                for sel_item in selected_items:
                    if sel_item[2] == wuborka:
                        iaseka_ta = True


            for id_iaseki, predmet in enumerate(wuborka.pridmetu):
                pol_snurf = pygame.Surface((slot_width, slot_height), pygame.SRCALPHA)

                if shet % 2:
                    color = (40, 40, 40, 150)
                else:
                    color = (40, 40, 40, 0)

                pygame.draw.rect(pol_snurf, color, (0, 0, slot_width, slot_height))

                krit = pygame.draw.rect(screen, (25 , 25 , 25 ), (self.x + 32, slot_y, slot_width - 226, slot_height  ) , width=1)

                spis_pridm_spr.append((krit , predmet , id_iaseki , wuborka ))

                screen.blit(pol_snurf, (self.x + 32, slot_y))

                screen.blit(predmet.izb, (self.x , slot_y))

                if iaseka_ta: # выделение 
                    for sel_item in selected_items:
                        if id_iaseki == sel_item[1]:
                            pygame.draw.rect(pol_snurf3, (120 , 120 , 120), (0, 0, slot_width, slot_height))
                            screen.blit(pol_snurf3, (self.x + 32, slot_y ))
                            

                text_surf = self.font[1].render(predmet.name, True, (200, 200, 200))
                screen.blit(text_surf, (self.x + 33 , slot_y + 7))

                text_surf = self.font[1].render(predmet.tip, True, (170, 190, 220))
                screen.blit(text_surf, (self.x + 252 , slot_y + 7))

                slot_y += slot_height

                shet += 1

            

        
        if wuborka == self.iasheki[0] and self.pokaz_nadetosti != None:
            pygame.draw.rect(screen, (140 , 140 , 140 ), (self.x  , slot_y , 477, 2))
            slot_y += 2

            wubr_nadet = wuborka.pridmetu + wse_shasti_nadetoi_broni
            pol_snurf = pygame.Surface((slot_width, slot_height), pygame.SRCALPHA)

            for id_iaseki, predmet in  enumerate(wse_shasti_nadetoi_broni):
                if shet % 2:
                    color = (40, 40, 40, 150)
                else:
                    color = (40, 40, 40, 0)

                pygame.draw.rect(pol_snurf, color, (0, 0, slot_width, slot_height))

                krit = pygame.draw.rect(screen, (25 , 25 , 25 ), (self.x + 32, slot_y, slot_width - 226, slot_height  ) , width=1)

                spis_pridm_spr.append((krit , predmet , id_iaseki , wubr_nadet))

                screen.blit(pol_snurf, (self.x + 32, slot_y))

                screen.blit(predmet.izb, (self.x , slot_y))
                screen.blit(self.pokaz_nadetosti, (self.x + 26 , slot_y + 25))

                text_surf = self.font[1].render(predmet.name, True, (200, 200, 200))
                screen.blit(text_surf, (self.x + 33 , slot_y + 7))

                text_surf = self.font[1].render(predmet.tip, True, (170, 190, 220))
                screen.blit(text_surf, (self.x + 250 , slot_y + 7))

                slot_y += slot_height

                shet += 1



        max_scroll = max(0, content_height - view_height)
        self.target_scroll_y = max(-max_scroll, min(0, self.target_scroll_y))

        self.scroll_y += (self.target_scroll_y - self.scroll_y) * 0.25

        if abs(self.scroll_y - self.target_scroll_y) < 0.5:
            self.scroll_y = self.target_scroll_y

        if content_height > view_height:
            self.wuzow_polzunka( screen ,  content_height ,  view_height , view_top , max_scroll )

        screen.set_clip(None)

        if wuzow_sprawki != None:
            self.pridmet_sprawka_print(screen , wuzow_sprawki[0] , wuzow_sprawki[1] , wuzow_sprawki[2])

        return spisok_iasheki , spis_pridm_spr


    def pridmet_sprawka_print(self , screen , predmet , x , y ):
        predmet.wuzow_sprawki(screen , x +  13 , y + 13 , self.font[3])

    def wuzow_polzunka(self , screen ,  content_height ,  view_height , view_top , max_scroll ):

        if content_height > view_height:
            bar_x = self.x + self.osn_kwadrat[1][0] - 6
            bar_width = 4

            bar_height = max(20,view_height * view_height / content_height)

            scroll_percent = -self.scroll_y / max_scroll if max_scroll else 0

            bar_y = view_top + scroll_percent * (view_height - bar_height)

            pygame.draw.rect(screen,(180, 180, 180),(bar_x - 22, bar_y, bar_width, bar_height),border_radius=3)

    def wuwod_wseh_shat_bron(self):
    
        spisok_weshei = set()
    
        if not self.priwazka_inwentara:
            return []
    
        for osn in self.priwazka_inwentara.part:
            for limb in osn.koneshonsti:
                for slot in limb.slots_ekwip:
                    if slot["nadetost"] is not None:
                        spisok_weshei.add(slot["nadetost"])
    
        return list(spisok_weshei)

class Iashika():
    def __init__(self , pridmetu , masa_max , name_iaseki , izb ):
        self.pridmetu = pridmetu
        self.masa_max = masa_max
        self.name_iaseki = name_iaseki
        self.izb = izb
        self.boks_iaseki = pygame.Rect(0, 0, 20, 20)


    
    def pridmet_sprawka_print(self ):
        print(1)
    

    @property
    def current_mass(self):
        return sum(p.masa for p in self.pridmetu)




sumka_igroka = Iashika(pridmetu= [ sword , sword2 , sword3 , pika1 , gambeson , latna_kirasa , kolshuga , sword4] , masa_max = 700000000000000, name_iaseki = "sumka" , izb = sumka) 

sumka_karman = Iashika(pridmetu = [] , masa_max = 100000 , name_iaseki = "sumka2" , izb = sumka2)


inwentar = Ikonki_draw(name = "инвентарь" , x = 10 , y = 10  , osn_kwadrat = [(500, 15) , (500 , 500)] , fontsize = [20 , 22 , 18 , 16 ] , polna_ikona = False , iasheki = [] , pokaz_nadetosti= pokaz_nadetosti) 



sudushka = Iashika(pridmetu= [] , masa_max = 100000, name_iaseki = "sanadalka" , izb = sumka) 

sudushka2 = Iashika(pridmetu= [sumoska , gambeson ] , masa_max = 7000000000000000, name_iaseki = "kuku" , izb = sumka) 



sudushka3 = Iashika(pridmetu= [gambeson] , masa_max = 700000000000000, name_iaseki = "sanadalka3" , izb = sumka) 
sumoska.iaseka = sudushka3


obshai = Ikonki_draw(name = "местность" , x = 150 , y = 10  , osn_kwadrat = [(500, 15) , (500 , 500)] , fontsize = [20 , 22 , 18 , 16 ] , polna_ikona = False , iasheki = [] , pokaz_nadetosti = None) 