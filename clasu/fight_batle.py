from funk.get_bloked_dist_put import *
from config.config import *

import random

class Fight():
    def __init__(self , Ui_interfese , iniceatiw_skal  ): 

        self.Ui_interfese = Ui_interfese 
        self.iniceatiw_skal = iniceatiw_skal

        self.kto_xodit = None
        self.start_batal = True

        self.kommand = [] 

        self.tmx_map = None
        self.zanat_cell = None

        self.kolors_arm = [(0 , 0 , 200) , (0 , 200 , 0) , (200 , 0 , 0)]

        self.tile  = None
        self.tile_zanat = None

        self.end_battle_bool = False


    def start_batel(self, kommand):
        st_kolor = 0
        self.kommand = kommand

        for km in kommand:
            
            for unit in km:
                color = self.kolors_arm[st_kolor]
                self.iniceatiw_skal.add_unit(unit , color , st_kolor)
                unit.in_battle = True
                unit.team = st_kolor

            st_kolor += 1

        self.iniceatiw_skal.update_xods(turns=10)
        self.iniceatiw_skal.normalize_initiative()

        self.Ui_interfese.start_batal = True
        self.kto_xodit = self.iniceatiw_skal.xods[0]
        tile_zanat = load_blocked_tiles_from_tmx(tmx_map, layer_name="colision")
        self.tile_zanat = tile_zanat

        self.kto_xodit["unit"].aktiv_unit = True



    def apdete_xod(self ):

        if self.end_battle_bool:
            return

        # --- УДАЛЯЕМ ВСЕХ МЁРТВЫХ ---
        someone_removed = False

        for x in self.iniceatiw_skal.xods[:]:
            unit = x["unit"]
            if unit.death:
                self.remove_dead_unit(unit)
                someone_removed = True

        if someone_removed:
            self.check_battle_end()
            if self.end_battle_bool:
                return


        if not self.kto_xodit:
            return
        
        if self.kto_xodit["unit"].death:
            dead = self.kto_xodit["unit"]
            self.remove_dead_unit(dead)
            self.check_battle_end()
            return

        if self.kto_xodit["unit"].xod_time <= 0  and  self.kto_xodit["unit"].attack_state is None :

            self.kto_xodit["unit"].aktiv_unit = False

            self.iniceatiw_skal.xods.remove(self.kto_xodit)
            
            if not self.iniceatiw_skal.xods:
                self.end_battle()
                return
            
            self.kto_xodit = self.iniceatiw_skal.xods[0]

            self.kto_xodit["unit"].xod_time = self.kto_xodit["unit"].xod_time_max   
            self.iniceatiw_skal.normalize_initiative()
            self.kto_xodit["unit"].aktiv_unit = True

            self.kto_xodit["unit"].update_efekts()


        if self.kto_xodit["unit"].main_system_hero["time_movement"] == 0:
            kol_cell = self.kto_xodit["unit"].xod_time // 1 
        else:
            kol_cell = self.kto_xodit["unit"].xod_time // self.kto_xodit["unit"].main_system_hero["spead_moving"] 


        tile = get_move_area(self.kto_xodit["unit"].x , self.kto_xodit["unit"].y , kol_cell , 50 , 50 , self.tile_zanat , units_kletki_zanatu)
        self.tile = tile


        if self.kto_xodit["unit"].team != 0:
            self.ai_single_unit(self.kto_xodit)
        


    def ai_single_unit(self, unit_dict):

        unit = unit_dict["unit"]

        if unit.death:
            print(unit.name, "death")
            self.remove_dead_unit(unit)
            self.check_battle_end()
            return

        if unit.attack_state is not None:
            return

        if unit.path:
            return

        enemy = self.find_nearest_enemy(unit)
        if not enemy:
            return

        dx = abs(enemy.x - unit.x)
        dy = abs(enemy.y - unit.y)

        in_range = max(dx, dy) <= unit.mein_range

        if in_range:
            unit.hit(enemy)
        
            if enemy.death:
                self.remove_dead_unit(enemy)
                self.check_battle_end()
        
            return

        # --- считаем занятые клетки ---
        occupied = {
            (u.x, u.y)
            for km in self.kommand
            for u in km
            if u != unit
        }


        free_cells = get_available_cells(
            start_x=enemy.x,
            start_y=enemy.y,
            radius=1,
            map_w=50,
            map_h=50,
            blocked_tiles=self.tile_zanat,
            occupied_tiles=occupied,
            allow_target_occupied=False  # ← ВАЖНО
        )


        free_cells.discard((enemy.x, enemy.y))


        if not free_cells:
            return

        target = min(
            free_cells,
            key=lambda pos: abs(pos[0] - unit.x) + abs(pos[1] - unit.y)
        )


        unit.idti_k(
            px=target[0],
            py=target[1],
            players=occupied,
            pretendeimue_kletki=[],
            ready_way=True
        )


    def find_nearest_enemy(self, active_unit):
        enemies = []

        for km in self.kommand:
            for u in km:
                if u != active_unit and u.team != active_unit.team:
                    enemies.append(u)

        if not enemies:
            return None

        # ищем по обычной дистанции (быстро и достаточно)
        nearest = min(
            enemies,
            key=lambda e: abs(e.x - active_unit.x) + abs(e.y - active_unit.y)
        )

        return nearest


    def remove_dead_unit(self, unit):

        unit.aktiv_unit = False
        unit.xod_time = 0

        for km in self.kommand:
            if unit in km:
                km.remove(unit)

        self.iniceatiw_skal.xods = [
            x for x in self.iniceatiw_skal.xods
            if x["unit"] != unit
        ]

        if self.kto_xodit and self.kto_xodit["unit"] == unit:
            if self.iniceatiw_skal.xods:
                self.kto_xodit = self.iniceatiw_skal.xods[0]
                self.kto_xodit["unit"].aktiv_unit = True
            else:
                self.end_battle()


    def check_battle_end(self):
        alive_teams = set()

        for km in self.kommand:
            for u in km:
                if not u.death:
                    alive_teams.add(u.team)

        if len(alive_teams) <= 1:
            self.end_battle()


    def end_battle(self):
        print("Бой завершён")

        for km in self.kommand:
            for u in km:
                u.in_battle = False
                u.aktiv_unit = False
                u.team = None

                # сброс эффектов
                if hasattr(u, "clear_effects"):
                    u.clear_effects()

                print("он тут пашол ")
                u.idti_k(
                    px=random.randint(1 , 50),
                    py=random.randint(1 , 50),
                    players=[],
                    pretendeimue_kletki=[],
                    ready_way=True
                )
        # очистить шкалу инициативы
        self.iniceatiw_skal.xods.clear()

        self.kto_xodit = None
        self.Ui_interfese.start_batal = False

        self.end_battle_bool = True







#kx2 = 0
#if len(self.xods) == 0:
#    self.update_xods( turns=10)

#elif len(self.xods) < 10:
#    turn = len(self.xods) - 10
#    turn = abs(turn)
#    self.update_xods(turns = turn)


