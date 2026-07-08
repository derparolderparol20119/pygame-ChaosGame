import pygame
import sys
from data.Maps.katra_tmx import *
from funk.otrisowka_leg_pred import *
from funk.get_bloked_dist_put import * 
from Screen_controller_funk_draw.Screencontroller_layers import *
from Screen_controller_funk_draw.funk_draw import *

import uuid

class ScreenController:
    def __init__(self, screen, base_surface):
        self.screen = screen
        self.base_surface = base_surface
        self.scale = 1.0
        self.min_scale = 0.3
        self.max_scale = 10
        self.cam_x = 0.0
        self.cam_y = 0.0
        self.dragging = False
        self.drag_start_mouse = (0,0)
        self.drag_start_cam = (0,0)
        self.bg_color = (0, 0 , 0)
        self.layer_cache = []
        self.ground_layers = []
        self.ysort_tiles = []   # ← сюда попадут деревья, стены и т.п.


        self._scaled_cache = None
        self._last_scale = None
        self._last_size = None

        self.tile_lookup = None  # быстрый доступ к тайлу по координате
        self.group_cache = None  # кеш групп (дерево уже найдено)
    
        self.ground_chunks = []
        self.chunk_size = 128


    # ---------- Зум ----------
    def zoom_in(self, factor=1.1, mouse_pos=None):
        self._zoom(factor, mouse_pos)


    def zoom_out(self, factor=1.1, mouse_pos=None):
        self._zoom(1/factor, mouse_pos)


    def _zoom(self, factor, mouse_pos):
        old_scale = self.scale
        new_scale = max(self.min_scale, min(self.scale * factor, self.max_scale))
        if mouse_pos is None:
            self.scale = new_scale
            return

        mx, my = mouse_pos
        gx = (mx - self.screen.get_width()/2 + self.cam_x * old_scale) / old_scale
        gy = (my - self.screen.get_height()/2 + self.cam_y * old_scale) / old_scale

        self.scale = new_scale

        self.cam_x = gx - (mx - self.screen.get_width()/2)/self.scale
        self.cam_y = gy - (my - self.screen.get_height()/2)/self.scale


    # ---------- Drag ----------
    def start_drag(self, mouse_pos):
        self.dragging = True
        self.drag_start_mouse = mouse_pos
        self.drag_start_cam = (self.cam_x, self.cam_y)


    def drag(self, mouse_pos):
        if not self.dragging:
            return
        mx, my = mouse_pos
        dx = (mx - self.drag_start_mouse[0]) / self.scale
        dy = (my - self.drag_start_mouse[1]) / self.scale
        self.cam_x = self.drag_start_cam[0] - dx
        self.cam_y = self.drag_start_cam[1] - dy


    def stop_drag(self):
        self.dragging = False


    def draw_world(self,player,dt,spisok_predmetow=None,npcs=None,igrowoe_okrugenie_personag=None,world_move=False,tile=None,unit_list_death=None):
        if npcs is None:
            npcs = []
        if spisok_predmetow is None:
            spisok_predmetow = []
        if unit_list_death is None:
            unit_list_death = []

        self.base_surface.fill((0, 0, 0, 0))
        drawables = []

        # --- GROUND ---
        visible = self.get_visible_world_rect()
        chunk_size = self.chunk_size


        for layer in self.ground_chunks:
            for (cx, cy), surf in layer.items():
                world_x = cx * chunk_size
                world_y = cy * chunk_size

                rect = pygame.Rect(world_x, world_y, chunk_size, chunk_size)

                if visible.colliderect(rect):
                    self.base_surface.blit(surf, (world_x, world_y))


        # --- move area ---
        if tile is not None:
            draw_move_area(
                surface=self.base_surface,
                tiles=tile,
                color=(0, 0, 0, 90),
                units=npcs + [player]
            )

        RenderCont = RenderContext(
            base_surface=self.base_surface,
            player=player,
            npcs=npcs,
            spisok_predmetow=spisok_predmetow,
            unit_list_death=unit_list_death,
            spisok_ostatkow=spisok_ostatkow,
            dt=dt,
            world_move=world_move,
            spis_podswetok_oy_musu=spis_podswetok_oy_musu,
            drawables=drawables , 
            scren_control = self
        )

        RenderSys = RenderSystem()
        RenderSys.add_layer(RenderLayer(name="ostatki", order=1, draw_func=def_spisok_ostatkow))
        RenderSys.add_layer(RenderLayer(name="death", order=10, draw_func=def_unit_list_death))
        RenderSys.add_layer(RenderLayer(name="predmetu", order=10, draw_func=def_spisok_predmetow))
        RenderSys.add_layer(RenderLayer(name="aktiw_karts", order=20, draw_func=def_player_aktiw_cards))
        RenderSys.add_layer(RenderLayer(name="units", order=30, draw_func=def_units_podswetka_itd))
        RenderSys.add_layer(RenderLayer(name="plear", order=30, draw_func=def_plear))
        RenderSys.add_layer(RenderLayer(name="aktiw_cards_finish", order=40, draw_func=def_player_aktiw_cards_finish))
        RenderSys.add_layer(RenderLayer(name="range", order=45, draw_func=def_player_range))
        RenderSys.add_layer(RenderLayer(name="cell_path", order=46, draw_func=def_cell_path))

        visible_rect = self.get_visible_world_rect()
        tile_w = tmx_map.tilewidth
        tile_h = tmx_map.tileheight

        start_x = max(0, int(visible_rect.left // tile_w) * tile_w)
        end_x = int(visible_rect.right // tile_w + 1) * tile_w

        start_y = max(0, int(visible_rect.top // tile_h) * tile_h)
        end_y = int(visible_rect.bottom // tile_h + 1) * tile_h

        # --- visible ysort tiles ---
        for x in range(start_x, end_x, tile_w):
            for y in range(start_y, end_y, tile_h):
                pos = (x, y)

                if pos not in self.tile_lookup:
                    continue

                for t in self.tile_lookup[pos]:
                    drawables.append((
                        t["rect"].bottom,
                        LAYER_WORLD,
                        {
                            "type": "tile",
                            "image": t["image"],
                            "pos": t["image_rect"].topleft,
                            "rect": t["rect"],
                            "id": t["id"],
                            "layer_name": t["layer_name"],
                            "world_pos": t["world_pos"]
                        }
                    ))

        RenderSys.draw(RenderCont)

        # единый y-sort внутри мира
        drawables.sort(key=lambda x: (x[1], x[0]))

        TARGET_LAYER = {
            "ysort_houses", "ysort_houses2",
            "ysort_stena", "ysort_stena2",
            "ysort_stena3", "ysort_stena4"
        }

        LAYER_ALPHA = {
            "ysort_houses": 50,
            "ysort_houses2": 50,
            "ysort_stena": 160,
            "ysort_stena2": 160,
            "ysort_stena3": 160,
            "ysort_stena4": 160,
        }

        transparent_trees = {}

        # --- find transparent tiles ---
        for _, _, obj in drawables:
            if obj["type"] != "tile":
                continue

            if obj["layer_name"] not in TARGET_LAYER:
                continue

            if player.feet_rect.colliderect(obj["rect"]):
                for t in self.get_tile_group(obj):
                    alpha = LAYER_ALPHA.get(t["layer_name"], 120)
                    if t["id"] in transparent_trees:
                        transparent_trees[t["id"]] = min(transparent_trees[t["id"]], alpha)
                    else:
                        transparent_trees[t["id"]] = alpha

            if npcs:
                for npc in npcs:
                    if npc.feet_rect.colliderect(obj["rect"]):
                        for t in self.get_tile_group(obj):
                            alpha = LAYER_ALPHA.get(t["layer_name"], 120)
                            if t["id"] in transparent_trees:
                                transparent_trees[t["id"]] = min(transparent_trees[t["id"]], alpha)
                            else:
                                transparent_trees[t["id"]] = alpha

        # --- normal draw ---
        for _, _, obj in drawables:
            if obj["type"] == "image":
                self.base_surface.blit(obj["image"], obj["pos"])

            elif obj["type"] == "object":
                obj["obj"].draw(self.base_surface, dt, world_move, self)

            elif obj["type"] == "tile":
                if obj["id"] not in transparent_trees:
                    self.base_surface.blit(obj["image"], obj["pos"])


        # --- transparent tiles ---
        for _, _, obj in drawables:
            if obj["type"] == "tile" and obj["id"] in transparent_trees:
                img = obj["image"]
                old_alpha = img.get_alpha()

                img.set_alpha(transparent_trees[obj["id"]])
                self.base_surface.blit(img, obj["pos"])
                img.set_alpha(old_alpha)


    def draw_to_screen(self):

        self.screen.fill(self.bg_color)

        # видимая область мира
        visible = self.get_visible_world_rect()

        map_rect = self.base_surface.get_rect()
        visible = visible.clip(map_rect)

        if visible.width <= 0 or visible.height <= 0:
            return

        # берем только видимую часть
        sub = self.base_surface.subsurface(visible)

        # масштаб
        scaled_w = int(visible.width * self.scale)
        scaled_h = int(visible.height * self.scale)

        scaled = pygame.transform.scale(sub, (scaled_w, scaled_h))

        # позиция камеры на экране
        center_x = self.screen.get_width() / 2
        center_y = self.screen.get_height() / 2

        screen_x = (visible.x - self.cam_x) * self.scale + center_x
        screen_y = (visible.y - self.cam_y) * self.scale + center_y

        self.screen.blit(scaled, (int(screen_x), int(screen_y)))


    def build_layer_cache(self):
        for layer in tmx_map.visible_layers:
            if not hasattr(layer, "tiles"):
                continue

            if layer.name.startswith("ground"):
                chunk_size = self.chunk_size
                chunks = {}

                for x, y, tile in layer.tiles():
                    world_x = x * tmx_map.tilewidth
                    world_y = y * tmx_map.tileheight

                    chunk_x = world_x // chunk_size
                    chunk_y = world_y // chunk_size

                    key = (chunk_x, chunk_y)

                    if key not in chunks:
                        surf = pygame.Surface((chunk_size, chunk_size), pygame.SRCALPHA)
                        chunks[key] = surf

                    surf = chunks[key]

                    local_x = world_x % chunk_size
                    local_y = world_y % chunk_size

                    surf.blit(tile, (local_x, local_y))

                self.ground_chunks.append(chunks)


            elif layer.name.startswith("ysort"):
                for x, y, tile in layer.tiles():
                    tile = tile.convert_alpha()

                    world_x = x * tmx_map.tilewidth
                    world_y = y * tmx_map.tileheight

                    image_rect = tile.get_rect(topleft=(world_x, world_y))

                    ysort_rect = pygame.Rect(
                        world_x,
                        world_y + tmx_map.tileheight - 5,
                        image_rect.width,
                        16
                    )

                    self.ysort_tiles.append({
                        "id": uuid.uuid4(),
                        "image": tile,
                        "image_rect": image_rect,
                        "rect": ysort_rect,
                        "world_pos": (world_x, world_y),
                        "layer_name": layer.name
                    })

        self.tile_lookup = {}
        for t in self.ysort_tiles:
            self.tile_lookup.setdefault(t["world_pos"], []).append(t)

        self.group_cache = {}

    def screen_to_world(self, sx, sy):
    
        center_x = self.screen.get_width() / 2
        center_y = self.screen.get_height() / 2
    
        world_x = (sx - center_x) / self.scale + self.cam_x
        world_y = (sy - center_y) / self.scale + self.cam_y
    
        return world_x, world_y


    def get_tile_group(self, start_tile):
        key = start_tile["id"]

        if key in self.group_cache:
            return self.group_cache[key]

        stack = [start_tile]
        visited = set()
        group = []

        tile_w = tmx_map.tilewidth
        tile_h = tmx_map.tileheight

        while stack:
            t = stack.pop()

            if t["id"] in visited:
                continue

            visited.add(t["id"])
            group.append(t)

            x, y = t["world_pos"]

            for dx, dy in ((tile_w, 0), (-tile_w, 0), (0, tile_h), (0, -tile_h)):
                np = (x + dx, y + dy)

                if np not in self.tile_lookup:
                    continue

                for nt in self.tile_lookup[np]:
                    if nt["layer_name"] != start_tile["layer_name"]:
                        continue

                    if nt["id"] not in visited:
                        stack.append(nt)

        for t in group:
            self.group_cache[t["id"]] = group

        return group


    def get_visible_world_rect(self):

        world_left, world_top = self.screen_to_world(0, 0)

        world_right, world_bottom = self.screen_to_world(
            self.screen.get_width(),
            self.screen.get_height()
        )

        rect = pygame.Rect(
            int(world_left),
            int(world_top),
            int(world_right - world_left),
            int(world_bottom - world_top)
        )

        rect.clamp_ip(self.base_surface.get_rect())

        return rect



#pygame.draw.line(
#    self.base_surface,
#    (255, 255, 0),
#    (0, player.feet_rect.bottom),
#    (self.base_surface.get_width(), player.feet_rect.bottom),
#    1
#) # важно для перекрытий
#for t in self.ysort_tiles:
#    pygame.draw.rect(
#        self.base_surface,
#        (0, 0, 255),
#        t["rect"],
#        1
#    ) # важно для перекрытий
