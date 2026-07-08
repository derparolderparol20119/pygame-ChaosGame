import pygame
from funk.bar_poloski_spr import *
from clasu.DamageProcessor import *
import math

class Brona():
    def __init__(self , name , tip  , izb  , spisok_shastei_broni ):# shasti_dla_pokrutia = [{ekwip_name , ekwip_name_na_shto}]
        self.name = name
        self.tip = tip 

        self.hp = 0
        self.hp_max = 0

        self.izb = izb
        self.izb_na_sheloweke = None
        self.izb_na_sheloweke_two_handed = None

        self.spisok_shastei_broni = spisok_shastei_broni
        self.masa = 0

        self.sprawka_text = [
        {"text":"Надеть","funk":"sprawka_nadet",},
        {"text":"Снять","funk":"sprawka_snat"},
        {"text":"Выбросить","funk":"vubrosit"}
        ]
        self.height = 45 + len(self.spisok_shastei_broni) * 90 + 6
        self.bg = pygame.Surface((230, self.height), pygame.SRCALPHA)

        self.perebor_izb_spiskow()
        self.masa_perebor()


    def eqwip(self, character, poz_x_y, wuborka_ydal):

        slots_to_equip = []

        for elem in self.spisok_shastei_broni:

            for osn in character.part:
                for limb in osn.koneshonsti:

                    if limb.name != elem.ekwip_name_na_shto:
                        continue

                    for slot in limb.slots_ekwip:
                        if slot["ekwip_name"] == elem.ekwip_name:
                            slots_to_equip.append(slot)
                        

        if not slots_to_equip:
            return

        # проверка занятости
        for slot in slots_to_equip:
            if slot["nadetost"] is not None:
                return

        # надеваем
        for slot in slots_to_equip:
            slot["nadetost"] = self

        self.ybrat_iz_inwentor(character, poz_x_y, wuborka_ydal)


    def unequip(self, character, poz, wuborka_ydal):
    
        slot_snat = False
    
        for osn in character.part:
            for limb in osn.koneshonsti:
                for slot in limb.slots_ekwip:
                    if slot["nadetost"] is self:
                        slot["nadetost"] = None
                        slot_snat = True
    
        if slot_snat:
            character.dobawit_predmet(poz, self, wuborka_ydal)


    def perebor_izb_spiskow(self):
        if not self.spisok_shastei_broni:
              return

        # --- определяем размер финального сурфейса ---
        max_w = 0
        max_h = 0
        
        for elem in self.spisok_shastei_broni:
          
            if elem.izb:
                max_w = max(max_w, elem.izb.get_width())
                max_h = max(max_h, elem.izb.get_height())
        
            if elem.izb_two_hend:
                max_w = max(max_w, elem.izb_two_hend.get_width())
                max_h = max(max_h, elem.izb_two_hend.get_height())
        
        if max_w == 0 or max_h == 0:
            return
        
        # --- создаём итоговые сурфейсы ---
        normal_surf = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
        two_hand_surf = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
        
        # --- объединяем изображения ---
        for elem in self.spisok_shastei_broni:
          
            # обычная версия
            if elem.izb:
                normal_surf.blit(elem.izb, (0, 0))
        
            # версия для двух рук
            if elem.izb_two_hend:
                two_hand_surf.blit(elem.izb_two_hend, (0, 0))
            elif elem.izb:
                # если нет отдельной версии — используем обычную
                two_hand_surf.blit(elem.izb, (0, 0))
        
        # сохраняем в объекте
        self.izb_na_sheloweke = normal_surf
        self.izb_na_sheloweke_two_handed = two_hand_surf


    def masa_perebor(self):
        self.masa = 0 
        self.hp = 0
        self.hp_max = 0 

        for elem in self.spisok_shastei_broni:
           self.masa += (elem.masa) * 0.001
           self.hp += elem.hp
           self.hp_max += elem.hp_max


    def ybrat_iz_inwentor(self, plear, poz , wuborka_ydal):
        plear.delit_predmet_iz_inw(poz , wuborka_ydal)


    def wuzow_sprawki(self, screen, x, y, font):
        x += 13
        y += 13

        PART_H = 90
        WIDTH = 260
        HEADER_H = 45

        height = self.height
        bg = self.bg

        # ---------- ФОН ----------
        pygame.draw.rect(bg, (35, 35, 35, 150), bg.get_rect())
        screen.blit(bg, (x, y))
        pygame.draw.rect(screen, (95, 95, 95), (x, y, WIDTH, height), 1)

        # ---------- ЗАГОЛОВОК ----------
        screen.blit(font.render(self.name, True, (170, 190, 220)), (x + 6, y + 4))
        screen.blit(
            font.render(f"Масса: {self.masa} кг", True, (180, 180, 180)),
            (x + 6, y + 24),
        )

        cy = y + HEADER_H

        # ---------- ЧАСТИ БРОНИ ----------
        for elem in self.spisok_shastei_broni:

            part_bg = pygame.Surface((WIDTH - 10, PART_H - 6), pygame.SRCALPHA)
            pygame.draw.rect(part_bg, (25, 25, 25, 160),
                             part_bg.get_rect(), border_radius=4)
            screen.blit(part_bg, (x + 5, cy))

            screen.blit(
                font.render(elem.name, True, (220, 220, 220)),
                (x + 10, cy + 4),
            )

            screen.blit(
                font.render(elem.ekwip_name_na_shto, True, (140, 140, 140)),
                (x + 150, cy + 4),
            )

            bar_x = x + 12
            bar_y = cy + 22

            cy += PART_H
    

    def eqwip_techn(self, character ):
        slots_to_equip = []

        for elem in self.spisok_shastei_broni:

            for osn in character.part:
                for limb in osn.koneshonsti:

                    if limb.name != elem.ekwip_name_na_shto:
                        continue

                    for slot in limb.slots_ekwip:
                        if slot["ekwip_name"] == elem.ekwip_name:
                            slots_to_equip.append(slot)

        if not slots_to_equip:
            return

        # проверка занятости
        for slot in slots_to_equip:
            if slot["nadetost"] is not None:
                return

        # надеваем
        for slot in slots_to_equip:
            slot["nadetost"] = self


    def sprawka_nadet(self , parts , poz_x_y ,  wuborka_ydal):
        self.eqwip(parts ,  poz_x_y , wuborka_ydal)

    def sprawka_snat(self , parts ,  poz_x_y , wuborka_ydal ):
        self.unequip(parts ,  poz_x_y , wuborka_ydal)

    def vubrosit(self , plear , poz, wuborka_ydal):
        plear.wubrosit_iz_inwentar(poz , wuborka_ydal , self)



