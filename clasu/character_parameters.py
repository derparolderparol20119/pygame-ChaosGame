import pygame



class Character_parameters:
    def __init__(self, name, x, y , osn_kwadrat , fontsize):
        self.start = False
        self.aktiw_moving = False

        self.name = name
        self.x = x
        self.y = y
        self.osn_kwadrat = osn_kwadrat
        self.fontsize = fontsize
        self.rect_interaction = None

        self.font = []

        self.offset_x = 0
        self.offset_y = 0

        self.plear = None

        self.del_ikonka = pygame.Rect(self.x + 3, self.y + 2, 12, 12)

        self.full_window = True

    def init_font(self):
        if not self.font:
            for size in self.fontsize:
                font = pygame.font.Font(None, size)
                self.font.append(font)

    def draw_rect(self, surface):

        if self.full_window == True:
            pol_snurf = pygame.Surface((self.osn_kwadrat[1][0], self.osn_kwadrat[1][1]), pygame.SRCALPHA) 
            pygame.draw.rect(pol_snurf,(40, 40, 40, 150),(0, 0, self.osn_kwadrat[1][0], self.osn_kwadrat[1][1]))
            surface.blit(pol_snurf, (self.x, self.y + self.osn_kwadrat[0][1]))

            pygame.draw.rect(surface, (0, 0, 0), (self.x , self.y + 14, self.osn_kwadrat[1][0], self.osn_kwadrat[1][1]) , width=1)

            self.draw_entrails(surface)
            #self.draw_parameters(surface)
            self.draw_main_system_hero(surface)
            self.draw_hp_kon(surface)
            self.draw_skil(surface)




        rect_wzaima = pygame.draw.rect(surface, (60, 60, 60), (self.x, self.y, self.osn_kwadrat[0][0], self.osn_kwadrat[0][1]))
        self.rect_interaction = rect_wzaima

        self.del_ikonka.topleft = (self.x + 3 , self.y + 2)
        pygame.draw.rect(surface , (200, 200, 200) , self.del_ikonka , width=2 )

        pygame.draw.rect(surface, (0, 0, 0), (self.x, self.y, self.osn_kwadrat[0][0], self.osn_kwadrat[0][1]) , width=2)

        text_surf = self.font[0].render(f"параметры: {self.plear.name}", True, (200, 200, 200))
        surface.blit(text_surf, (self.x + 20 , self.y ))

    
    def draw_entrails(self, surface):
        scaled = pygame.transform.scale(
            self.plear.render_layer_static,
            (
                self.plear.render_layer_static.get_width() * 3,
                self.plear.render_layer_static.get_height() * 3
            )
        )

        rect = scaled.get_rect(topleft=(self.x, self.y))

        surface.blit(scaled , rect)


        pygame.draw.line(surface, (40, 40, 40), rect.topright , rect.bottomright , 2)
        pygame.draw.line(surface, (40, 40, 40), rect.bottomright, rect.bottomleft, 2)


    def draw_parameters(self, surface):
        blok_atribut_hg_sum = 0

        for i in self.plear.parameter_list:
            blok_atribut = i.draw_atribut(surface, self.x + 220, self.y - 13  + blok_atribut_hg_sum , font = self.font)
            blok_atribut_hg_sum += blok_atribut.height  


    def draw_main_system_hero(self , surface):

        x = self.x + 220
        y = self.y + 20

        timer = 0

        for key, value in self.plear.main_system_hero.items():

            text = f"{key[:17]}: {value}"

            img = self.font[3].render(text, True, (255, 255, 255))

            surface.blit(img, (x, y))

            y += 20

            timer += 1 

            if timer >= 11:
                timer = 0
                y = self.y + 20
                x += 150

        timer = 0
        x += 160
        y = self.y + 20
        
        for param in self.plear.parameter_list:
            text = f"{param.name[:17]}: {param.value}"

            img = self.font[3].render(text, True, (255, 255, 255))

            surface.blit(img, (x, y))

            y += 20

            timer += 1 

            if timer >= 11:
                timer = 0
                y = self.y + 40
                x += 160
        

    def draw_skil(self, surface):
        x = self.x + 540
        y = self.y + 20

        timer = 0

        for i in self.plear.sklil_list:

            text = f"{i.name[:17]}: {i.value * i.interest_level}%"

            img = self.font[3].render(text, True, (255, 255, 255))

            surface.blit(img, (x, y))

            y += 20

            timer += 1 

            if timer >= 11:
                timer = 0
                y = self.y + 20
                x += 150



    def draw_hp_kon(self, surface):

        x = self.x 
        y = self.y + 240
        dobul_x = 180

        timer = 0 
        spr_full = 0

        for osn in self.plear.part:
            text = f"{osn.name}: {int(osn.hp)} / {int(osn.hp_max)}"

            img = self.font[3].render(text, True, (255, 55, 55))

            surface.blit(img, (x, y))

            y += 20

            timer += 1

            for i in osn.parametrs:
                text = f"    {i.name}: {int(i.value)}"
                img = self.font[3].render(text, True, (55, 55, 255))
                surface.blit(img, (x, y))
                y += 20

                timer += 1

                if timer >= 20:
                    x += dobul_x
                    y = self.y + 240
                    timer = 0


            for kon in osn.koneshonsti:
                for key , value in kon.spr_wozdeistwiam_test.items():
                    spr_full += value[0]
                       
                text = f"{kon.name[:11]}: {int(kon.hp)} / {int(kon.hp_max) } | {spr_full}"

                img = self.font[3].render(text, True, (255, 255, 255))

                surface.blit(img, (x, y))

                y += 20

                timer += 1

                if timer >= 20:
                    x += dobul_x
                    y = self.y + 240
                    timer = 0

                spr_full = 0



sprawka_parameters = Character_parameters(name = "параметры" , x = 200 , y = 200 , osn_kwadrat = [(500, 15) , (500 , 700)] , fontsize = [20 , 20 , 15 , 20 , 25])

sprawka_parameters.init_font()


