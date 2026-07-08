import pygame
from funk.bar_poloski_spr import *
from Screen_controller_funk_draw.ScreenController import *

from funk.get_bloked_dist_put import *

def clamp_to_range( dx, dy , range):
    dist_sq = dx * dx + dy * dy
    max_sq = range * range
    if dist_sq > max_sq:
        dist = dist_sq ** 0.5
        if dist != 0:
            scale = range / dist
            dx = int(dx * scale)
            dy = int(dy * scale)

    return dx, dy

def get_line(x0, y0, x1, y1):
    points = []

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1

    err = dx - dy

    while True:
        points.append((x0, y0))

        if x0 == x1 and y0 == y1:
            break

        e2 = err * 2

        if e2 > -dy:
            err -= dy
            x0 += sx

        if e2 < dx:
            err += dx
            y0 += sy

    return points


class Cards():
    def __init__(self , name , type , rang  , determining_rang , int_activeted_cards , coldung , img  , ramka , choice_target , method_damage_and_draw):
        self.name = name # имя 
        self.type = type # ето тип например ударная 
        self.rang = rang # ето ранг от1 до 13

        self.determining_rang = determining_rang # тип цвета карты 

        self.int_activeted_cards = int_activeted_cards # сколько карту можно применить до куладауна
        self.int_activeted_cards_max = int_activeted_cards # макс 
        self.coldung = coldung # кулдаун карты

        self.img = img 
        self.ramka = ramka

        self.choice_target = choice_target
        self.method_damage = method_damage_and_draw