class Elem_Broni(DamageProcessor):
    def __init__(self , name , ekwip_name , ekwip_name_na_shto , xit_boks , izb , izb_two_hend , tolshina , plotnost , kof_hp_material_strength  , twerdost  , spr_wozdeistwiam_test  , spr_wozdeistwiam_impuls  , softening_prn  , contact_profile  , increasing_contact_pr = 0.0, increasing_contact_kn = 0.0, impulse_damping = 0.0):
        super().__init__(name, tolshina, plotnost, kof_hp_material_strength, increasing_contact_pr, increasing_contact_kn, impulse_damping, twerdost, spr_wozdeistwiam_test, spr_wozdeistwiam_impuls, softening_prn, contact_profile)


        self.ekwip_name = ekwip_name
        self.ekwip_name_na_shto = ekwip_name_na_shto
        self.xit_boks = xit_boks

        self.izb = izb
        self.izb_two_hend = izb_two_hend 

        self.hp_raz()



    def hp_raz(self):
        for rect in self.xit_boks:
           v_h = (rect.width // 10)  * (rect.height // 10) * self.tolshina 

           self.v += v_h 
           self.hp += v_h * self.kof_hp_material_strength


    def draw(self , skeen):
        for xit in self.xit_boks:
            pygame.draw.rect(skeen, (200, 20, 200), xit  )

    
    def damage_calculation(self, tolsh , S  , tipe_faza , efc_value , P_loss ):     
        print(f"\n---------- Hp faza {tipe_faza} ----------")

        if tipe_faza == "penetration":
            volume_destruction =  tolsh * S 
            self.v = max(0, self.v - volume_destruction)

            self.masa = self.v * self.plotnost

            hp_loss = volume_destruction * efc_value
            print(f"    | volume_destruction: {volume_destruction} | tolsh: {tolsh} | S: {S} | efc_value: {efc_value}")

        else:
            hp_loss = (P_loss / max(self.tolshina, 0.5)) * efc_value
            print(f"    |  P_loss: {P_loss} | tolsh: {tolsh} | S: {S} | efc_value: {efc_value}")


        self.hp = max(0, self.hp - hp_loss)


        print(f"    || hp: {self.hp} | hp_max: {self.hp_max} | hp_loss: {hp_loss}")
    

        print(f"-------- Hp finished {tipe_faza} --------\n")


