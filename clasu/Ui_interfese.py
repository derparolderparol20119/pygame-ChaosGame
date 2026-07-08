import pygame
from funk.bar_poloski_spr import *
from funk.dos_morgi import *
# как зделать проверить где рисуетца интерфейс


class Ui_interfes():
    def __init__(self , x , y , key_buttun  , klilk , plear , surface , iniciatiw , controller  ):
        self.x_poz_maus = x
        self.y_poz_maus = y

        self.key_buttun = key_buttun 
        self.klilk = klilk # ((x ,y) , 1)
        self.plear = plear
        self.surface = surface 
        self.size_screen = self.surface.get_size()

        self.font = pygame.font.Font(None , 20)
        self.font2 = pygame.font.Font(None , 15)
        self.font3 = pygame.font.Font(None , 40)



        self.doun_panel = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\gaming_assets\Ui_elements\doun_panel.png').convert_alpha()
        self.doun_peremushka = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\gaming_assets\Ui_elements\doun_peremushka.png').convert_alpha()

        self.hover_card = None          # карта под мышью
        self.hover_start_time = 0       # когда навели
        self.tooltip_visible = False

        self.hover_delay = 400          # обычная задержка (мс)
        self.fast_hover_delay = 50     # быстрая задержка
        self.iniciatiw = iniciatiw
        self.start_batal = False
        self.podswetka_karta = None
        

        self.controller = controller

        self.smena_x = 0
        self.smena_y = 0

        self.dragging = False
        self.drag_offset_x = 0



        self.spisok_kart = plear.aktiwator  # список карт для отображения
        self.spisok_vuvoda_cards = []  # список выведенных карт на экран

        self.rect_ne_xodit = None  # область для перетаскивания

        self.container_x = 0
        self.container_y = 0 


    def ui_display(self  ):
        width , height = self.size_screen

        x_k , y_k = pos_percent(width , height, 0.1, 1 , padding_x=0, padding_y=-self.doun_panel.get_height())


        self.mein_panel_doun(x_k , y_k )


        if self.start_batal == True:
            x_k3 , y_k3 = pos_percent(width , height, 0.22, 0.001)
            self.iniciatiw.draw_initiative_scale( x_k3 , y_k3 , self.surface , self.x_poz_maus , self.y_poz_maus)



    def ui_update(self , poz , klilk , key_buttun ):
        self.x_poz_maus = poz[0]
        self.y_poz_maus = poz[1]
        self.klilk = klilk
        self.key_buttun = key_buttun


    def add_card(self, card):
        if isinstance(card, list):
            for c in card:
                self.spisok_kart.append(c)

        else:
            self.spisok_kart.append(card)

    


    def mein_panel_doun(self, x_nash, y_nash):

        self.surface.blit(self.doun_panel, (x_nash, y_nash))
        self.rect_ne_xodit = pygame.Rect(x_nash , y_nash , self.doun_panel.get_width(), self.doun_panel.get_height())  # область для перетаскивания
        pygame.draw.rect(self.surface, (0, 0, 0), self.rect_ne_xodit, 1)  

        container_x = x_nash + 348
        container_y = y_nash + 12

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_buttons = pygame.mouse.get_pressed()

        rect = pygame.Rect(container_x + self.smena_x,container_y + self.smena_y,11,110)  # область для перетаскивания

        # начало перетаскивания
        if mouse_buttons[0]:
            if not self.dragging and rect.collidepoint(mouse_x, mouse_y):
                self.dragging = True
                self.drag_offset_x = mouse_x - (container_x + self.smena_x)

        # движение
        if self.dragging:
            self.smena_x = mouse_x - container_x - self.drag_offset_x
            self.smena_x = max( 0, min(self.smena_x, self.doun_peremushka.get_width() - 11))

        # окончание перетаскивания
        if not mouse_buttons[0]:
            self.dragging = False

        container = pygame.Surface((    self.doun_peremushka.get_width() -1,    self.doun_peremushka.get_height()),pygame.SRCALPHA)
        container.blit(self.doun_peremushka,(self.smena_x, self.smena_y))

        self.print_cards(container , self.smena_x, self.smena_y)
        self.timer_fight(self.surface , x_nash, y_nash)

        self.surface.blit(container,(container_x, container_y))

        self.container_x = container_x
        self.container_y = container_y
        

        self.mein_panel_doun_wepon(x_nash, y_nash)


    def print_cards(self, container , x_nash, y_nash):
        x_nash = x_nash + 15
        y_nash = y_nash + 5

        for id , card in enumerate(self.spisok_kart):
            self.spisok_vuvoda_cards.append({"card":card, "rect":card.ramka.get_rect() , "id": id})

        self.spisok_kart.clear()

        for card_info in self.spisok_vuvoda_cards:
            card = card_info["card"]
            rect = card_info["rect"]
            id_1 = card_info["id"]

            rect.topleft = (x_nash, y_nash)

            if self.hover_card != None and (self.hover_card[0] == card and self.hover_card[1] == id_1):
                pygame.draw.rect(container, (255, 255, 0), rect, 2)  # рисуем желтую рамку вокруг выбранной карты


            container.blit(card.ramka, rect)  
            container.blit(card.img, rect) 

            x_nash  += card.ramka.get_width() + 6  # отступ между картами



    def mein_panel_doun_wepon(self, x_nash, y_nash):
        x_nash = x_nash + 198
        y_nash = y_nash + 5

        if self.plear.current_weapons != []:
            sokr_wariant = self.plear.current_weapons[0]["weapon"].izb

            if len(self.plear.current_weapons) > 1:
                sokr_wariant2 = self.plear.current_weapons[1]["weapon"].izb

                width = sokr_wariant2.get_width()
                height = sokr_wariant2.get_height()

                big_image = pygame.transform.scale(sokr_wariant2, (width * 2, height * 2))

                if self.plear.current_weapons[0]["weapon"].two_handed == True:
                    
                    big_image.set_alpha(128)  # от 0 до 255
                    self.surface.blit(big_image, (x_nash + 70, y_nash))
                else:
                    self.surface.blit(big_image, (x_nash + 70, y_nash))


            width = sokr_wariant.get_width()
            height = sokr_wariant.get_height()

            big_image = pygame.transform.scale(sokr_wariant, (width * 2, height * 2))
            self.surface.blit(big_image, (x_nash, y_nash))


    def timer_fight(self , container, x_nash, y_nash):
        if self.start_batal == True:
            x_nash = x_nash + 1285
            y_nash = y_nash + 50

            timer_text = self.font3.render(f"{self.plear.xod_time}", True, (255, 255, 255))
            container.blit(timer_text, (x_nash, y_nash))

        pass

    def ui_logik(self, event):
        for card_info in self.spisok_vuvoda_cards:
            card = card_info["card"]
            rect = card_info["rect"]
            id_1 = card_info["id"]

            rect2 = rect.copy()  # создаем копию rect для использования в коллизии

            rect[0] += self.container_x #+ self.smena_x
            rect[1] += self.container_y #+ self.smena_y

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if rect.collidepoint(self.x_poz_maus, self.y_poz_maus):
                    self.hover_card = (card , id_1 )
                    self.plear.aktiw_cards = [card]
                    break


                else:
                    self.hover_card = None


            rect = rect2





        