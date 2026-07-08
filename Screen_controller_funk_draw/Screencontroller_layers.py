
class RenderLayer:
    def __init__(self, name, order, draw_func):
        self.name = name
        self.order = order
        self.draw_func = draw_func



class RenderSystem:
    def __init__(self):
        self.layers = []

    def add_layer(self, layer):
        self.layers.append(layer)
        self.layers.sort(key=lambda l: l.order)

    def draw(self, context):
        for layer in self.layers:
            layer.draw_func(context)





class RenderContext:
    def __init__(self, base_surface, player, npcs, spisok_predmetow, unit_list_death, spisok_ostatkow, dt, world_move, spis_podswetok_oy_musu, drawables , scren_control):
        self.base_surface = base_surface
        self.player = player
        self.npcs = npcs
        self.spisok_predmetow = spisok_predmetow
        self.unit_list_death = unit_list_death
        self.spisok_ostatkow = spisok_ostatkow

        self.dt = dt
        self.world_move = world_move
        self.spis_podswetok_oy_musu = spis_podswetok_oy_musu
        self.drawables = drawables

        self.scren_control = scren_control

    def add_image(self, y, layer, surface, x, y_pos):
        self.drawables.append((
            y,
            layer,
            {
                "type": "image",
                "image": surface,
                "pos": (x, y_pos)
            }
        ))

    def add_object(self, y, layer, obj):
        self.drawables.append((
            y,
            layer,
            {
                "type": "object",
                "obj": obj
            }
        ))

