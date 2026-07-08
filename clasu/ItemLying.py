import pygame
from config.config import *


class ItemLying():
    def __init__(self, x, y, image, prudmet , rotate=0 ):
        self.image_original = image
        self.prudmet = prudmet
        self.image = pygame.transform.rotate(self.image_original, rotate)

        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)
        self.podswetka = False
        self.sprawka_text = [
            {"text": "Подобрать", "funk": "podobrat"},
        ]



    def draw_outline(self, surface, color=(235, 235, 235)):
        outline = self.mask.outline()
        if len(outline) > 1:
            for i in range(len(outline)):
                x1, y1 = outline[i]
                x2, y2 = outline[(i + 1) % len(outline)]
                pygame.draw.line(
                    surface,
                    color,
                    (x1 + self.rect.x, y1 + self.rect.y),
                    (x2 + self.rect.x, y2 + self.rect.y),
                    1
                )

        glow = self.mask.to_surface(setcolor=color, unsetcolor=(0, 0, 0))
        glow.set_colorkey((0, 0, 0))
        glow.set_alpha(60)
        surface.blit(glow, self.rect)


    def check_click(self, mouse_pos):
        mx, my = mouse_pos
        x = mx - self.rect.x
        y = my - self.rect.y

        if 0 <= x < self.rect.width and 0 <= y < self.rect.height:
            return self.mask.get_at((x, y))
        return False
    
    def podobrat(self , nps):
        nps.dobawit_predmet( 1 , self.prudmet , None)
        self.prudmet = None

    def ybrat_iz_spiskow(self , list = [igrowoe_okrugenie_personag , predmetu_leg] ):
        for lst in list:
            if self in lst:
                lst.remove(self)


    def draw(self, skrean , a ,b , c ):
        skrean.blit(self.image, self.rect)

        if hasattr(self, "podswetka") and self.podswetka:
            self.draw_outline(skrean)

        if self.prudmet is None:
            self.ybrat_iz_spiskow()