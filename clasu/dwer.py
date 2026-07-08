from data.Maps.katra_tmx import *
from data.gaming_assets.dors.dors_zagruzka_izb import *

class Dweri:
    def __init__(self, x, y, closed_img, open_img):
        self.x = x
        self.y = y
        self.closed_img = closed_img
        self.open_img = open_img
        self.sprawka_text = [
        {"text":"Открыть","funk":"toggle_door",}
        ]
        self.xit_boks = pygame.Rect(x * 16, y * 16, 16, 16)
        self.is_open = False

    def image(self):
        return self.open_img if self.is_open else self.closed_img
    


    def toggle_door(self, atr_clas_spraw , plear = None):

        x, y = atr_clas_spraw
        x = int(x)
        y = int(y)

        if (x, y) not in doors:
            return

        door = doors[(x, y)]

        door.is_open = not door.is_open

        col_layer = tmx_map.get_layer_by_name("colision")

    
        try:
            if door.is_open:
                col_layer.data[y][x] = 0    
            else:
                col_layer.data[y][x] = 1    

        except TypeError:
            return

        print(f"Дверь ({x},{y}) теперь {'ОТКРЫТА' if door.is_open else 'ЗАКРЫТА'}")


    def draw_doors(self , surface , x , y , door):
        px = x * 16
        py = y * 16
        door.xit_boks.topleft = (px, py)
        pygame.draw.rect(surface, (255, 50, 75), door.xit_boks, 1)
        surface.blit(door.image(), (px, py))
        return x, y


def is_door(x, y):
    return (x, y) in doors


doors = {}

door = Dweri(4, 4, dwer_clos , dwer_open)
doors[(16, 19)] = door