class Choice_target_1():
    def __init__(self , range , cell_blow):
        self.range = range
        self.cell_blow = cell_blow
        
        self.ms_x = None
        self.ms_y = None

        self.target_dx = None
        self.target_dy = None

        self.draw_pos_x = 0   
        self.draw_pos_y = 0

        self.spisok_cell_atak = []
        self.cache_cells = None  # чтобы понимать, когда обновлять кеш

        self.cache_surface = None


    def risowka(self, start_x, start_y , surface , m_x, m_y , ):
        tile_size = 16
        self.ms_x, self.ms_y = m_x, m_y

        blocked_cache = load_blocked_tiles_from_tmx(tmx_map)


        # --- мышь -> клетка
        grid_x = int(self.ms_x // tile_size)
        grid_y = int(self.ms_y // tile_size)

        player_x = start_x
        player_y = start_y

        dx = grid_x - player_x
        dy = grid_y - player_y

        self.target_dx = dx
        self.target_dy = dy

        dx, dy = clamp_to_range(dx, dy , self.range)

        last_x = player_x
        last_y = player_y
        
        for x, y in get_line(
            player_x,
            player_y,
            player_x + dx,
            player_y + dy
        ):
            if (x, y) in blocked_cache:
                break
            
            last_x = x
            last_y = y
        
        dx = last_x - player_x
        dy = last_y - player_y

        self.target_dx = dx
        self.target_dy = dy

        offset = (self.range + 1) * tile_size

        # ✅ позиция отрисовки СРАЗУ считаем
        self.draw_pos_x = player_x * tile_size - offset
        self.draw_pos_y = player_y * tile_size - offset

        # --- обновление кеша
        if self.cache_cells != (grid_x, grid_y):
            self.spisok_cell_atak = []
            self.cache_cells = (grid_x, grid_y)

            size = tile_size * (self.range * 2 + 3)
            self.cache_surface = pygame.Surface((size, size), pygame.SRCALPHA)

            # --- рисуем фигуру удара
            for cx, cy in self.cell_blow:
                tx = cx + dx
                ty = cy + dy

                if tx * tx + ty * ty > self.range * self.range:
                    continue

                world_x = player_x + tx
                world_y = player_y + ty

                if self.is_blocked(player_x, player_y, world_x, world_y, blocked_cache):
                    continue

                draw_x = offset + tx * tile_size
                draw_y = offset + ty * tile_size

                # rect ВНУТРИ surface
                local_rect = pygame.Rect(draw_x, draw_y, tile_size, tile_size)

                # 🔥 переводим в МИРОВЫЕ координаты
                world_rect = local_rect.move(self.draw_pos_x, self.draw_pos_y)

                self.spisok_cell_atak.append(world_rect)

                # рисуем
                pygame.draw.rect(
                    self.cache_surface,
                    (255, 0, 0, 120),
                    local_rect
                )

            # --- линия
            start_px = offset + tile_size // 2
            start_py = offset + tile_size // 2

            end_px = offset + dx * tile_size + tile_size // 2
            end_py = offset + dy * tile_size + tile_size // 2



            pygame.draw.line(
                self.cache_surface,
                (255, 255, 0, 180),
                (start_px, start_py),
                (end_px, end_py),
                3
            )


    def is_blocked(self, start_x, start_y, end_x, end_y, blocked_cache):

        for x, y in get_line(start_x, start_y, end_x, end_y):

            if (x, y) == (start_x, start_y):
                continue

            if (x, y) in blocked_cache:
                return True

        return False




class Method_damage_and_draw():
    def __init__(self , animation, time_animation, range , ostatki_na_zemle , frame_ostatki_na_zemle , smesh_lishnoe_x , smesh_lishnoe_y , duration_atak , range_px , hold):
        self.animation = animation
        self.animation_tekush = 0
    
        self.time_anim = time_animation
        self.time_anim_tekush = 0
        
        self.range = range

        self.cache_surface_anima = pygame.Surface(
                    (self.animation[0].get_width(), self.animation[0].get_height()),
                    pygame.SRCALPHA)
        


        self.draw_x2 = 0
        self.draw_y2 = 0


        self.atak_committed = False

        self.ostatki_na_zemle = ostatki_na_zemle

        self.frame_ostatki_na_zemle = frame_ostatki_na_zemle #меньше -2 но не больше длинны self.animation 

        self.smesh_lishnoe_x = smesh_lishnoe_x
        self.smesh_lishnoe_y = smesh_lishnoe_y


        self.duration_atak = duration_atak
        self.range_px = range_px
        self.hold = hold


    def animeishon_cards(self , dt , draw_pos_x, draw_pos_y , target_dx , target_dy , m_x, m_y):
        if not self.animation:
            return

        # --- таймер
        self.time_anim_tekush += dt

        if self.time_anim_tekush >= self.time_anim:
            self.time_anim_tekush = 0
            self.animation_tekush += 1

            if self.animation_tekush >= len(self.animation):
                self.animation_tekush = 0

        frame = self.animation[self.animation_tekush] 

        tile_size = 16
        offset = (self.range + 1) * tile_size

        # 🔥 ВОТ ЗДЕСЬ clamp
        dx, dy = clamp_to_range(target_dx, target_dy, self.range)

        # 🔥 центр удара
        center_x = offset + dx * tile_size + tile_size // 2
        center_y = offset + dy * tile_size + tile_size // 2

        # --- мировые координаты
        self.draw_x2 = draw_pos_x + center_x - frame.get_width() // 2
        self.draw_y2 = draw_pos_y + center_y - frame.get_height() // 2
    
        self.draw_x2 -= self.smesh_lishnoe_x * tile_size
        self.draw_y2 -= self.smesh_lishnoe_y * tile_size

        self.cache_surface_anima.fill((0, 0, 0, 0))
        self.cache_surface_anima.blit(frame, (0, 0))

        if self.animation_tekush >= len(self.animation) - 1:
            self.animation_tekush = 0
            self.cache_surface_anima.fill((0, 0, 0, 0))
            self.atak_committed = False
            return True
        
        else:
            return False


    def damage_get(self , choice , context , npc):
        source_x = choice.spisok_cell_atak[0].x // 16
        source_y = choice.spisok_cell_atak[0].y // 16

        npc.apply_recoil_from_point(
            source_x,
            source_y,
            duration=self.duration_atak,
            range_px=self.range_px,
            hold=self.hold
        )





#class DamageCardsHausite():
#    def __init__(self, animation, time_animation, range, cell_blow , smesh_lishnoe_x = 0 , smesh_lishnoe_y = 0 , ostatki_na_zemle = None , poaw_ostatki_na_zemle = -2 , duration_atak = 40 , range_px = 5 , hold = 20 ):
#        self.animation = animation
#        self.animation_tekush = 0
#
#        self.time_anim = time_animation
#        self.time_anim_tekush = 0
#        
#        self.range = range
#        self.cell_blow = cell_blow
#
#        self.cache_surface = None
#
#        self.cache_surface_anima = pygame.Surface(
#            (self.animation[0].get_width(), self.animation[0].get_height()),
#            pygame.SRCALPHA
#        )
#
#        self.cache_cells = None  # чтобы понимать, когда обновлять кеш
#
#        self.draw_pos_x = 0
#        self.draw_pos_y = 0
#
#        self.spisok_cell_atak = []
#
#        self.target_dx = 0
#        self.target_dy = 0
#
#        self.draw_x2 = 0
#        self.draw_y2 = 0 
#
#        self.smesh_lishnoe_x = smesh_lishnoe_x
#        self.smesh_lishnoe_y = smesh_lishnoe_y
#        self.ostatki_na_zemle = ostatki_na_zemle
#
#        self.poaw_ostatki_na_zemle = poaw_ostatki_na_zemle #меньше -2 но не больше длинны self.animation 
#        self.atak_committed = False
#
#        self.duration_atak = duration_atak
#        self.range_px = range_px
#        self.hold = hold
#
#



