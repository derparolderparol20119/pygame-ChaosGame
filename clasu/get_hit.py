class Get_hit:
    def __init__(self, name , damage_data , vse_sloi):
        self.name = name 
        self.damage_data = damage_data
        self.vse_sloi = vse_sloi

    def unpacking(self):
        Ek = self.damage_data["Ek"]
        P = self.damage_data["P"]
        S = self.damage_data["S"]
        obj = self.damage_data["object"]
        twerdost = self.damage_data["twerdost"]


        return Ek , P  , S, obj, twerdost

        
    def get_hit(self):

        Ek, P , S , obj, twerdost = self.unpacking()

        print("\n================= НОВЫЙ УДАР =================")
        print(f"Цель: {self.name}")
        print(f"Начальные параметры:")
        print(f"  Ek (энергия): {Ek:.2f}")
        print(f"  P  (импульс): {P:.2f}")
        print(f"  S  (площадь): {S:.6f}")
        print(f"  Твердость оружия: {twerdost}")
        print("==============================================\n")

        layer_index = 0

        S_impuls = S // 2
        type = "prn"

        for sloi in self.vse_sloi:
            layer_index += 1

            print(f"\n------------ СЛОЙ {layer_index}: {sloi.name} ------------")
            print(f"До слоя:")
            print(f"  Ek: {Ek:.2f} | P: {P:.2f} | S: {S:.6f}")

            # вызов твоего нового process_hit
            Ek, type, S, P, S_impuls = sloi.process_hit(
                Ek=Ek,
                P=P,
                S=S,
                S_impuls=S_impuls,
                object_hit=obj,
                twerdost=twerdost,
                type= type
            )

            print(f"После слоя:")
            print(f"  Ek: {Ek:.2f} | P: {P:.2f} | S: {S:.6f} | тип: {type}")
            print("---------------------------------------------------------")

            # остановка если всё поглощено
            if Ek <= 0 and P <= 0:
                print("\n>>> УДАР ПОЛНОСТЬЮ ОСТАНОВЛЕН НА ЭТОМ СЛОЕ <<<")
                break

        print("\n================= ИТОГ =================")
        print(f"Осталось энергии: {Ek:.2f}")
        print(f"Осталось импульса: {P:.2f}")
        print("========================================\n")

        return Ek, P, S


