import pygame
from data.Maps.katra_tmx import *
from clasu.inwentori import *

from data.gaming_assets.chest.chest_load import *


class Sunduk:
    def __init__(self, x, y, closed_img, open_img, iaseka_inwentor=None ):
        self.x = x
        self.y = y
        self.closed_img = closed_img
        self.open_img = open_img
        self.is_open = False

        self.xit_boks = pygame.Rect(x * 16, y * 16, 32, 32)

        self.boks_inwentor = pygame.Rect((x - 1) * 16, (y - 1) * 16, 64, 64)
        self.iaseka_inwentor = iaseka_inwentor
        self.sprawka_text = [
            {"text": "Открыть", "funk": "toggle_sunduk"}
        ]

    def image(self):
        return self.open_img if self.is_open else self.closed_img

    def toggle_sunduk(self, atr_clas_spraw , plear = None):
        x, y = map(int, atr_clas_spraw)

        if (x, y) not in sunduki:
            return

        sunduk = sunduki[(x, y)]

        sunduk.is_open = not sunduk.is_open


    def draw(self, surface , x , y , door):
        px = x * 16
        py = y * 16
        door.xit_boks.topleft = (px, py)
        #pygame.draw.rect(surface, (255, 50, 75), door.xit_boks, 1)
        #pygame.draw.rect(surface, (255, 50, 75), door.boks_inwentor , 1)

        surface.blit(door.image(), (px, py))
        return x, y


    def colison_poaw(self):
        col_layer = tmx_map.get_layer_by_name("colision")

        try:
            col_layer.data[self.y][self.x] = 1   
            col_layer.data[self.y + 1][self.x] = 1 
            col_layer.data[self.y ][self.x + 1] = 1 
            col_layer.data[self.y + 1][self.x + 1] = 1 
        except TypeError:
            pass


sunduki = {}

sunduk = Sunduk( 4, 4, sunduk_zakr, sunduk_otkr, iaseka_inwentor = sudushka )

sunduk2 = Sunduk( 7 , 4, sunduk_zakr, sunduk_otkr, iaseka_inwentor = sudushka2 )

def is_sunduk(x, y):
    return (x, y) in sunduki

sunduki[(4, 4)] = sunduk
sunduki[(7 , 4)] = sunduk2