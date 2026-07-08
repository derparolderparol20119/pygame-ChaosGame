import pygame
import sys
from random import *
import math
from pytmx import load_pygame
from copy import deepcopy

from Screen_controller_funk_draw.ScreenController import *
from funk.a_star_idti_k_celi import *
from clasu.telo import *
from random import *
from clasu.ItemLying import *
from config.config import *
from config.text import *
from clasu.parameters import *
from clasu.skils import *
from funk.get_bloked_dist_put import *
from clasu.character_parameters import *

from data.game_items.living_creatures.liwing_creatures import *
from data.game_items.coat_of_arms_gerbs.loadind_gerb import *
from clasu.get_hit import *

from templat_factory.limb_templates import *
from slice_spritesheet.slice_spritesheet import *
# изправить ходьб время

class Vse_personagu():
    def __init__(self, x, y, izb , izb_morg , perw_sumka , name = "solider" , trup = trup_izb , shadow = shadows_izb , ikn_mordu = ikn_mordu , color_gerb = brown_wht_st_a_color_gerb , stroke_gerb = none_stroke_gerb ):
        self.name = name
        self.zanat_kletka = (x , y)
        self.aktiv_unit = False
        self.in_battle = False

        self.team = None # tests

        # -------------------- cards --------------------
        self.aktiwator = [] # tests
        self.aktiw_cards = None
        self.aktiWnost_kartu = False
        self.aktiw_animeshon = False
        # -------------------- cards finish --------------------

        self.meim_spels = [] # tests

        self.trup = trup

        self.move_area_timer = 0
        self.move_area_delay = 90  # миллисекунды задержки
        self.move_area_ready = False

        self.x = x  
        self.y = y
        self.izb = izb 
        self.direction = "right"
        self.shadow = shadow

        self.attack_range_surface = None
        self.attack_range_offset = None


        self.izb_morg = izb_morg
        self.ikn_mordu  = ikn_mordu # лицо

        self.part = None
        self.path = None

        self.inwentor = None
        self.iaseki = [perw_sumka ]

        self.sprawka_text = [
        {"text":"Параметры","funk":"sprawka",},
        {"text":"ударить раб. не кор.","funk":"hit"}
        ]

        self.plita = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\gaming_assets\Ui_elements\plit_sheet.png').convert_alpha()
        self.plita_wsatu = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\gaming_assets\Ui_elements\plit_wstatu.png').convert_alpha()
        self.plita_frames = def_slice_spritesheet(self.plita, 16, 16 )
        self.frame_index = 0
        self.frame_timer = 0
        self.frame_speed = 0.2



        self.image_rect = self.izb.get_rect()
        self.xit_boks = pygame.Rect(0, 0, 16, 16)
        self.feet_rect = pygame.Rect(0, 0, 10, 4)
        self.image_offset = pygame.Vector2(0, 0)
        
        self.idle_phase = 0.0
        self.idle_speed = 0.032   # медленно
        self.idle_amplitude = 1

        self.hit_flash_time = 0.0
        self.hit_flash_duration = 80  # мс (Stone Shard примерно так)
        self.hit_flash_surface = None

        self.random_time_morg = 0 
        self.time_morg = randint(500 , 650)

        self.tek_kadr = 0
        self.tek_time = 0
  
        self.melee_weapons = True

        self.two_handed = False

        self.attack_state = None   
        self.recoil_state = None   
        self.attack_offset = pygame.Vector2(0, 0)   
        self.recoil_offset = pygame.Vector2(0, 0)   
        self.visual_offset_right = pygame.Vector2(+4, +3)  # пример
        self.visual_offset_left  = pygame.Vector2(-3, +3)

        self.unit_attack_range = []
        self.variable_draw_attack_range = False

        self.color_gerb = color_gerb
        self.stroke_gerb = stroke_gerb

        self.podswetka = (False , (0 , 0 , 0))

        self.kesh_poz = None
        self.kesh_cell = None

        self.char_surf = None
        self.render_layer_static = None



        self.plit_leng = []

        self.operations = {
            "+": lambda a, b: a + b,
            "-": lambda a, b: a - b,
            "*": lambda a, b: a * b,
            "/": lambda a, b: a / b,
            "//":lambda a, b: a // b,
        }



        # -------------------------- hero's body parameters --------------------------
        self.bload = 5000
        self.bload_max = self.bload

        self.mein_range = 3
        self.weapons_range = 0

        self.parameter_list = []
        self.sklil_list = []

        self.current_weapons = []


        self.iniciatiw = randint(15 , 30) # tests
        self.bar_iniciatiw = 0 # tests
        self.max_iniciatiw = 100 # tests

        self.xod_time = 6 # tests
        self.xod_time_max = self.xod_time  

        self.main_system_hero = {
            "time_movement":30,
            "time_movement_max":30,

            "spead_moving":5,

            "spead_moving_max":24,
            "spead_moving_min":1,

            "reaction":0,
            "razum":0,

            "lungs":0,
            "cerdce":0,
            "blood_purification":0,

            "efectiuw_torso":0,

            "efectiuw_praw_ruka":0,
            "efectiuw_lew_ruka":0,

            "carry_weight":0,
            "carry_weight_max":10,

            "efectiuw_lew_leg":0,
            "efectiuw_praw_leg":0,
        }

        self.main_system_hero_copy = self.main_system_hero


        self.pain = 0
        pain_states = {
            "small":  { "min": 10, "effects": [] },
            "medium": { "min": 30, "effects": [] },
            "high":   { "min": 60, "effects": [] },
            "shock":  { "min": 85, "effects": [] }
        }

        self.ranu_tela = [] # их можно лечить ето дебафы типа кровотечение боль 

        self.death = False
        self.van = None

        # ---------------------------------------------------------------------------



    def update_rects(self):
        px = self.x * 16
        py = self.y * 16
        self.xit_boks.midbottom = (px + 8, py + 16)
        self.feet_rect.midbottom = self.xit_boks.midbottom
        self.image_rect.midbottom = (self.feet_rect.midbottom[0] , self.feet_rect.midbottom[1] + self.image_offset.y)

        px2 = (self.x - self.mein_range) * 16
        py2 = (self.y - self.mein_range) * 16

        self.image_rect = self.izb.get_rect()
        self.image_rect.midbottom = self.feet_rect.midbottom


    def draw(self, surface , dt , world_move , controller):
        self.otobrogenie(surface , dt , world_move , controller)

    def otobrogenie(self, surface, dt, world_move, controller):

        if self.death:
            surface.blit(self.trup, (self.image_rect.x, self.image_rect.y))
            return

        self.update_rects()

        if self.variable_draw_attack_range:
            self.draw_attack_range(surface)

        # =====================================================
        # СОЗДАЁМ / КЕШИРУЕМ SURFACE ТОЛЬКО 1 РАЗ
        # =====================================================

        surf_size = (self.image_rect.width + 8, self.image_rect.height + 8)

        if self.char_surf is None or self.char_surf.get_size() != surf_size:
            self.char_surf = pygame.Surface(surf_size, pygame.SRCALPHA)

        if self.render_layer_static is None or self.render_layer_static.get_size() != surf_size:
            self.render_layer_static = pygame.Surface(surf_size, pygame.SRCALPHA)

        # очищаем кешированные поверхности
        self.char_surf.fill((0, 0, 0, 0))
        self.render_layer_static.fill((0, 0, 0, 0))

        # =====================================================
        # OFFSETS / АНИМАЦИЯ
        # =====================================================
        offset_x = 0.0
        offset_y = 0.0
        offset_x_shad = 0.0
        offset_y_shad = 0.0

        if not self.path or world_move == False:
            self.idle_phase += self.idle_speed * dt
            sway = math.sin(self.idle_phase)

            offset_x = sway * self.idle_amplitude
            offset_y = abs(sway) * 1.2

        total_offset = pygame.Vector2(offset_x, offset_y)
        total_offset_shadow = pygame.Vector2(offset_x_shad, offset_y_shad)

        if self.attack_state:
            total_offset += self.attack_offset
            total_offset_shadow += self.attack_offset

        if self.recoil_state:
            total_offset += self.recoil_offset
            total_offset_shadow += self.recoil_offset

        offset_x = total_offset.x
        offset_y = total_offset.y

        # =====================================================
        # МОРГАНИЕ
        # =====================================================
        self.tek_time += dt

        if self.tek_kadr == 0:
            if self.tek_time > self.time_morg + self.random_time_morg:
                self.tek_time = 0
                self.tek_kadr = (self.tek_kadr + 1) % len(self.izb_morg)
                self.random_time_morg = randint(50, 150)
        else:
            if self.tek_time > 19:
                self.tek_time = 0
                self.tek_kadr = (self.tek_kadr + 1) % len(self.izb_morg)

        # =====================================================
        # SHADOW
        # =====================================================
        surface.blit(
            self.shadow,
            (
                (self.image_rect.x ) + total_offset_shadow.x * 0.9,
                (self.image_rect.y ) + total_offset_shadow.y * 0.9
            )
        )

        # =====================================================
        # STATIC LAYER (БЕЗ ЭФФЕКТОВ / БЕЗ ДВИЖЕНИЯ)
        # =====================================================
        self.otrisowka_tela_sbarag(self.render_layer_static, 0, 0)
        self.anim_wepon(self.render_layer_static)

        # =====================================================
        # MAIN CHAR SURF (С ЭФФЕКТАМИ / С ДВИЖЕНИЕМ)
        # =====================================================
        self.otrisowka_tela_sbarag(self.char_surf, 0, 0)

        if self.podswetka[0]:
            self.draw_outline(
                self.char_surf,
                (0, 0),
                self.podswetka[1],
                self.podswetka[2]
            )

        self.anim_wepon(self.char_surf)

        self.flesh_tela(self.char_surf, dt)

        # =====================================================
        # FLIP
        # =====================================================
        draw_surf = self.char_surf

        if self.direction == "left":
            draw_surf = pygame.transform.flip(draw_surf, True, False)

        # =====================================================
        # DRAW RECT
        # =====================================================
        if self.direction == "left":
            vo = self.visual_offset_left
        else:
            vo = self.visual_offset_right

        draw_rect = draw_surf.get_rect(
            center=(
                self.image_rect.centerx + total_offset.x + vo.x,
                self.image_rect.centery + total_offset.y + vo.y
            )
        )

        surface.blit(draw_surf, draw_rect)

        # =====================================================
        # ПРОЧЕЕ
        # =====================================================
        m_x5, m_y5 = pygame.mouse.get_pos()
        m_x, m_y = controller.screen_to_world(m_x5, m_y5)

        self.turn_attacking(surface, m_x, m_y, draw_rect)

        self.draw_cell_xotbi(surface)

        self.card_application(surface, dt , m_x, m_y)


    def otrisowka_tela_sbarag(self, surface, x, y):

        vse_sloi = []  # сюда собираем всё что нужно нарисовать
        two_handed = getattr(self, "two_handed", False)

        for osn in self.part:  
            for kon in osn.koneshonsti:

                telo_draw = kon.draw_lear_telo

                if two_handed and hasattr(kon, "izb_tip_b") and kon.izb_tip_b:
                    telo_img = kon.izb_tip_b
                else:
                    telo_img = kon.izb

                if kon.name == "челюсть":
                    telo_img = self.izb_morg[self.tek_kadr]

                if telo_img:
                    vse_sloi.append((telo_draw, telo_img))



                for slot in kon.slots_ekwip:

                    nadet = slot.get("nadetost")
                    slot_draw = slot.get("draw_lear", 0)

                    if nadet is None:
                        continue

                    final_draw = telo_draw + slot_draw


                    if hasattr(nadet, "spisok_shastei_broni"):

                        for elem in nadet.spisok_shastei_broni:

                            if elem.ekwip_name_na_shto != kon.name:
                                continue

                            if two_handed and elem.izb_two_hend:
                                img = elem.izb_two_hend
                            else:
                                img = elem.izb

                            if img:
                                vse_sloi.append((final_draw, img))


                    else:
                        if two_handed and hasattr(nadet, "izb_na_sheloweke_two_handed"):
                            img = nadet.izb_na_sheloweke_two_handed
                        else:
                            img = getattr(nadet, "izb_na_sheloweke", None)

                        if img:
                            vse_sloi.append((final_draw, img))


        vse_sloi.sort(key=lambda elem: elem[0])


        for _, img in vse_sloi:
            surface.blit(img, (x, y))


    def draw_cell_xotbi(self, surface):

        if self.path:
            self.plit_leng = []
            prev = (self.x, self.y)
            frame_count = len(self.plita_frames)

            if self.in_battle == True:
                max_steps = min(self.xod_time // self.main_system_hero["spead_moving"], len(self.path))
                limited_path = self.path[:int(max_steps)]

                for (cx, cy) in limited_path:
                    offset = (cx + cy) % frame_count
                    frame = self.plita_frames[(self.frame_index + offset) % frame_count]


                    self.plit_leng.append({
                        "frame":frame,
                        "cx":cx * 16,
                        "cy":cy * 16
                    })

                    dx = cx - prev[0]
                    dy = cy - prev[1]

                    if dx != 0 and dy != 0:
                        mid_x = prev[0] * 16 + dx * 8
                        mid_y = prev[1] * 16 + dy * 8


                        self.plit_leng.append({
                            "frame":frame,
                            "cx":mid_x,
                            "cy":mid_y
                        })

                    prev = (cx, cy)

                if limited_path:
                    last_x, last_y = limited_path[-1]
                    surface.blit(self.plita_wsatu, (last_x * 16, last_y * 16))

            else:
                for (cx, cy) in self.path:
                    offset = (cx + cy) % frame_count
                    frame = self.plita_frames[(self.frame_index + offset) % frame_count]


                    self.plit_leng.append({
                        "frame":frame,
                        "cx":cx * 16,
                        "cy":cy * 16
                    })

                    dx = cx - prev[0]
                    dy = cy - prev[1]

                    if dx != 0 and dy != 0:
                        mid_x = prev[0] * 16 + dx * 8
                        mid_y = prev[1] * 16 + dy * 8


                        self.plit_leng.append({
                            "frame":frame,
                            "cx":mid_x,
                            "cy":mid_y
                        })                        

                    prev = (cx, cy)

                if self.path:
                    last_x, last_y = self.path[-1]
                    surface.blit(self.plita_wsatu, (last_x * 16, last_y * 16))
                    
        else:
            self.plit_leng = []


    def flesh_tela(self ,  char_surf , dt):
        if self.hit_flash_time > 0:
            t = self.hit_flash_time / self.hit_flash_duration
            t = math.sin(t * math.pi * 0.5)
            alpha = int(255 * t)

            flash = char_surf.copy()
            flash.fill((255, 255, 255), special_flags=pygame.BLEND_RGB_ADD)
            flash.set_alpha(alpha)

            char_surf.blit(flash, (0, 0))

            self.hit_flash_time -= dt
            if self.hit_flash_time < 0:
                self.hit_flash_time = 0


    def anim_wepon(self , char_surf):
        if self.attack_state:
            st = self.attack_state
            weapon = self.current_weapons[0]['weapon'] if self.current_weapons else None
        
            if weapon:
                anim_type = st.get("anim_type")
                frame = st.get("frame_index", 0)
                flip_x = st.get("flip_x", False)
                flip_y = st.get("flip_y", False)
        
                if anim_type in weapon.animations:
                    frames = weapon.animations[anim_type]
        
                    if frame < len(frames):
                        img = frames[frame]
        
                        img = pygame.transform.flip(img, flip_x, flip_y)
        
                        dir_vec = st["dir"]
                        push = dir_vec * 16  # или 20

                        cx = self.image_rect.width // 2 + push.x
                        cy = self.image_rect.height // 2 + push.y

                        char_surf.blit(
                            img,
                            (cx - img.get_width() // 2,
                             cy - img.get_height() // 2)
                        )




    def blokirowka_prosm(self, x, y):
        if x < 0 or y < 0 or x >= tmx_map.width or y >= tmx_map.height:
            return True  # считаем за стену, чтобы A* не выходил за карту

        for layer in tmx_map.visible_layers:
            if layer.name == "colision":         
                gid = layer.data[y][x]           
                if gid != 0:                     
                    return True
        return False
      

    def idti_k(self, px, py, players, pretendeimue_kletki, ready_way=False):
        if self.in_battle == True:
            if self.aktiv_unit == True:
                pass
            else:
                return


        if ready_way == False:
            tx = int(px / 16)
            ty = int(py / 16)

        else:
            tx = px 
            ty = py

        start = (self.x, self.y)
        goal = (tx, ty)

        players_set = set(players)
        pretend_set = set(pretendeimue_kletki)



        def is_blocked_path(x, y):
            # для ПРОХОДА
            if (x, y) in players_set:
                return True
            return self.blokirowka_prosm(x, y)


        def is_blocked_goal(x, y):
            # для КОНЕЧНОЙ точки
            if (x, y) in players_set:
                return True
            if (x, y) in pretend_set:
                return True
            return self.blokirowka_prosm(x, y)


        if is_blocked_goal(tx, ty):
            goal = get_nearest_walkable(goal, is_blocked_goal)

        # поиск пути

        path = a_star(start, goal, is_blocked_path)

        self.path = path if path else []


    def dwigenie_po_pathu(self):
        # нет пути — нечего делать
        if not self.path:
            return
    
        # ❌ НЕТ очков хода — СТОП
        if self.in_battle == True:

            if self.xod_time <= 0 or  self.xod_time < self.main_system_hero["spead_moving"]:
                self.path = []      # можно очистить путь
                return
    
        nx, ny = self.path[0]
        dx = nx - self.x
        dy = ny - self.y
        
        # меняем направление ТОЛЬКО по горизонтали
        if dx > 0:
            self.direction = "right"
        elif dx < 0:
            self.direction = "left"
        # если вверх/вниз — direction не трогаем
    
        # ❌ если путь заблокирован
        if self.blokirowka_prosm(nx, ny):
            self.path = []
            return
    
        # ✅ ШАГ
        self.x = nx
        self.y = ny
        self.path.pop(0)
    
        # ❗ ТРАТИМ очко хода ТОЛЬКО ЗДЕСЬ
        #print( "время хода" ,self.xod_time ,  "стоимость хода" , self.zaderzka_moving)
        if self.in_battle == True:
            self.xod_time -= self.main_system_hero["spead_moving"]
            


    def apdete(self, dt):
        self._update_attack_and_recoil(dt)
        self.update_cell_path(dt)
        masy_timov = self.main_system_hero["time_movement"]
        masy_timov_max = self.main_system_hero["time_movement_max"]
    
        if self.path:
            if masy_timov > 0:
                masy_timov -= dt
            else:
                masy_timov = masy_timov_max
                self.dwigenie_po_pathu()
        else:
            masy_timov = masy_timov_max
        
        if self.path == [] or self.path == None:
            if self.zanat_kletka != (self.x , self.y):
                self.zanat_kletka = (self.x , self.y)
            
        if self.aktiv_unit:
            self.move_area_timer += dt
            if self.move_area_timer >= self.move_area_delay:
                self.move_area_ready = True

        else:
            self.move_area_timer = 0
            self.move_area_ready = False

        self.main_system_hero["time_movement"] = masy_timov


    def sozdan_tel(self): 
        torso_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"броне жылет" , "sloi":4 , "nadetost":None , "draw_lear":20},
                {"ekwip_name":"сумка" , "sloi":5 , "nadetost":None , "draw_lear":25}]

        torso_slots_niz = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"броне жылет" , "sloi":4 , "nadetost":None , "draw_lear":20},
                            {"ekwip_name":"пояс" , "sloi":5 , "nadetost":None , "draw_lear":25} , {"ekwip_name":"фолды" , "sloi":3 , "nadetost":None , "draw_lear":14} ]

        


        head_slots = [{"ekwip_name":"подшлемник" , "sloi":1 , "nadetost":None , "draw_lear":5} , {"ekwip_name":"шлем" , "sloi":2 , "nadetost":None , "draw_lear":10} ,
                      {"ekwip_name":"забрало" , "sloi":3 , "nadetost":None , "draw_lear":15} ]

        shea_slots = [{"ekwip_name":"горжет" , "sloi":1 , "nadetost":None , "draw_lear":5} , {"ekwip_name":"шарф" , "sloi":2 , "nadetost":None , "draw_lear":10} ]



        plesho_praw_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"наплечник" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        pred_plesho_praw_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"наручи" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        kist_praw_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                    {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"перчатки" , "sloi":4 , "nadetost":None , "draw_lear":20} ,
                    {"ekwip_name":"оружые" , "sloi":1 , "nadetost":None , "draw_lear":-1}]



        plesho_lewoe_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                    {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"наплечник" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]


        pred_plesho_lewoe_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"наручи" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        kist_lewoe_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                    {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"перчатки" , "sloi":4 , "nadetost":None , "draw_lear":20} ,
                    {"ekwip_name":"оружые" , "sloi":1 , "nadetost":None , "draw_lear":-1}]


        bedro_praw_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                    {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"набедренники" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        golen_praw_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"поножи" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        golen_praw_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"поножи" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        stopa_praw_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"ботинки" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]


        bedro_lewoe_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
                {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"набедренники" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        golen_lewoe_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"поножи" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        golen_lewoe_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"поножи" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        stopa_lewoe_slots = [{"ekwip_name":"нижний слой" , "sloi":1 , "nadetost":None , "draw_lear":5}, {"ekwip_name":"средний слой" , "sloi":2 , "nadetost":None , "draw_lear":10} , 
            {"ekwip_name":"верхний слой" , "sloi":3 , "nadetost":None , "draw_lear":15} ,{"ekwip_name":"ботинки" , "sloi":4 , "nadetost":None , "draw_lear":20} ,]

        # ---------------- ГОЛОВА ----------------
        data_liambs_shea = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "шея",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(105, 76, 15, 15),
            "fabric_depth": 10,
            "parent": None,
            "draw_lear_telo": 1,
            "slots_ekwip": shea_slots,
            "izb": None,
            "izb_tip_b": None,
        }
        shea = Limb(**data_liambs_shea)


        data_liambs_shelust = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "челюсть",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(100, 63, 25, 15),
            "fabric_depth": 10,
            "parent": shea,
            "draw_lear_telo": 1,
            "slots_ekwip": head_slots,
            "izb": shelust_izb,
            "izb_tip_b": None,
        }
        shelust = Limb(**data_liambs_shelust)


        data_liambs_lob = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "лоб",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(100, 50, 25, 15),
            "fabric_depth": 23,
            "parent": shelust,
            "draw_lear_telo": 2,
            "slots_ekwip": head_slots,
            "izb": lob_izb,
            "izb_tip_b": None,
        }
        lob = Limb(**data_liambs_lob)

        
        razum = Influence_parameters(
            name= "разум",
            meaning=100,
            vliaet_na_shto="razum",
            znak= "+"
        )

        reaction = Influence_parameters(
            name= "реакцыя",
            meaning=100,
            vliaet_na_shto="reaction",
            znak= "+"
        )


        golowa = Osnowa("голова", [shea, lob, shelust], 15, 15 , 
                        influence_attributes_list = [razum , reaction] , parametrs = [stoikost])



        # ---------------- ТОРС ----------------
        data_liambs_verx_tors = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "верх торса",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(90, 89, 45, 30),
            "fabric_depth": 25,
            "parent": None,
            "draw_lear_telo": 1,
            "izb": verx_torsa_izb,
            "slots_ekwip": torso_slots,
        }
        verx_tors = Limb(**data_liambs_verx_tors)

        data_liambs_niz_tors = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "низ торса",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(93, 118, 40, 30),
            "fabric_depth": 25,
            "parent": verx_tors,
            "draw_lear_telo": 1,
            "izb": niz_torsa_izb,
            "slots_ekwip": torso_slots_niz,
        }
        niz_tors = Limb(**data_liambs_niz_tors)

        data_liambs_rebra = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "ребра",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(97, 89, 31, 35),
            "fabric_depth": 7,
            "parent": verx_tors,
        }
        rebra = Limb(**data_liambs_rebra)

        breath2 = Influence_parameters(
            name= "легкое левое",
            meaning=50,
            vliaet_na_shto="lungs",
            znak= "+"
        )
        data_liambs_legkoe_lew = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "легкое левое",
            "tip": "tkani",
            "glubina": 2,
            "bodi_rekt": pygame.Rect(100, 90, 9, 22),
            "parent": rebra,
            "influence":breath2 
        }
        legkoe_lew = Limb(**data_liambs_legkoe_lew)



        breath1 = Influence_parameters(
            name= "легкое правое",
            meaning=50
            ,
            vliaet_na_shto="lungs",
            znak= "+"
        )
        data_liambs_legkoe_praw = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "легкое правое",
            "tip": "tkani",
            "glubina": 2,
            "bodi_rekt": pygame.Rect(116, 90, 9, 22),
            "parent": rebra,
            "influence":breath1,
            
        }
        legkoe_praw = Limb(**data_liambs_legkoe_praw)


        
        cerdce1 = Influence_parameters(
            name= "сердце",
            meaning=100,
            vliaet_na_shto="cerdce",
            znak= "+"
        )
        data_liambs_cerdce = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "сердце",
            "tip": "tkani",
            "glubina": 2,
            "bodi_rekt": pygame.Rect(109, 94, 8, 11),
            "parent": rebra,
            "influence":cerdce1
        }
        cerdce = Limb(**data_liambs_cerdce)

        data_liambs_peshen = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "печень",
            "tip": "tkani",
            "glubina": 2,
            "bodi_rekt": pygame.Rect(97, 120, 20, 11),
            "parent": niz_tors,
        }
        peshen = Limb(**data_liambs_peshen)


             
        poska_lew1 = Influence_parameters(
            name= "почка левая",
            meaning=50,
            vliaet_na_shto="blood_purification",
            znak= "+"
        )
        data_liambs_poska_lew = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "почка левая",
            "tip": "tkani",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(97, 130, 7, 11),
            "parent": niz_tors,
            "influence":poska_lew1
        }
        poska_lew = Limb(**data_liambs_poska_lew)


        poska_prw2 = Influence_parameters(
            name= "почка правая",
            meaning=50,
            vliaet_na_shto="blood_purification",
            znak= "+"
        )
        data_liambs_poska_praw = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "почка правая",
            "tip": "tkani",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(120, 130, 7, 11),
            "parent": niz_tors,
            "influence":poska_prw2
        }
        poska_praw = Limb(**data_liambs_poska_praw)



        efectiuw_torso2 = Influence_parameters(
            name= "ефективвность торса",
            meaning=100,
            vliaet_na_shto="efectiuw_torso",
            znak= "+"
        )

        torso = Osnowa("торс", [verx_tors, niz_tors, rebra, legkoe_lew, legkoe_praw, cerdce, peshen, poska_lew, poska_praw], 15, 15 , 
                       influence_attributes_list = [efectiuw_torso2] , parametrs = [stoikost])



        # ---------------- ПРАВАЯ РУКА ----------------
        data_liambs_plesho_praw = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "плечо правое",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(79, 89, 10, 35),
            "fabric_depth": 10,
            "parent": None,
            "draw_lear_telo": 25,
            "izb": plesho_praw_izb,
            "slots_ekwip": plesho_praw_slots,
            "izb_tip_b": plesho_praw_b_izb,
        }
        plesho_praw = Limb(**data_liambs_plesho_praw)

        data_liambs_kost_plesha_praw = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость плеча правого",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(82, 89, 5, 32),
            "parent": plesho_praw,
        }
        kost_plesha_praw = Limb(**data_liambs_kost_plesha_praw)


        data_liambs_pred_plesho_praw = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "предплечье правое",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(79, 122, 10, 27),
            "fabric_depth": 8,
            "parent": plesho_praw,
            "draw_lear_telo": 24,
            "izb": pred_p_praw_izb,
            "slots_ekwip": pred_plesho_praw_slots,
            "izb_tip_b": pred_p_praw_b_izb,
        }
        pred_plesho_praw = Limb(**data_liambs_pred_plesho_praw)

        data_liambs_kost_pred_plesha_praw = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость предплечья правого",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(82, 124, 5, 24),
            "parent": pred_plesho_praw,
        }
        kost_pred_plesha_praw = Limb(**data_liambs_kost_pred_plesha_praw)


        data_liambs_kist_praw = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "кисть правая",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(79, 149, 10, 10),
            "fabric_depth": 4,
            "parent": pred_plesho_praw,
            "draw_lear_telo": 46,
            "izb": kist_prawa_izb,
            "slots_ekwip": kist_praw_slots,
            "izb_tip_b": kist_prawa_b_izb,
        }
        kist_praw = Limb(**data_liambs_kist_praw)


        efectiuw_paraw_ruka2 = Influence_parameters(
            name= "ефективвность правая рука",
            meaning=100,
            vliaet_na_shto="efectiuw_praw_ruka",
            znak= "+"
        )

        paraw_ruka = Osnowa("правая рука", [ plesho_praw , pred_plesho_praw , kist_praw , kost_plesha_praw , kost_pred_plesha_praw], 15, 15 , 
                            influence_attributes_list = [efectiuw_paraw_ruka2] , parametrs = [stoikost , sila , kordinatio , spead])



        # ---------------- ЛЕВАЯ РУКА ----------------
        data_liambs_plesho_lewoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "плечо левое",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(136, 89, 10, 35),
            "fabric_depth": 10,
            "parent": None,
            "draw_lear_telo": 25,
            "izb": plesho_lew_izb,
            "slots_ekwip": plesho_lewoe_slots,
            "izb_tip_b": plesho_lew_b_izb,
        }
        plesho_lewoe = Limb(**data_liambs_plesho_lewoe)

        data_liambs_pred_plesho_lewoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "предплечье левое",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(136, 122, 10, 27),
            "fabric_depth": 8,
            "parent": plesho_lewoe,
            "draw_lear_telo": 24,
            "izb": pred_p_lew_izb,
            "slots_ekwip": pred_plesho_lewoe_slots,
            "izb_tip_b": pred_p_lew_b_izb,
        }
        pred_plesho_lewoe = Limb(**data_liambs_pred_plesho_lewoe)

        data_liambs_kist_lewoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "кисть левая",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(136, 149, 10, 10),
            "fabric_depth": 4,
            "parent": pred_plesho_lewoe,
            "draw_lear_telo": 46,
            "izb": kist_lew_izb,
            "slots_ekwip": kist_lewoe_slots,
            "izb_tip_b": kist_lew_b_izb,
        }
        kist_lewoe = Limb(**data_liambs_kist_lewoe)


        data_liambs_kost_plesha_lewoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость плеча левого",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(139, 89, 5, 32),
            "parent": plesho_lewoe,
        }
        kost_plesha_lewoe = Limb(**data_liambs_kost_plesha_lewoe)

        data_liambs_kost_pred_plesha_lewoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость предплечья левого",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(139, 124, 5, 24),
            "parent": pred_plesho_lewoe,
        }
        kost_pred_plesha_lewoe = Limb(**data_liambs_kost_pred_plesha_lewoe)


        efectiuw_lewoe_ruka2 = Influence_parameters(
            name= "ефективвность левая рука",
            meaning=100,
            vliaet_na_shto="efectiuw_lew_ruka",
            znak= "+"
        )


        lewoe_ruka = Osnowa("левая рука", [plesho_lewoe, pred_plesho_lewoe, kist_lewoe, kost_plesha_lewoe, kost_pred_plesha_lewoe], 15, 15 , 
                            influence_attributes_list = [efectiuw_lewoe_ruka2] , parametrs = [stoikost , sila , kordinatio , spead])


        # ---------------- ПРАВАЯ НОГА ----------------
        data_liambs_bedro_prawoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "бедро правое",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(92, 146, 20, 45),
            "fabric_depth": 12,
            "parent": None,
            "draw_lear_telo": 1,
            "izb": bedro_praw_izb,
            "slots_ekwip": bedro_praw_slots,
        }
        bedro_prawoe = Limb(**data_liambs_bedro_prawoe)

        data_liambs_kost_bedra_prawoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость бедра правого",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(97, 146, 10, 43),
            "parent": bedro_prawoe,
        }
        kost_bedra_prawoe = Limb(**data_liambs_kost_bedra_prawoe)

        data_liambs_golen_prawoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "голень правая",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(93, 189, 18, 50),
            "fabric_depth": 8,
            "parent": bedro_prawoe,
            "draw_lear_telo": 1,
            "izb": golen_praw_izb,
            "slots_ekwip": golen_praw_slots,
        }
        golen_prawoe = Limb(**data_liambs_golen_prawoe)

        data_liambs_kost_golen_prawoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость голени правой",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(97, 189, 10, 50),
            "parent": golen_prawoe,
        }
        kost_golen_prawoe = Limb(**data_liambs_kost_golen_prawoe)

        data_liambs_stopa_prawoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "стопа правая",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(93, 237, 18, 10),
            "fabric_depth": 6,
            "parent": golen_prawoe,
            "draw_lear_telo": 1,
            "izb": stopa_praw_izb,
            "slots_ekwip": stopa_praw_slots,
        }
        stopa_prawoe = Limb(**data_liambs_stopa_prawoe)

        data_liambs_kost_stopu_prawoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость стопы правой",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(97, 237, 10, 10),
            "parent": stopa_prawoe,
        }
        kost_stopu_prawoe = Limb(**data_liambs_kost_stopu_prawoe)        



        prawa_noga_parametor = Influence_parameters(
            name= "ноги прм",
            meaning=3,
            vliaet_na_shto="spead_moving",
            znak= "-"
        )

        prawa_noga_parametor2 = Influence_parameters(
            name= "ефективность правая нога",
            meaning=100,
            vliaet_na_shto="efectiuw_praw_leg",
            znak= "+"
        )

        prawa_noga = Osnowa(name="правая нога",koneshonsti=[bedro_prawoe,golen_prawoe,stopa_prawoe,kost_bedra_prawoe,kost_golen_prawoe,kost_stopu_prawoe],x=15,y=15 , 
                            influence_attributes_list = [prawa_noga_parametor, prawa_noga_parametor2] , parametrs = [stoikost , sila , kordinatio , spead] )


        # ---------------- ЛЕВАЯ НОГА ----------------
        data_liambs_bedro_lewoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "бедро левое",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(114, 146, 20, 45),
            "fabric_depth": 12,
            "parent": None,
            "draw_lear_telo": 1,
            "izb": bedro_lew_izb,
            "slots_ekwip": bedro_lewoe_slots,
        }
        bedro_lewoe = Limb(**data_liambs_bedro_lewoe)

        data_liambs_kost_bedra_lewoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость бедра левого",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(119, 146, 10, 43),
            "parent": bedro_lewoe,
        }
        kost_bedra_lewoe = Limb(**data_liambs_kost_bedra_lewoe)

        data_liambs_golen_lewoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "голень левая",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(115, 189, 18, 50),
            "fabric_depth": 8,
            "parent": bedro_lewoe,
            "draw_lear_telo": 1,
            "izb": golen_lew_izb,
            "slots_ekwip": golen_lewoe_slots,
        }
        golen_lewoe = Limb(**data_liambs_golen_lewoe)

        data_liambs_kost_golen_lewoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость голени левой",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(119, 189, 10, 50),
            "parent": golen_lewoe,
        }
        kost_golen_lewoe = Limb(**data_liambs_kost_golen_lewoe)

        data_liambs_stopa_lewoe = {
            **LIMB_TEMPLATES["basic_limb"],
            "name": "стопа левая",
            "tip": "tkani",
            "glubina": 0,
            "bodi_rekt": pygame.Rect(115, 237, 18, 10),
            "fabric_depth": 6,
            "parent": golen_lewoe,
            "draw_lear_telo": 1,
            "izb": stopa_lew_izb,
            "slots_ekwip": stopa_lewoe_slots,
        }
        stopa_lewoe = Limb(**data_liambs_stopa_lewoe)


        data_liambs_kost_stopu_lewoe = {
            **LIMB_TEMPLATES["basic_bone"],
            "name": "кость стопы левой",
            "tip": "bone",
            "glubina": 1,
            "bodi_rekt": pygame.Rect(119, 237, 10, 10),
            "parent": stopa_lewoe,
        }
        kost_stopu_lewoe = Limb(**data_liambs_kost_stopu_lewoe)



        lew_noga_parametor = Influence_parameters(
            name= "ноги прм",
            meaning=3,
            vliaet_na_shto="spead_moving",
            znak = "-"
        )

        lew_noga_parametor2 = Influence_parameters(
            name= "ефективность правая нога",
            meaning=100,
            vliaet_na_shto="efectiuw_lew_leg",
            znak= "+"
        )

        lewa_noga = Osnowa( name = "левая нога", koneshonsti=[bedro_lewoe,golen_lewoe,stopa_lewoe,kost_bedra_lewoe,kost_golen_lewoe,kost_stopu_lewoe], x=15, y=15, 
                           influence_attributes_list = [lew_noga_parametor, lew_noga_parametor2], parametrs = [stoikost , sila , kordinatio , spead])



        self.part = [golowa , torso , paraw_ruka , lewoe_ruka , prawa_noga , lewa_noga]

        self.perebor_statow_tela()


    def update_cell_path(self , dt):
        self.frame_timer += self.frame_speed
        if self.frame_timer >= 1:
            self.frame_timer = 0
            self.frame_index = (self.frame_index + 1) % len(self.plita_frames)


    def perebor_statow_tela(self): ##!!!!!!!!
        temp_stats = self.main_system_hero_copy.copy()


        for part in self.part:
            part.perebor_koneshnostei()

            for yacheyka in part.influence_attributes_list_ready:

                if (
                    yacheyka is not None
                    and yacheyka["vliaet_na_shto"] in temp_stats
                ):
                    stat = yacheyka["vliaet_na_shto"]

                    result = self.operations[yacheyka["znak"]](temp_stats[stat],yacheyka["meaning"])
                    result = self.checking_permissions(result, stat)

                    temp_stats[stat] = result

        self.main_system_hero = temp_stats
                
        for part in self.part:
            # что будет удалено
            deleted = [k for k in part.koneshonsti if k.destroyed]

            # оставляем только живые
            part.koneshonsti = [
                k for k in part.koneshonsti
                if not k.destroyed
            ]

        self.apply_parameters()


    def update_efekts(self):
        #print(self.bload , "мл")
        krw = 0

        for rana in self.ranu_tela:
            spisok_ran = rana[0]

            for odna_rana in spisok_ran:   
                krw += odna_rana["кровь_л"]

        self.bload -= krw  * 1000 

        if self.bload <= 0 :
            self.death = True


    def apply_parameters(self):

        print("Применение параметров к конечностям...")

        # СБРОС К БАЗЕ
        for osn in self.part:
            for kon in osn.koneshonsti:

                for key, value in kon.base_stats.items():

                    if isinstance(value, dict):
                        setattr(kon, key, deepcopy(value))
                    else:
                        setattr(kon, key, value)

        # НАЛОЖЕНИЕ ПАРАМЕТРОВ
        for osn in self.part:

            for atribut in osn.parametrs:

                for kon in osn.koneshonsti:

                    if kon.tip != atribut.impact_factories:
                        continue

                    for key, value in atribut.influence_part_finish.items():

                        if not hasattr(kon, key):
                            continue

                        target = getattr(kon, key)

                        if isinstance(target, dict):

                            if isinstance(value, dict):

                                for sub_key, sub_value in value.items():

                                    if sub_key in target:

                                        target[sub_key][0] += sub_value[0]
                                        target[sub_key][1] += sub_value[1]

                        else:
                            setattr(
                                kon,
                                key,
                                target + value
                            )
    
        for osn in self.part:
            for atribut in osn.parametrs:
            
                for key, value in atribut.influence_main_system_finish.items():
                
                    if key in self.main_system_hero:
                        print(f"Применение бонуса {key}: +{value}")
        
                        self.main_system_hero[key] += value

        for skil in self.sklil_list:
            for name_sk in skil.influence_main_system:
                
                if name_sk in self.main_system_hero:
                    print(f"Применение бонуса от скила {name_sk} {key}: +{value}")
    
                    self.main_system_hero[name_sk] = self.main_system_hero[name_sk] + (self.main_system_hero[name_sk] / 100 * (skil.value * skil.interest_level))
    

    def checking_permissions(self , result , vliv):
        max_vliv = vliv + "_max"
        min_vliv = vliv + "_min"

        if max_vliv in self.main_system_hero:
            result = min(result, self.main_system_hero[max_vliv])

        if min_vliv in self.main_system_hero:
            result = max(result, self.main_system_hero[min_vliv])
            
    
        return int(result)



    def risowka_xit_boksa_tela(self, skreen):
        for osn in self.part:
            for kon in osn.koneshonsti:
                kon.draw(skreen)

        for osn in self.part:
            for slot in osn.slotu_broni:
                if slot["nadetost"] is not None:
                    bronya_obj = slot["nadetost"] 

                    if hasattr(bronya_obj, "spisok_shastei_broni"):
                        for elem_brona in bronya_obj.spisok_shastei_broni:
                                elem_brona.draw(skreen)


    def pol_spisok_tela_popad(self, point):
        x, y = point
        hit_parts = []

        all_osnowa = self.part

        outer_hits = []
        inner_candidates = []

        for osn in all_osnowa:
            for limb in osn.koneshonsti:

                if limb.glubina == 0:
                    if limb.bodi_rekt.collidepoint(x, y):
                        outer_hits.append(limb)

                        for inner_limb in osn.koneshonsti:
                            if inner_limb.glubina > 0:
                                inner_candidates.append(inner_limb)

        if not outer_hits:
            return []

        hit_parts.extend(outer_hits)

        inner_candidates.sort(key=lambda l: l.glubina)

        for limb in inner_candidates:
            if limb.bodi_rekt.collidepoint(x, y):
                hit_parts.append(limb)

        return hit_parts


    def pol_spisok_broni_popad(self, point):

        x, y = point
        vse_sloi = []
        used_ids = set()
    
        for osn in self.part:
            for limb in osn.koneshonsti:
            
                for slot in limb.slots_ekwip:
                
                    bronya = slot.get("nadetost")
                    sloi = slot.get("sloi")
    
                    if bronya is None or sloi is None:
                        continue
                    
                    if hasattr(bronya, "spisok_shastei_broni"):
                    
                        for elem in bronya.spisok_shastei_broni:
                        
                            if any(rect.collidepoint(x, y) for rect in elem.xit_boks):
                            
                                # 🔥 проверка на уникальность
                                if id(elem) not in used_ids:
                                    vse_sloi.append((sloi, elem))
                                    used_ids.add(id(elem))
    
        vse_sloi.sort(key=lambda item: item[0], reverse=True)
    
        hit_armor = [elem for _, elem in vse_sloi]
    
        return hit_armor


    def random_klik_popad(self):
        proiti = True
        while proiti:
            x = randint(1 , 300)
            y =  randint(1 ,300)
            vuvod_shastei_broni = self.pol_spisok_broni_popad((x , y))
            vuvod_shastei_tela = self.pol_spisok_tela_popad((x , y))
            if vuvod_shastei_tela:
                proiti = False

        return vuvod_shastei_broni , vuvod_shastei_tela


    def sprawka(self , rect ,  a ):

        if sprawka_parameters.start == False and sprawka_parameters.plear == None:
            sprawka_parameters.start = True
            sprawka_parameters.plear = a
            print("начало справки" , a)


        elif sprawka_parameters.start == True and sprawka_parameters.plear != a:
            sprawka_parameters.start = True
            sprawka_parameters.plear = a
            print("смена персонажа в справке" , a)
            
        else:
            sprawka_parameters.start = False
            sprawka_parameters.plear = None
            print("конец справки" , a)


    def eqwip_plear(self , brona):
        brona.eqwip_techn(self)
        self.update_weapons_in_hands()


    def inwentor_add_iasheka(self , app_iaseki):
        for iasheika in self.iaseki:
            self.inwentor.iasheki.append(iasheika)

        for iasheika in app_iaseki:
            self.inwentor.iasheki.append(iasheika)


    def delit_predmet_iz_inw(self, poz_x_y , wuborka_ydal):
        self.update_weapons_in_hands()
        x, y = poz_x_y
        #print( wuborka_ydal , wuborka_ydal.spis_pridm_spr)
        if wuborka_ydal == None:
            for rect, pred, index , wuborka in self.inwentor.spis_pridm_spr:
                if rect.collidepoint(x, y):
                    wuborka.pridmetu.pop(index)
                    return
                
        else:
            for rect, pred, index , wuborka in wuborka_ydal.spis_pridm_spr:
                if rect.collidepoint(x, y):
                    wuborka.pridmetu.pop(index)
                    return


    def dobawit_predmet(self , poz_x_y , predmet , wuborka = None ):
        #if wuborka:
        #    print("не продумана")
        #else:
        self.inwentor.iasheki[0].pridmetu.append(predmet)
        self.update_weapons_in_hands()


    def inwentor_add_iasheka_vse(self , app_iaseki , sposob_yd_dob):
        if sposob_yd_dob == True:
            self.inwentor.iasheki.append(app_iaseki)

        elif sposob_yd_dob == False:
            self.inwentor.iasheki.remove(app_iaseki)

        else:
            print("ошбыка")
        

    def wubrosit_iz_inwentar(self , poz_x_y , wuborka_ydal , predmet):
            TILE = 16
            offsets = [(-1, -1) , (0, -1) , (1, -1),(-1,  0) , (1,  0) , (-1,  1) , (0,  1), (1,  1)]

            dx, dy = choice(offsets)
            dalshe_x = (self.x + dx) * TILE - 24
            dalshe_y = (self.y + dy) * TILE - 48

            reteite = randint(0 , 360)
            predmet_igru = ItemLying(x=dalshe_x,y=dalshe_y,image=predmet.izb_na_sheloweke,prudmet=predmet , rotate = reteite)

            igrowoe_okrugenie_personag.append(predmet_igru)
            predmetu_leg.append(predmet_igru)

            self.delit_predmet_iz_inw(poz_x_y, wuborka_ydal)


    def update_weapons_in_hands(self):

        self.current_weapons = []
        self.two_handed = False

        hands = ["кисть правая", "кисть левая"]

        for part_osn in self.part:            # Osnowa
            for limb in part_osn.koneshonsti: # все Limb

                if limb.name not in hands:
                    continue

                for slot in limb.slots_ekwip:   # ✅ новая система
                    
                    if slot["ekwip_name"] != "оружые":

                        continue

                    weapon = slot["nadetost"]
                    if weapon is None:
                        continue

                    weapon_info = {
                        "weapon": weapon,
                        "hand": limb.name,
                        "osnova": part_osn,
                        "osnova_name": part_osn.name,
                        "hand_type": getattr(weapon, "two_handed", False)
                    }

                    # если одно оружие двуручное, флаг включается
                    if getattr(weapon, "two_handed", False):
                        self.two_handed = True

                    self.current_weapons.append(weapon_info)


    def apply_recoil_from_point(self, source_x, source_y, duration, range_px, hold):
    
        dx = self.x - source_x
        dy = self.y - source_y

        dx = -dx
        dy = -dy
    
        dx = 0 if dx == 0 else dx // abs(dx)
        dy = 0 if dy == 0 else dy // abs(dy)
    
        if dx == 0 and dy == 0:
            dir_vec = pygame.Vector2(1, 0)
        else:
            dir_vec = pygame.Vector2(dx, dy).normalize()
    
        if dy == 0:
            anim_type = "side"
        elif dx == 0:
            anim_type = "vertical"
        else:
            anim_type = "diagonal"
    
        # 🔥 ВОТ ЭТО ДОБАВЬ
        self.hit_flash_time = self.hit_flash_duration
    
        self.recoil_state = {
            'source': None,
            'dir': dir_vec,
            'progress': 0.0,
            'duration': duration,
            'range': range_px,
            'flip_x': (self.direction == "left"),
            'flip_y': dy > 0,
            'anim_type': anim_type,
            'hold': hold
        }


    def calc_layers(self , layers):
        if not layers:
            return []

        # сортируем копию по глубине
        sorted_layers = sorted(layers, key=lambda x: x.glubina)

        # сумма внутренних слоев
        inner_sum = sum(l.fabric_depth for l in sorted_layers[1:])

        result_map = {}

        # первый слой уменьшается
        first = sorted_layers[0]
        result_map[first] = max(first.fabric_depth - inner_sum, 0)

        # остальные без изменений
        for l in sorted_layers[1:]:
            result_map[l] = l.fabric_depth

        # возвращаем в исходном порядке
        return [(l, result_map[l]) for l in layers]



    def hit(self, unit_atakowan):
        if self.xod_time <= 0 and self.in_battle == True:
            return

        if self.in_battle == True:
            self.xod_time -= 3

        if unit_atakowan is self:
            print("Нельзя атаковать самого себя")
            return
        
        """Запускает анимацию атаки у self и отбрасывание у цели (simultaneous)."""
        if not unit_atakowan:
            return

        # direction in tile coords
        dx = unit_atakowan.x - self.x
        dy = unit_atakowan.y - self.y

        dx = 0 if dx == 0 else dx // abs(dx)
        dy = 0 if dy == 0 else dy // abs(dy)

        if dy == 0:
            anim_type = "side"
        elif dx == 0:
            anim_type = "vertical"
        else:
            anim_type = "diagonal"

        if dx == 0 and dy == 0:
            # если в одной клетке — направление по умолчанию
            dir_vec = pygame.Vector2(1, 0)
        else:
            dir_vec = pygame.Vector2(dx, dy)
            dir_vec = dir_vec.normalize()

        # pixel ranges (настраиваемые)
        attacker_range_px = 6    # атака — сдвиг атакующего на ~половину клетки (16px) => 8px

        if dx == 0 or dy == 0:  # удар по стороне
            target_recoil_px = 8
        else:  # диагональ
            target_recoil_px = 9

        duration_ms = 60  # длительность анимации (мс)

        if dir_vec.x < 0:
            self.direction = "left"
        else:
            self.direction = "right"


        # ставим state у атакующего
        self.attack_state = {
            'target': unit_atakowan,
            'dir': dir_vec,
            'progress': 0.0,
            'duration': duration_ms,
            'range': attacker_range_px,
            'damage_applied': False,
            'frame_index': 0,
            'flip_x': (self.direction == "left"),
            'flip_y': dy > 0,
            'anim_type': anim_type,
            'hold': 20 ,
        }

        # ставим recoil у цели — происходит одновременно
        unit_atakowan.recoil_state = {
            'source': self,
            'dir': -dir_vec,
            'progress': 0.0,
            'duration': duration_ms,
            'range': target_recoil_px , 
            'flip_x': (self.direction == "left") ,
            'weapon': self.current_weapons[0]['weapon'] if self.current_weapons else None , 
            'angle': math.degrees(math.atan2(dy, dx)),
            'anim_type': anim_type,
            'flip_y': dy > 0 ,
            'hold': 20
        }

        # (опционально) можно сразу проиграть звук, поставить cooldown и т.п.


    def get_hit(self, source, damage_data):
        self.hit_flash_time = self.hit_flash_duration


        vuvod_shastei_broni , vuvod_shastei_tela = self.random_klik_popad()
        vse_sloi = vuvod_shastei_broni + vuvod_shastei_tela

        hit = Get_hit(self.name , damage_data, vse_sloi)
        Ek , P , S = hit.get_hit()

        self.perebor_statow_tela()

    def hit_hand(self , None_wepon_is_hand_hit , None_wepon_is_hand_hit_spr_prm):
        twerd = None_wepon_is_hand_hit_spr_prm.twerdost

        for i in None_wepon_is_hand_hit.parametrs:
            if i.name == "сила":
                sila = i
            elif i.name == "скорость":
                spead = i



        return {"Ek": sila.value * sila.modifier, "P": 5 * spead.value * spead.modifier, "S": 3 , "object": None, "twerdost": twerd}
                
    def _update_attack_and_recoil(self, dt):
        # =========================
        # ATTACK
        # =========================
        None_wepon_is_hand_hit = self.part[2]  # правая рука
        None_wepon_is_hand_hit_spr_prm = self.part[2].koneshonsti[2] # кисть


        if self.attack_state:
            st = self.attack_state
            st['progress'] += dt

            duration = st['duration']
            hold = st.get('hold', 0.0)

            time = min(st['progress'], duration)

            # фазы: вперёд → задержка → назад
            move_time = duration - hold
            half = move_time / 2

            if time < half:
                ease = time / half
            elif time < half + hold:
                ease = 1.0
            else:
                ease = 1.0 - (time - half - hold) / half

            ease = max(0.0, min(1.0, ease))

            # ✅ ДВИЖЕНИЕ (без костылей)
            px_off = st['dir'] * (st['range'] * ease)
            self.attack_offset = px_off

            # нанесение урона
            if (not st['damage_applied']) and time >= half:
                target = st['target']

                if self.current_weapons:
                    weapon = self.current_weapons[0]['weapon']
                    weapon.hero = {"hero": self , "osnova":self.current_weapons[0]["osnova"]}
                    dmg = weapon.damage_calculations()
                    weapon.hero = None
                else:
                    dmg = self.hit_hand(None_wepon_is_hand_hit, None_wepon_is_hand_hit_spr_prm)

                target.get_hit(self, dmg)
                st['damage_applied'] = True

            # завершение
            if time >= duration:
                self.attack_state = None
                self.attack_offset = pygame.Vector2(0, 0)

            # анимация оружия
            if self.current_weapons:
                weapon = self.current_weapons[0]['weapon']
                anim_type = st.get("anim_type")

                if anim_type in weapon.animations:
                    frames = weapon.animations[anim_type]
                    frame_count = len(frames)

                    p = time / duration
                    frame = int(p * frame_count)
                    frame = min(frame, frame_count - 1)

                    st['frame_index'] = frame

        # =========================
        # RECOIL
        # =========================
        if self.recoil_state:
            rst = self.recoil_state
            rst['progress'] += dt

            duration = rst['duration']
            hold = rst.get('hold', 0.0)

            time = min(rst['progress'], duration)

            move_time = duration - hold
            half = move_time / 2

            if time < half:
                ease = time / half
            elif time < half + hold:
                ease = 1.0
            else:
                ease = 1.0 - (time - half - hold) / half

            ease = max(0.0, min(1.0, ease))

            # ✅ ОТДАЧА (в обратную сторону)
            px_off = -rst['dir'] * (rst['range'] * ease)
            self.recoil_offset = px_off

            # завершение
            if time >= duration:
                self.recoil_state = None
                self.recoil_offset = pygame.Vector2(0, 0)

            # анимация оружия
            weapon = rst.get('weapon')
            if weapon and hasattr(weapon, "animation_frames") and weapon.animation_frames:
                frames = weapon.animation_frames
                frame_count = len(frames)

                p = time / duration
                frame = int(p * frame_count)
                frame = min(frame, frame_count - 1)

                rst['frame_index'] = frame

        # =========================
        # HIT FLASH
        # =========================
        if self.hit_flash_time > 0:
            self.hit_flash_time -= dt
            if self.hit_flash_time < 0:
                self.hit_flash_time = 0



    def draw_attack_range(self, surface):
        current_pos = (self.x, self.y)
    
        # -----------------------------
        # КЕШ blocked tiles карты
        # -----------------------------
        if not hasattr(self, "blocked_cache"):
            self.blocked_cache = load_blocked_tiles_from_tmx(tmx_map)
    
        # -----------------------------
        # СОЗДАНИЕ ТАЙЛА melee
        # -----------------------------
        if not hasattr(self, "attack_tile"):
            fill_color = (200, 205, 210, 40)
            outline_color = (255, 255, 255, 120)
    
            self.attack_tile = pygame.Surface(
                (TILE_SIZE, TILE_SIZE),
                pygame.SRCALPHA
            )
    
            pygame.draw.rect(
                self.attack_tile,
                fill_color,
                self.attack_tile.get_rect(),
                border_radius=3
            )
    
            pygame.draw.rect(
                self.attack_tile,
                outline_color,
                self.attack_tile.get_rect(),
                1,
                border_radius=3
            )
    
        # -----------------------------
        # ЕСЛИ ПОЗИЦИЯ ИЛИ ТИП АТАКИ ИЗМЕНИЛИСЬ
        # -----------------------------
        if (
            not hasattr(self, "attack_range_surface")
            or self.kesh_poz != current_pos
            or getattr(self, "last_melee_state", None) != self.melee_weapons
        ):
    
            self.kesh_poz = current_pos
            self.last_melee_state = self.melee_weapons
    
            # -----------------------------
            # ПОЛУЧАЕМ КЛЕТКИ
            # -----------------------------
            if self.melee_weapons:
                self.kesh_cell = get_attack_cells(
                    self.x,
                    self.y,
                    self.mein_range,
                    self.blocked_cache
                )
            else:
                self.kesh_cell = get_attack_cells(
                    self.x,
                    self.y,
                    self.mein_range,
                    self.blocked_cache,
                    shape="circle"
                )
    
            cells = self.kesh_cell
    
            # -----------------------------
            # ЕСЛИ НЕТ КЛЕТОК — ВЫХОД
            # -----------------------------
            if not cells:
                return
    
            # -----------------------------
            # ГРАНИЦЫ SURFACE (локальный bounding box)
            # -----------------------------
            min_x = min(cx for cx, cy in cells)
            max_x = max(cx for cx, cy in cells)
            min_y = min(cy for cx, cy in cells)
            max_y = max(cy for cx, cy in cells)
    
            width = (max_x - min_x + 1) * TILE_SIZE
            height = (max_y - min_y + 1) * TILE_SIZE
    
            self.attack_range_offset = (min_x * TILE_SIZE, min_y * TILE_SIZE)
    
            # -----------------------------
            # СОЗДАЁМ SURFACE
            # -----------------------------
            self.attack_range_surface = pygame.Surface(
                (width, height),
                pygame.SRCALPHA
            )
    
            # -----------------------------
            # BLIT RECTS ДЛЯ ПРОВЕРКИ
            # -----------------------------
            self.unit_attack_range = []
    
            # =========================================================
            # MELEE
            # =========================================================
            if self.melee_weapons:
            
                for cx, cy in cells:
                
                    local_x = (cx - min_x) * TILE_SIZE
                    local_y = (cy - min_y) * TILE_SIZE
    
                    rect = pygame.Rect(
                        cx * TILE_SIZE,
                        cy * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
    
                    self.unit_attack_range.append(rect)
    
                    self.attack_range_surface.blit(
                        self.attack_tile,
                        (local_x, local_y)
                    )
    
            # =========================================================
            # RANGED
            # =========================================================
            else:
                cells_set = set(cells)
                ts = TILE_SIZE
                color = (255, 255, 255, 180)
    
                for cx, cy in cells_set:
                
                    px = (cx - min_x) * ts
                    py = (cy - min_y) * ts
    
                    rect = pygame.Rect(
                        cx * TILE_SIZE,
                        cy * TILE_SIZE,
                        TILE_SIZE,
                        TILE_SIZE
                    )
    
                    self.unit_attack_range.append(rect)
    
                    # верх
                    if (cx, cy - 1) not in cells_set:
                        pygame.draw.line(
                            self.attack_range_surface,
                            color,
                            (px, py),
                            (px + ts, py),
                            2
                        )
    
                    # низ
                    if (cx, cy + 1) not in cells_set:
                        pygame.draw.line(
                            self.attack_range_surface,
                            color,
                            (px, py + ts),
                            (px + ts, py + ts),
                            2
                        )
    
                    # лево
                    if (cx - 1, cy) not in cells_set:
                        pygame.draw.line(
                            self.attack_range_surface,
                            color,
                            (px, py),
                            (px, py + ts),
                            2
                        )
    
                    # право
                    if (cx + 1, cy) not in cells_set:
                        pygame.draw.line(
                            self.attack_range_surface,
                            color,
                            (px + ts, py),
                            (px + ts, py + ts),
                            2
                        )
    



    def build_outline_cache(self, surface , color=(235,235,235)):

        self.mask = pygame.mask.from_surface(surface)

        self.outline_points = self.mask.outline()

        self.outline_glow = self.mask.to_surface(setcolor=color, unsetcolor=(0,0,0))
        self.outline_glow.set_colorkey((0,0,0))
        self.outline_glow.set_alpha(0)


    def draw_outline(self, screen,  pos, color=(235, 235, 235) , color2 = (180, 180, 180)):
        mask = pygame.mask.from_surface(screen)

        # создаём увеличенную маску
        outline_mask = pygame.mask.Mask(
            (mask.get_size()[0] + 2, mask.get_size()[1] + 2)
        )

        # накладываем оригинал со смещением (расширяем)
        outline_mask.draw(mask, (1, 0))
        outline_mask.draw(mask, (-1, 0))
        outline_mask.draw(mask, (0, 1))
        outline_mask.draw(mask, (0, -1))

        # вычитаем оригинал → остаётся только контур
        outline_mask.erase(mask, (0, 0))

        # превращаем в surface
        outline_surface = outline_mask.to_surface(
            setcolor=color,
            unsetcolor=(0, 0, 0)
        )
        outline_surface.set_colorkey((0, 0, 0))

        # рисуем
        # --- внутренняя подсветка ---
        fill_surface = mask.to_surface(
            setcolor=color2,
            unsetcolor=(0, 0, 0)
        )
        fill_surface.set_colorkey((0, 0, 0))
        fill_surface.set_alpha(45)  # прозрачность (настрой)

        screen.blit(fill_surface, pos)


        screen.blit(outline_surface, (pos[0] , pos[1] ))

        screen.blit(self.color_gerb , (pos[0] + 24 , pos[1] + 12 )) 
        screen.blit(self.stroke_gerb , (pos[0] + 24 , pos[1] + 12 ))


    def card_application(self, surface, dt , m_x, m_y):
        if self.aktiw_cards is not None and self.aktiw_animeshon == False:
            self.melee_weapons = False

            card = self.aktiw_cards[0]

            self.mein_range = card.choice_target.range
            self.variable_draw_attack_range = True

            card.choice_target.risowka(self.x, self.y, surface , m_x, m_y)

            self.aktiWnost_kartu = True

    
        elif self.aktiWnost_kartu == True and self.aktiw_animeshon == True:
            card = self.aktiw_cards[0]

            card.choice_target.cache_surface = None

            self.variable_draw_attack_range = False
            self.melee_weapons = True
            prodolgutelnost = card.method_damage.animeishon_cards(
                dt,
                card.choice_target.draw_pos_x,
                card.choice_target.draw_pos_y,
                card.choice_target.target_dx,
                card.choice_target.target_dy,
                m_x, 
                m_y
            )

            if prodolgutelnost:
                self.aktiw_cards = None
                self.aktiWnost_kartu = False
                self.aktiw_animeshon = False



    def turn_attacking(self , skren ,  m_x , m_y , draw_rect):
        if self.variable_draw_attack_range:
            dead_zone = 4  
            dx = draw_rect.centerx - m_x
            if abs(dx) > dead_zone:

                if dx > 0:
                    self.direction = "left"
                elif dx < 0:
                    self.direction = "right"





class DrawWrapper:
    def __init__(self, obj, draw_layer):
        self.obj = obj
        self.draw_layer = draw_layer

    def __getattr__(self, name):
        return getattr(self.obj, name)
    
    