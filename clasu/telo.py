import pygame
import math
from clasu.DamageProcessor import *
from copy import deepcopy
# вывод урон если попал в кожу или кость урона по телу мало основное ето потеря крови и выведение органов 



class Osnowa():
    def __init__(self , name , koneshonsti , x , y , influence_attributes_list , parametrs = []):  
        self.name = name
        self.hp = 0
        self.hp_max = 0

        self.slotu_broni = None

        self.koneshonsti = koneshonsti 
        self.x = x 
        self.y = y 
        self.influence_attributes_list = influence_attributes_list
        self.influence_attributes_list_ready = []
        self.efficiency = 0

        self.parametrs = parametrs


    def perebor_koneshnostei(self):
        self.influence_attributes_list_ready = []
        self.hp = 0

        if self.hp_max == 0:
            for kon in self.koneshonsti:
                self.hp += round(kon.hp , 2)
                self.hp_max += round(kon.hp_max , 2)
                slw_inf = kon.influence_update()
                self.influence_attributes_list_ready.append(slw_inf)

        else:
            for kon in self.koneshonsti:
                self.hp += round(kon.hp , 2)
                slw_inf = kon.influence_update()
                self.influence_attributes_list_ready.append(slw_inf)
    

        self.update_influence()


    def update_influence(self):
        if self.hp != 0 :
            self.efficiency = self.hp / self.hp_max

            for attrubut in self.influence_attributes_list:
                self.influence_attributes_list_ready.append({
                    "name":attrubut.name,
                    "meaning":attrubut.meaning * self.efficiency,
                    "vliaet_na_shto":attrubut.vliaet_na_shto,
                    "znak":attrubut.znak
                })






class Limb(DamageProcessor):
    DEFAULTS = {
        "name": "no name",
        "tip": "tkani",
        "glubina": 0,
        "bodi_rekt": pygame.Rect(0, 0, 0, 0),
        "x": 0,
        "y": 0,
        "fabric_depth": 0,
        "parent": None,
        "draw_lear_telo": 0,
        "izb": None,
        "izb_tip_b": None,
        "slots_ekwip": [],
        "influence":None,
        

        #Processor
        "tolshina": 5,
        "plotnost": 10,
        "kof_hp_material_strength": 1.0,
        "increasing_contact_pr": 1.0,
        "increasing_contact_kn": 1.0,
        "impulse_damping": 0.3,
        "twerdost": 5,
        "spr_wozdeistwiam_test": {
            "режущий":[5 , 2.2 ] ,  
            "дробящий": [6 , 2 ]  ,       
            "колющий":[3 , 1.5 ] ,  
        },
        "spr_wozdeistwiam_impuls": { 
            "дробящий": [6 , 0.8 ]  ,       
        },
        "softening_prn": 1,
        "contact_profile": 1

        }
    
    def __init__(self, **kwargs):
        data = deepcopy(self.DEFAULTS)

        # Обновляем тем, что передали
        for key, value in kwargs.items():
            if isinstance(value, (dict, list, set)):
                data[key] = deepcopy(value)
            else:
                data[key] = value

        # Проверка на мусорные ключи
        unknown_keys = set(kwargs) - set(self.DEFAULTS)
        if unknown_keys:
            raise TypeError(f"Неизвестные параметры Limb: {unknown_keys}")

        # Передаем нужное в родителя
        super().__init__(
            data["name"],
            data["tolshina"],
            data["plotnost"],
            data["kof_hp_material_strength"],
            data["increasing_contact_pr"],
            data["increasing_contact_kn"],
            data["impulse_damping"],
            data["twerdost"],
            data["spr_wozdeistwiam_test"],
            data["spr_wozdeistwiam_impuls"],
            data["softening_prn"],
            data["contact_profile"]
        )

        # Limb поля
        self.tip = data["tip"]
        self.glubina = data["glubina"]  # позиция рисования
        self.bodi_rekt = data["bodi_rekt"]
        self.x = data["x"]
        self.y = data["y"]
        self.fabric_depth = data["fabric_depth"]

        self.tek_rana = []

        self.parent = data["parent"]
        self.children = []

        self.destroyed = False
        self.draw_lear_telo = data["draw_lear_telo"]
        self.influence = data["influence"]

        self.izb = data["izb"]
        self.izb_tip_b = data["izb_tip_b"]

        # Защита от общей ссылки
        self.slots_ekwip = deepcopy(data["slots_ekwip"]) if data["slots_ekwip"] is not None else []

        self.base_stats = {
            "plotnost": self.plotnost,
            "kof_hp_material_strength": self.kof_hp_material_strength,
            "increasing_contact_pr": self.increasing_contact_pr,
            "increasing_contact_kn": self.increasing_contact_kn,
            "impulse_damping": self.impulse_damping,
            "twerdost": self.twerdost,
            "spr_wozdeistwiam_test": deepcopy(self.spr_wozdeistwiam_test),
            "spr_wozdeistwiam_impuls": deepcopy(self.spr_wozdeistwiam_impuls),
            "softening_prn": self.softening_prn,
            "contact_profile": self.contact_profile
        }


        self.hp_raz()

        if self.parent:
            self.parent.children.append(self)

        self.efficiency = 0



    def draw(self , skeen):
        pygame.draw.rect(skeen, (200, 200, 200), self.bodi_rekt, 2)



    def hp_raz(self):
        v_h = int((self.bodi_rekt.width / 10) * (self.bodi_rekt.height / 10) * self.tolshina)

        self.v += v_h 
        self.hp += v_h * self.kof_hp_material_strength
        self.hp_max = self.hp
        #print(self.bodi_rekt.width , self.bodi_rekt.height , self.tolshina , v_h , self.v)



    def destroy(self):
        self.destroyed = True

        # 1️⃣ снимаем предметы
        for slot in self.slots_ekwip:
            if slot["nadetost"] is not None:
                # просто удаляем
                slot["nadetost"] = None

        # 2️⃣ очищаем слоты полностью (по желанию)
        self.slots_ekwip.clear()

        # 3️⃣ уничтожаем детей
        for child in self.children:
            child.destroy()



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

        if self.hp <= 0:
            self.destroy()
    

        print(f"-------- Hp finished {tipe_faza} --------\n")
     
    def influence_update(self):

        #print(self.influence , self.hp , "====___====")

        if self.influence != None and self.hp != 0 :
            
            self.efficiency = self.hp / self.hp_max

            return ({
                "name":self.influence.name,
                "meaning":self.influence.meaning * self.efficiency,
                "vliaet_na_shto":self.influence.vliaet_na_shto,
                "znak":self.influence.znak
            })


    def __deepcopy__(self, memo):
        new = self.__class__.__new__(self.__class__)

        memo[id(self)] = new

        for key, value in self.__dict__.items():

            if isinstance(value, pygame.Surface):
                setattr(new, key, value)
            else:
                setattr(new, key, deepcopy(value, memo))

        return new


class Influence_parameters():
    def __init__(self , name , meaning , vliaet_na_shto , znak ):
        self.name = name
        self.meaning = meaning
        self.vliaet_na_shto = vliaet_na_shto
        self.znak = znak



