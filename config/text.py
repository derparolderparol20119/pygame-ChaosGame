
from random import *
import math


#class Wepon():
#    def __init__(self , name  , masa , predel_deformacion  ,  twerdost , hp  , contact_area , len , hit_point):
#        self.name = name 
#
#        self.predel_deformacion =  predel_deformacion
#        self.twerdost = twerdost 
#
#        self.hp = hp 
#        self.hp_max = self.hp
#
#        self.contact_area = contact_area # м
#        self.len = len # м
#        self.hit_point = hit_point # м
#        self.masa = masa # кг 
#
#
#    def calculet_Ek(self):
#        m = self.masa
#        L = self.len
#        r = self.hit_point
#
#        randon_range_grad = randint(160 , 190 )
#        theta = math.radians(randon_range_grad)
#
#        # время разгона зависит от силы
#        
#        base_time = randint(1 , 2) * 0.1
#
#
#        delta_t = base_time / (1 + 0.05 )
#
#        omega = theta / delta_t
#        v = omega * r
#
#        # момент инерции (как стержень)
#        I = (1/3) * m * L**2
#
#        m_eff = I / (r**2)
#
#        Ek = 0.5 * m_eff * v**2
#
#        # площадь контакта уменьшается от ловкости
#        S = self.contact_area / (1 + 0.03)
#
#        impulse = m_eff * v
#
#        Ek = round(Ek , 2)
#        S = round(S , 6)
#        I = round(I , 6)
#        m_eff = round(m_eff , 5)
#        impulse = round(impulse , 5)
#
#        
#        return Ek , S , I , randon_range_grad , base_time , m_eff , impulse
#
#
#
#
#class Armor():
#    def __init__(self):
#        self.name 
#        self.masa
#
#        self.predel_deformacion 
#        self.predel_razrushenia 
#        self.ydarna_vazkost 
#        self.twerdost
#        self.tolshina 
#
#        self.hp
#        self.hp_max = self.hp
#
#    def rashet_broni_damage(self , type_damage , ploshad , damage , name ,  brona , twerdost , orugue , bron_osnw):
#        ploshad_koef = ploshad 
#        if type_damage == "pronikaushi":
#            broneprobitie = damage / ploshad
#
#            if broneprobitie >= (brona.pron_s * brona.tolshina + brona.twerdost):
#                rasnica = (brona.pron_s * brona.tolshina + brona.twerdost) - broneprobitie
#
#                if rasnica <= 0:
#
#                    if twerdost > brona.twerdost:
#                        yron_proshol = max(0,damage - (brona.pron_s * brona.tolshina + twerdost))
#
#                        yron_proshol *= ploshad_koef
#                        brona.proshnost -= yron_proshol
#
#                    else:
#                        yron_proshol = max(0,damage - (brona.pron_s * brona.tolshina))
#
#                        yron_proshol *= ploshad_koef
#                        orugue.proshost -= yron_proshol
#
#                    self.rashet_pizdula_dla_broni(yron_proshol, "pronikaushi", name , bron_osnw)
#                    return yron_proshol , "pronikaushi"
#
#                else:
#                    kin_proc = max(0, 10 - rasnica)
#                    kin_proc = min(kin_proc, 10)
#                    kin_proc *= 10
#
#                    kin_damage = damage * (kin_proc / 100)
#
#                    if damage > (brona.twerdost * brona.tolshina):
#                        yron_proshol = max(0,damage - max(0, kin_damage * brona.tolshina - brona.twerdost))
#
#                    else:
#                        yron_proshol = max(0,damage - (kin_damage * brona.tolshina + brona.twerdost))
#
#                    yron_proshol *= ploshad_koef
#                    brona.proshnost -= yron_proshol
#
#                    self.rashet_pizdula_dla_broni(kin_damage, "kinetik", brona, ploshad, name , bron_osnw)
#                    return kin_damage , "kinetik"
#
#            else:
#                if broneprobitie >= (brona.kin_s * brona.tolshina):
#                    damage = damage * 0.5
#
#                    if damage > (brona.twerdost * brona.tolshina):
#                        yron_proshol = max(0,damage - max(0, damage * brona.tolshina - brona.twerdost))
#                    else:
#                        yron_proshol = max(0,damage - (damage * brona.tolshina + brona.twerdost))
#
#                    yron_proshol *= ploshad_koef
#                    brona.proshnost -= yron_proshol
#
#                    self.rashet_pizdula_dla_broni(yron_proshol, "kinetik", brona, name , bron_osnw)
#                    return yron_proshol , "kinetik"
#
#                else:
#                    print(f"{name} не пробил {brona.name}")
#                    return
#
#        elif type_damage == "kinetik":
#            broneprobitie = damage / ploshad
#
#            if broneprobitie >= (brona.kin_s * brona.tolshina):
#                rasnica = (brona.kin_s * brona.tolshina + brona.twerdost) - broneprobitie
#
#                if rasnica <= 0:
#                    if twerdost > brona.twerdost:
#                        yron_proshol = max(0,damage - (brona.kin_s * brona.tolshina + twerdost))
#                        yron_proshol *= ploshad_koef
#                        brona.proshnost -= yron_proshol
#                    else:
#                        yron_proshol = max(0,damage - (brona.kin_s * brona.tolshina))
#                        yron_proshol *= ploshad_koef
#                        orugue.proshost -= yron_proshol
#
#                else:
#                    kin_proc = max(0, 10 - rasnica)
#                    kin_proc = min(kin_proc, 10)
#                    kin_proc *= 10
#
#                    kin_damage = damage * (kin_proc / 100)
#
#                    if damage > (brona.twerdost * brona.tolshina):
#                        yron_proshol = max(0,damage - max(0, kin_damage * brona.tolshina - brona.twerdost))
#
#                    else:
#                        yron_proshol = max(0,damage - (kin_damage * brona.tolshina + brona.twerdost))
#
#                    yron_proshol *= ploshad_koef
#                    brona.proshnost -= yron_proshol
#                    
#
#                self.rashet_pizdula_dla_broni(yron_proshol, "kinetik", brona, name , bron_osnw)
#                return yron_proshol , "kinetik"
#
#            else:
#                print(f"{name} не пробил {brona.name}")
#                return
#            
#
#
#
#sword = Wepon(name = "ашквальд"  , masa = 2 , predel_deformacion = 300  ,  twerdost = 21 , hp = 100  , contact_area = 0.0004 , len = 0.7 , hit_point = 0.6)
#
#
#
#
#for _ in range(5):
#    Ek , S , I , randon_range_grad , base_time , m_eff , impulse = sword.calculet_Ek()
#    print(f"Ek: {Ek} \n S: {S} \n I: {I} \n Rrg: {randon_range_grad} \n time: {base_time} \n m_ef: {m_eff} \n imp: {impulse} \n\n ")


a = 6


if a > 5:
    b = a + 1

else:

    if a < 10 :
        b = a*2

    else:
        b = a - 1


print(b)