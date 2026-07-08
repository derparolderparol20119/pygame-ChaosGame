import pygame 
from funk.bar_poloski_spr import * 

from data.game_items.bags.bags_load import *


class Sumka:
    def __init__(self, name, tip, izb , izb_na_sheloweke , masa, ekwip_name, ekwip_name_na_shto , iaseka ):
        self.name = name
        self.tip = tip
        self.izb = izb
        self.izb_na_sheloweke = izb_na_sheloweke 
        self.masa = masa

        # куда и что
        self.ekwip_name = ekwip_name              # например: "bag"
        self.ekwip_name_na_shto = ekwip_name_na_shto  # например: "back"
        self.iaseka = iaseka

        self.sprawka_text = [
            {"text": "Надеть", "funk": "sprawka_nadet"},
            {"text": "Снять",  "funk": "sprawka_snat"},
            {"text":"Выбросить","funk":"vubrosit"}
        ]


    def eqwip(self, parts, poz_x_y , wuborka_ydal):
        slot = self._find_free_slot(parts)
        if not slot:
            return False

        slot["nadetost"] = self
        self.ybrat_iz_inwentor(parts, poz_x_y , wuborka_ydal)

        return True

    def _find_free_slot(self, parts):
        for part in parts.part:

            # проверка части тела
            if part.name != self.ekwip_name_na_shto:
                continue

            for slot in part.slotu_broni:

                # проверка типа слота
                if slot["ekwip_name"] != self.ekwip_name:
                    continue

                if slot["nadetost"] is None:
                    return slot

        return None


    def unequip(self, plear, poz):
        slot_snat = False

        for part in plear.part:
            for slot in part.slotu_broni:
                if slot["nadetost"] is self:
                    slot["nadetost"] = None
                    slot_snat = True

        if slot_snat:
            plear.dobawit_predmet(poz, self)
            plear.inwentor_add_iasheka_vse(self.iaseka , False)

        return slot_snat


    def ybrat_iz_inwentor(self, plear, poz , wuborka_ydal): # app_iaseki , sposob_yd_dob
        plear.delit_predmet_iz_inw(poz , wuborka_ydal)

        if self.iaseka:
            plear.inwentor_add_iasheka_vse(self.iaseka , True)


    def sprawka_nadet(self, parts, poz_x_y , wuborka_ydal):
        self.eqwip(parts, poz_x_y , wuborka_ydal)

    def sprawka_snat(self, parts, poz_x_y , wuborka_ydal):
        self.unequip(parts, poz_x_y)

    def vubrosit(self , plear , poz, wuborka_ydal):
        plear.wubrosit_iz_inwentar(poz , wuborka_ydal , self)

    def wuzow_sprawki(self, screen, x, y, font):
        x += 13
        y += 13

        # -------------------------
        # настройки сетки
        # -------------------------
        ICON_SIZE = 32
        COLS = 4
        MAX_ROWS = 10
        PADDING = 4

        items = self.iaseka.pridmetu if self.iaseka else []
        max_items = COLS * MAX_ROWS
        items = items[:max_items]

        rows = min(MAX_ROWS, (len(items) + COLS - 1) // COLS)

        grid_w = COLS * (ICON_SIZE + PADDING) - PADDING
        grid_h = rows * (ICON_SIZE + PADDING) - PADDING

        info_h = 90
        width = max(160, grid_w + 20)
        height = info_h + grid_h + 10

        # -------------------------
        # фон
        # -------------------------
        bg = pygame.Surface((width, height), pygame.SRCALPHA)
        pygame.draw.rect(bg, (35, 35, 35, 150), bg.get_rect())
        screen.blit(bg, (x, y))

        pygame.draw.rect(screen, (95, 95, 95), (x, y, width, height), 1)

        # -------------------------
        # текст
        # -------------------------
        screen.blit(font.render(self.name, True, (170, 190, 220)), (x + 5, y + 5))
        screen.blit(font.render(f"Тип: {self.ekwip_name}", True, (200, 200, 200)), (x + 5, y + 30))
        screen.blit(font.render(f"Куда: {self.ekwip_name_na_shto}", True, (200, 200, 200)), (x + 5, y + 50))
        screen.blit(font.render(f"Масса: {self.masa}", True, (200, 200, 200)), (x + 5, y + 70))

        # -------------------------
        # сетка предметов
        # -------------------------
        start_x = x + 10
        start_y = y + info_h

        for i, predmet in enumerate(items):
            col = i % COLS
            row = i // COLS

            px = start_x + col * (ICON_SIZE + PADDING)
            py = start_y + row * (ICON_SIZE + PADDING)

            # рамка
            pygame.draw.rect(
                screen,
                (70, 70, 70),
                (px, py, ICON_SIZE, ICON_SIZE),
                1
            )

            # иконка
            if predmet.izb:
                icon = pygame.transform.scale(predmet.izb, (ICON_SIZE, ICON_SIZE))
                screen.blit(icon, (px, py))




sumoska = Sumka(name = "бек_сумка", tip = "СУМКА", izb = sumka_v_inv , izb_na_sheloweke= sumka_v_pol,  masa = 15 , ekwip_name = "сумка", ekwip_name_na_shto = "торс" , iaseka = None )


