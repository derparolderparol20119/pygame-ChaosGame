import pygame

class Initiative():
    def __init__(self):
        self.xods = []
        self.units = []  # [(unit, color), ...]
        self.units_podswetka = []

    def add_unit(self, unit, color , team):
        self.units.append({
            "unit": unit,
            "color": color,
            "team":team
        })


    def update_xods(self, turns=1):
        if not self.units:
            return

        for _ in range(turns):

            # 1. все накапливают инициативу
            for data in self.units:
                unit = data["unit"]
                unit.bar_iniciatiw += unit.iniciatiw

            # 2. выбираем того, кто дошёл до порога
            data = max(
                self.units,
                key=lambda d: d["unit"].bar_iniciatiw
            )

            unit = data["unit"]

            # 3. фиксируем ход
            self.xods.append(data)

            # 4. сбрасываем шкалу
            unit.bar_iniciatiw = 0


    def draw_initiative_scale(self, kx, ky, surface , x_poz_maus , y_poz_maus):
        offset_x = 0    


        for data in self.xods:
            unit = data["unit"]
            color = data["color"]

            # иконка

            rect_strec_morda = pygame.draw.rect(surface,color,(kx + offset_x, ky, 100, 100),)

            if rect_strec_morda.collidepoint(x_poz_maus , y_poz_maus):
                un_star = unit.podswetka
                unit.podswetka = (True , (235,235,235) , (235,235,235))

                if not any(u == unit for u, r , i in self.units_podswetka):
                    self.units_podswetka.append((unit, rect_strec_morda , un_star))


            for kotr_un_rect in self.units_podswetka:

                if kotr_un_rect[1].collidepoint(x_poz_maus , y_poz_maus):
                    pass
                else:
                    self.units_podswetka.remove(kotr_un_rect)
                    kotr_un_rect[0].podswetka = kotr_un_rect[2]



            surface.blit(unit.ikn_mordu, (kx + offset_x, ky))

            surface.blit(pygame.transform.scale(unit.color_gerb,(unit.color_gerb.get_width()*3, unit.color_gerb.get_height()*3)),(kx + offset_x, ky))
            surface.blit(pygame.transform.scale(unit.stroke_gerb,(unit.stroke_gerb.get_width()*3, unit.stroke_gerb.get_height()*3)),(kx + offset_x, ky))

            pygame.draw.rect(surface,(200 , 200 , 200),(kx + offset_x, ky, 100, 100),2)


            offset_x += 100




    def normalize_initiative(self):     
        # 1️⃣ Удаляем мёртвых
        self.xods = [
            x for x in self.xods
            if not x["unit"].death
        ]

        # 2️⃣ Дозаполняем до 10 ходов
        while len(self.xods) < 10:
            self.update_xods(turns=1)

        # 3️⃣ Обрезаем если больше 10
        self.xods = self.xods[:10]



#self.iniciatiw = 15
#self.bar_iniciatiw = 0 
#self.max_iniciatiw = 100