import math
from random import *


class DamageProcessor:
    def __init__(self, name , tolshina , plotnost , kof_hp_material_strength , increasing_contact_pr , increasing_contact_kn , impulse_damping , twerdost , spr_wozdeistwiam_test , spr_wozdeistwiam_impuls , softening_prn , contact_profile ):
        self.name = name

        self.tolshina = tolshina 
        self.plotnost = plotnost
        
        self.kof_hp_material_strength = kof_hp_material_strength # коэффициент прочности материала для расчета HP

        self.v = 0
        self.hp = 0

        self.v_max = self.v
        self.masa = self.v * self.plotnost
        self.hp_max = self.hp


        self.increasing_contact_pr = increasing_contact_pr # ето типа форма брони выпуклая или как кольчуга сеточная 
        self.increasing_contact_kn = increasing_contact_kn # ето разпределяет импульс по площади в зависимости от типа брони
        self.impulse_damping = impulse_damping # 0.0 - не гасит, 1.0 - полностью гасит

        self.twerdost = twerdost


        self.spr_wozdeistwiam_test = spr_wozdeistwiam_test
        self.spr_wozdeistwiam_impuls = spr_wozdeistwiam_impuls
        self.softening_prn  = softening_prn 

        self.contact_profile = contact_profile


    def process_hit(self, Ek , P , S , S_impuls , object_hit , twerdost , type ):
        print(f"=============================== New hit on {self.name} ===============================")
        print(f"Object {self.name} Ek: {Ek} , P: {P} , S: {S} , type: {type} ")
        S , S_base , S_impuls = self.S_setigs(S , S_impuls)

        kof_tw = round((self.twerdost / twerdost) ** 0.75 , 2 )
        kof_tw = max(0.5, min(kof_tw, 2.0))


        if hasattr(object_hit, "take_damage"): # ето урон оружыю идиоты 
            Ek_wepon = Ek * kof_tw
            object_hit.take_damage(Ek_wepon, "kn")


        print(f"|| self.twerdost: {self.twerdost} || {twerdost}| kof_tw: {kof_tw} ")


        if type == "prn":
            modul_correct , modul_correct_name , spr_value,  damage_percent  = self.modes_calculate(Ek , P , S )
            if modul_correct == None:
                type = "kn"    
            print(f"| {modul_correct_name} | modul_correct: {modul_correct} | spr_value: {spr_value}")


        if type == "prn":
            print(f"|---| type: {type} || S: {S} | S_base: {S_base} | Ek: {Ek} | P: {P}  ")
            Ek , type , P , tolsh_prn = self.calculate_penetration_energy(S, kof_tw , Ek , P , type , damage_percent)
            type , P ,  S_impuls = self.calculate_impuls_energy(S_impuls  , P , type , tolsh_prn , "prn" )

        else: 
            print(f"|---| type: {type} || S_impuls: {S_impuls} | Ek: {Ek} | P: {P}") 
            type , P ,  S_impuls = self.calculate_impuls_energy(S_impuls , P , type , 0 , "kn" )



        if type == "kn":
            print(f"|| итог : Ek: {Ek} | type: {type} | S: {S} | S_base: {S_base} | P: {P}")
            print(f"=============================== final hit on {self.name} ===============================")
            return Ek , type  , S , P , S_impuls
        
        elif type == "prn":
            print(f"|| итог : Ek: {Ek} | type: {type} | S: {S} | S_base: {S_base} |  P: {P}")
            print(f"=============================== final hit on {self.name} ===============================")
            return Ek , type , S_base , P , S_impuls
        
        else:
            print("ошыбка")
            print(f"=============================== final hit on {self.name} ===============================")



    def calculate_penetration_energy(self, S, kof_tw , Ek , P , type , damage_percent):
        Ek_base = Ek
        S_eff = S * (1 + 0.5 * self.contact_profile)

        if S_eff <= 0:
            S_eff = 1
            print(f"    | S_eff was adjusted to avoid non-positive value: {S_eff} ")


        spr_value , efc_value , spr_ef_total = self.percent_translate_int_spr(damage_percent)


        print(f"    | spr_value: {spr_value} | S_eff: {S_eff} | Ek после: {Ek} ")

        spr_perunit = spr_value * S_eff * kof_tw

        max_dm = Ek / spr_perunit
        max_dm = max(0, min(max_dm, self.tolshina))

        spent_energy = spr_value * S_eff * max_dm * kof_tw
        Ek = Ek - spent_energy

        if max_dm >= self.tolshina:
            result_type = "prn"
            tolsh = self.tolshina
            print(f"    | полное пробитие || max_dm: {max_dm} | tolsh: {tolsh} | Ek после: {Ek} ")

        else:
            result_type = "kn"
            tolsh = max_dm



        print(f"    | result_type: {result_type} | tolsh: {tolsh}/{self.tolshina} | Ek после: {Ek} ")
        Ek_loss = Ek_base - Ek
        print(f"    | Ek_loss = {Ek_loss}")


        self.damage_calculation(tolsh , S , "penetration" , efc_value , None )

        if Ek < 0:
            Ek = 0.0
            print(f"Ek == {Ek}.")


        return Ek , result_type , P , tolsh
    


    def calculate_impuls_energy(self, S_impuls,  P , type , tolsh_prn , type_faza):
        print(f"===== impuls ===== \n")
        print(f"| S_impuls: {S_impuls} | type: {type} | tolsh_prn: {tolsh_prn}")
        if S_impuls <= 0:
            S_impuls = 1

        print(f"|---| P: {P} | S_impuls: {S_impuls} ")

        spr_value = self.spr_wozdeistwiam_impuls["дробящий"][0]
        efc_value = self.spr_wozdeistwiam_impuls["дробящий"][1]

        # --- гашение импульса
        P_after , P_loss , tolsh ,  S_impuls = self.impuls_extinction(P , spr_value , S_impuls , tolsh_prn )

        if type_faza == "kn" or tolsh_prn < self.tolshina:
            self.damage_calculation(tolsh , S_impuls  , "impuls" , efc_value , P_loss )

        else:
            pass

        return  type, P_after , S_impuls



    def impuls_extinction(self, P , spr_value, S_impuls , tolsh_prn):
        p_beas = P
        total_tolshina = 0 
        tolsh_prn = tolsh_prn
        tolsh_ost = self.tolshina - tolsh_prn

        growth_rate_kn = self.increasing_contact_kn - 1
        growth_rate_pr = self.increasing_contact_pr - 1

        S_cap = S_impuls * (1 + growth_rate_kn * math.log1p(self.tolshina))

        for _ in range(math.ceil(self.tolshina)):
            if tolsh_prn <= 0 and tolsh_ost > 0:
                if tolsh_ost < 1:
                    factor = tolsh_ost
                else:
                    factor = 1

                damping_p = spr_value * S_impuls * (1 + self.impulse_damping)

                if P >= damping_p:
                    tolsh_ost -= factor 
                    total_tolshina += factor
                    P -= (damping_p * factor)
                    S_impuls += (S_cap - S_impuls) * growth_rate_kn * factor

                else:
                    min_damping_p = damping_p * 0.1 
                    max_proiti = P / min_damping_p
                    max_proiti_nrm = max_proiti * 0.1

                    total_tolshina += max_proiti_nrm       
                    S_impuls += (S_cap - S_impuls) * growth_rate_kn * factor

                    P_after = 0
                    print(f"    | damping_p: {damping_p} | spr_value: {spr_value} | self.impulse_damping: {self.impulse_damping} ")
                    print(f"    | Impulse fully OST zone | total_tolshina: {total_tolshina} | P_after: {P_after}/{p_beas} | S_impuls: {S_impuls:.2f} ")
                    return P_after , p_beas , total_tolshina , S_impuls

            else:
                if tolsh_prn < 1:
                    factor = tolsh_prn
                else:
                    factor = 1
                damping_p = (spr_value * S_impuls * self.softening_prn) * (1 + self.impulse_damping)

                if P >= damping_p:
                    tolsh_prn -= factor
                    total_tolshina += factor
                    P -= (damping_p * factor)
                    S_impuls += (S_cap - S_impuls) * growth_rate_pr * factor

                else:
                    min_damping_p = damping_p * 0.1
                    max_proiti = P / min_damping_p
                    max_proiti_nrm = max_proiti * 0.1

                    total_tolshina += max_proiti_nrm       
                    S_impuls += (S_cap - S_impuls) * growth_rate_pr * factor

                    P_after = 0
                    print(f"    | damping_p: {damping_p} | spr_value: {spr_value} | self.impulse_damping: {self.impulse_damping} ")
                    print(f"    | Impulse fully PRN zone | total_tolshina: {total_tolshina} | P_after: {P_after}/{p_beas} | S_impuls: {S_impuls:.2f} ")
                    return P_after , p_beas , total_tolshina , S_impuls

        print(f"    | damping_p: {damping_p} | spr_value: {spr_value} | self.impulse_damping: {self.impulse_damping} ")
        print(f"    | Impulse fully zone | total_tolshina: {total_tolshina} | P_after: {P}/{p_beas} | S_impuls: {S_impuls:.2f} ")
        return P , p_beas - P , total_tolshina ,  S_impuls                




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



    def modes_calculate(self , Ek , impulse , S , ):
        print(S)
        if Ek <= 0 or impulse <= 0 or S <= 0:
            print("    || Недостаточно данных")
            return None, None, None, None 


        # --- новые score ---
        damage_scores = {}

        print("==== DAMAGE TYPES ====")

        slash_score = Ek / (S ** 0.5) 
        blunt_score = (impulse * 0.4) * (1 + S * 0.1)
        pierce_score = Ek / S  

        damage_scores["режущий"] = slash_score
        damage_scores["дробящий"] = blunt_score
        damage_scores["колющий"] = pierce_score

        data_source = self.spr_wozdeistwiam_test

        modes = {}

        for damage_type, score in damage_scores.items():

            if damage_type not in data_source:
                continue

            spr, efficiency = data_source[damage_type]

            power = (score / spr) * efficiency

            modes[damage_type] = [power, (spr, efficiency)]

            print(
                f"| {damage_type}: "
                f"score={round(score,2)} "
                f"power={round(power,2)}"
            )

        # --- если ничего не прошло ---
        valid = {
            k: v for k, v in modes.items()
            if v[0] >= 0.5
        }

        if not valid:
            print("    || no valid damage type")
            return None, None, None, None 

        modul_correct_name = max(valid , key=lambda k: valid[k][0] )

        modul_correct = valid[modul_correct_name]


        spr_value = modul_correct[1][0]

        # --- проценты смешанного урона ---
        total_score = sum(damage_scores.values())

        damage_percent = {
            k: (v / total_score) * 100
            for k, v in damage_scores.items()
        }

        print("==== DAMAGE PERCENT ====")
        for k, v in damage_percent.items():
            print(f"| {k}: {round(v,1)}%")

        return  modul_correct , modul_correct_name , spr_value,  damage_percent
    


    def percent_translate_int_spr(self , percent ):
        
        van_r = round(percent["режущий"] / 100, 3)
        van_d = round(percent["дробящий"] / 100, 3)
        van_k = round(percent["колющий"] / 100, 3)

        spr_r = self.spr_wozdeistwiam_test["режущий"][0] * van_r
        spr_d = self.spr_wozdeistwiam_test["дробящий"][0] * van_d
        spr_k = self.spr_wozdeistwiam_test["колющий"][0] * van_k

        efc_r = self.spr_wozdeistwiam_test["режущий"][1] * van_r
        efc_d = self.spr_wozdeistwiam_test["дробящий"][1] * van_d
        efc_k = self.spr_wozdeistwiam_test["колющий"][1] * van_k

        efc_value = efc_r + efc_d + efc_k
        spr_value = spr_r + spr_d + spr_k
        spr_ef_total = (spr_r * efc_r ) + (spr_d * efc_d )+ (spr_k * efc_k)

        print(f"    | spr_value: {spr_value} || spr_r: {spr_r} | spr_d: {spr_d} | spr_k: {spr_k} ")
        print(f"    | efc_value: {efc_value} || efc_r: {efc_r} | efc_d: {efc_d} | efc_k: {efc_k} ")

        return round(spr_value , 3) , round(efc_value , 3) , round(spr_ef_total , 3)
    


    def S_setigs(self , S , S_impuls):
        if S <= 0:
            S = 1
        S_base = S
        
        if S_impuls <= 0:
            S_impuls = S

        return S , S_base , S_impuls

