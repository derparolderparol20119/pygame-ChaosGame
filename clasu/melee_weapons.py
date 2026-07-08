import pygame
#from data.zag_w_igru.zagruzka_test import *
#from funk.bar_poloski_spr import *
from math import *
from random import *


standart_anim1 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\aset_animeted_wepon\standart_wepon_anim\st_1.png').convert_alpha() 
standart_anim2 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\aset_animeted_wepon\standart_wepon_anim\st_2.png').convert_alpha() 
standart_anim3 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\aset_animeted_wepon\standart_wepon_anim\st_3.png').convert_alpha() 

standart_anim4 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\aset_animeted_wepon\standart_wepon_anim\stw_1.png').convert_alpha() 
standart_anim5 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\aset_animeted_wepon\standart_wepon_anim\stw_2.png').convert_alpha() 



class Melee_weapons():
    def __init__(self , name , tip ,  hp , hp_max  , length , hit_point ,  contact_area  , izb , izb_na_sheloweke , spisok_shastei_wepon  , masa , twerdost , two_handed , influence_attributes , influence_skills , possession_weapons = None , minimum_limit = None , 
                 draw_layer = None , rotation_angle = None ,  animations = {"side": [standart_anim1, standart_anim2, standart_anim3], "vertical": [standart_anim4, standart_anim5],"diagonal": [standart_anim4, standart_anim5]}   ):
        

        self.name = name
        self.tip = tip 
        self.hp = hp
        self.hp_max = hp_max 
        self.izb = izb
        self.izb_na_sheloweke = izb_na_sheloweke

        self.spisok_shastei_wepon = spisok_shastei_wepon
        self.masa = masa
        self.twerdost = twerdost 
        self.two_handed = two_handed

        self.length = length # длинна оружыя всего
        self.hit_point = hit_point # длинна от руки до кончика 
        self.contact_area = contact_area  # площядь контакта 0.00005 


        self.influence_attributes = influence_attributes
        self.influence_skills = influence_skills

        self.possession_weapons = possession_weapons
        self.minimum_limit = round(self.masa * self.hit_point * 2)

        self.rotation_angle = rotation_angle

        self.draw_layer = draw_layer
        self.sprawka_text = [
        {"text":"Надеть","funk":"sprawka_nadet",},
        {"text":"Снять","funk":"sprawka_snat"},
        {"text":"Выбросить","funk":"vubrosit"}
        ]

        self.animations = animations

        self.impact_time = None

        self.hero = None


    def eqwip(self, character, poz_x_y, wuborka_ydal):

        slots_to_equip = []

        for elem in self.spisok_shastei_wepon:

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


    def eqwip_techn(self, character ):
        slots_to_equip = []

        for elem in self.spisok_shastei_wepon:

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



    def ybrat_iz_inwentor(self, plear, poz , wuborka_ydal):
        plear.delit_predmet_iz_inw(poz , wuborka_ydal)



    def wuzow_sprawki(self, screen, x, y, font):
        x += 13
        y += 13

        PART_H = 70
        WIDTH = 230
        HEADER_H = 45

        height = HEADER_H + len(self.spisok_shastei_wepon) * PART_H + 6

        # ---------- ФОН ----------
        bg = pygame.Surface((WIDTH, height), pygame.SRCALPHA)
        pygame.draw.rect(bg, (35, 35, 35, 150), bg.get_rect())
        screen.blit(bg, (x, y))
        pygame.draw.rect(screen, (95, 95, 95), (x, y, WIDTH, height), 1)

        # ---------- ЗАГОЛОВОК ----------
        screen.blit(font.render(self.name, True, (170, 190, 220)), (x + 6, y + 4))
        screen.blit(
            font.render(f"Масса: {self.masa}", True, (180, 180, 180)),
            (x + 6, y + 24),
        )

        cy = y + HEADER_H

    def skils_influence(self):
        podxodit = {'сила': 0, 'скорость': 0, 'моторика': 0}

        for skil in self.hero["hero"].sklil_list:
            for teg , slowar in skil.influence_parameters.items(): 
                if teg in self.influence_skills:
                    for key, value in slowar.items():
                        if key in podxodit:
                            podxodit[key] += skil.value * skil.interest_level * value
                        else:
                            print(f"Навык {skil.name} имеет неизвестный параметр {key} для расчета времени удара. пошол нах !!!")
                            
                            
                if teg == "All":
                    for key, value in slowar.items():
                        if key in podxodit:
                            podxodit[key] += skil.value * skil.interest_level * value
                        else:
                            print(f"Навык {skil.name} имеет неизвестный параметр {key} для расчета времени удара. пошол нах !!!")

        return podxodit


    def calculations_imapct_time(self , pdo):
        speed_bonus = 0
        osnova_ti = self.hero["osnova"]

        for param in osnova_ti.parametrs:

            if param.name == "скорость":

                speed_bonus = (
                    param.value *
                    self.influence_attributes.get("скорость", 0) * 15 * (1 + pdo["скорость"] / 100)
                )

                break

        base_time = 0.5 + self.masa * 0.15

        self.impact_time = base_time / (1 + speed_bonus / 20)

    def damage_calculations(self):
        sila_bonus = 0

        pdo = self.skils_influence()
        self.calculations_imapct_time(pdo)

        osnova_ti = self.hero["osnova"]

        for param in osnova_ti.parametrs:

            if param.name == "сила":

                sila_bonus = (
                    param.value * self.influence_attributes.get("сила", 0) * 17 * (1 + pdo["сила"] / 100)
                )

                break

        # эффективная масса оружия
        effective_mass = self.masa * (1 + sila_bonus / 50)

        # скорость удара
        v = (1 / max(0.1, self.impact_time)) * (1 + self.length * 0.2)

        # энергия
        Ek = 0.5 * effective_mass * v**2


        # импульс
        P = effective_mass * v


        print(
            f"{self.name} | "
            f"mass={self.masa} "
            f"eff_mass={effective_mass:.2f} "
            f"v={v:.2f} "
            f"Ek={Ek:.2f} "
            f"P={P:.2f}"
        )

        return {
            "Ek": Ek,
            "P": P,
            "S": self.contact_area,
            "object": self,
            "twerdost": self.twerdost
        }


    def sprawka_nadet(self , parts , poz_x_y ,  wuborka_ydal):
        self.eqwip(parts ,  poz_x_y , wuborka_ydal)


    def sprawka_snat(self , parts ,  poz_x_y , wuborka_ydal ):
        self.unequip(parts ,  poz_x_y , wuborka_ydal)


    def vubrosit(self , plear , poz, wuborka_ydal):
        plear.wubrosit_iz_inwentar(poz , wuborka_ydal , self)




class Elem_wepon():
    def __init__(self , name ,  ekwip_name , ekwip_name_na_shto ):
        self.name = name
        self.ekwip_name = ekwip_name
        self.ekwip_name_na_shto = ekwip_name_na_shto

    def draw(self , skeen):
        pass



#self.attribute_dependence = [{
#    "сила":1.5,
#    "ловкости":1.0
#    ""
#
#                    
#
#
#                    }]

def raz_gad(Ek , S , skill_bonus , self  ):
    sigma_hit = Ek / (S * self.penetration_depth)

    if sigma_hit > self.material_resistance:
        penetration_coeff = 1
    else:
        penetration_coeff = sigma_hit / self.material_resistance

    damage = Ek * penetration_coeff + skill_bonus

    return damage