from funk.a_star_idti_k_celi import *
from heapq import *
import math 
from collections import deque
import pygame
from config.config import *

from data.Maps.katra_tmx import *

TILE_SIZE = 16
DIRS = [
    (1,0), (-1,0), (0,1), (0,-1),
    (1,1), (-1,1), (1,-1), (-1,-1)
]


def get_move_area(
    start_x, start_y,
    radius,
    map_w, map_h,
    blocked_tiles,
    occupied_tiles
):
    visited = set()
    reachable = set()

    queue = deque()
    queue.append((start_x, start_y, 0))
    visited.add((start_x, start_y))

    def is_blocked(x, y):
        return (x, y) in blocked_tiles or (x, y) in occupied_tiles

    while queue:
        x, y, dist = queue.popleft()

        # круговой радиус (как у тебя)
        if max(abs(x - start_x), abs(y - start_y)) > radius:
            continue

        reachable.add((x, y))

        if dist >= radius:
            continue

        for dx, dy in DIRS:
            nx, ny = x + dx, y + dy

            if not (0 <= nx < map_w and 0 <= ny < map_h):
                continue

            if (nx, ny) in visited:
                continue

            # 🔥 проверка диагонального угла (как в A*)
            if dx != 0 and dy != 0:
                if is_blocked(x + dx, y) or is_blocked(x, y + dy):
                    continue

            if is_blocked(nx, ny):
                continue

            visited.add((nx, ny))
            queue.append((nx, ny, dist + 1))

    return reachable


def draw_move_area(surface, tiles, color=(0, 0, 255, 80), units=None):

    overlay = pygame.Surface((16, 16), pygame.SRCALPHA)
    overlay.fill(color)

    for unit in units:
        if ( unit.aktiv_unit and unit.team == 0 and unit.move_area_ready and (unit.path is None or unit.path == [])):
            for x, y in tiles:
                surface.blit(overlay, (x * 16, y * 16))



def load_blocked_tiles_from_tmx(tmx_map, layer_name="colision"):
    blocked_tiles = set()

    collision_layer = tmx_map.get_layer_by_name(layer_name)

    for y in range(tmx_map.height):
        for x in range(tmx_map.width):
            gid = collision_layer.data[y][x]
            if gid != 0:
                blocked_tiles.add((x, y))

    return blocked_tiles


# 8 направлений
DIRS_8 = [
    (1,0), (-1,0), (0,1), (0,-1),
    (1,1), (-1,1), (1,-1), (-1,-1)
]


def get_available_cells(
    start_x,
    start_y,
    radius,
    map_w,
    map_h,
    blocked_tiles,        # стены TMX
    occupied_tiles,       # занятые юнитами
    allow_target_occupied=False  # можно ли выбирать занятую клетку
):
    visited = set()
    reachable = set()

    queue = deque()
    queue.append((start_x, start_y, 0))
    visited.add((start_x, start_y))

    while queue:
        x, y, dist = queue.popleft()

        if dist > radius:
            continue

        # стартовую не добавляем
        if (x, y) != (start_x, start_y):
            reachable.add((x, y))

        if dist == radius:
            continue

        for dx, dy in DIRS_8:
            nx, ny = x + dx, y + dy

            # границы карты
            if not (0 <= nx < map_w and 0 <= ny < map_h):
                continue

            if (nx, ny) in visited:
                continue

            # стена
            if (nx, ny) in blocked_tiles:
                continue

            # запрет среза угла (ВАЖНО)
            if dx != 0 and dy != 0:
                if (x + dx, y) in blocked_tiles or (x, y + dy) in blocked_tiles:
                    continue

            # занято другим юнитом
            if (nx, ny) in occupied_tiles:
                # если разрешаем выбрать занятую — не распространяемся дальше
                if allow_target_occupied:
                    reachable.add((nx, ny))
                continue

            visited.add((nx, ny))
            queue.append((nx, ny, dist + 1))

    return reachable



def has_line_of_sight(x0, y0, x1, y1, blocked_tiles):
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    x = x0
    y = y0

    n = 1 + dx + dy

    x_inc = 1 if x1 > x0 else -1
    y_inc = 1 if y1 > y0 else -1

    error = dx - dy

    dx *= 2
    dy *= 2

    for _ in range(n):

        if (x, y) in blocked_tiles and (x, y) != (x0, y0):
            return False

        if error > 0:
            x += x_inc
            error -= dy
        else:
            y += y_inc
            error += dx

    return True


def get_attack_cells(start_x, start_y, radius, blocked_tiles, shape="circle"):

    visible = set()

    map_w = tmx_map.width
    map_h = tmx_map.height

    def blocked(x, y):
        return (x, y) in blocked_tiles

    def in_map(x, y):
        return 0 <= x < map_w and 0 <= y < map_h

    def cast_light(cx, cy, row, start_slope, end_slope, radius,
                   xx, xy, yx, yy):

        if start_slope < end_slope:
            return

        radius_sq = radius * radius

        for i in range(row, radius + 1):

            dx = -i - 1
            dy = -i
            blocked_flag = False
            new_start = start_slope

            while dx <= 0:
                dx += 1

                X = cx + dx * xx + dy * xy
                Y = cy + dx * yx + dy * yy

                l_slope = (dx - 0.5) / (dy + 0.5)
                r_slope = (dx + 0.5) / (dy - 0.5)

                if start_slope < r_slope:
                    continue
                elif end_slope > l_slope:
                    break

                if not in_map(X, Y):
                    continue

                dist_sq = dx*dx + dy*dy

                if shape == "circle":
                    if dist_sq <= radius_sq:
                        visible.add((X, Y))
                else:
                    if max(abs(X-cx), abs(Y-cy)) <= radius:
                        visible.add((X, Y))

                if blocked_flag:
                    if blocked(X, Y):
                        new_start = r_slope
                        continue
                    else:
                        blocked_flag = False
                        start_slope = new_start
                else:
                    if blocked(X, Y) and i < radius:
                        blocked_flag = True
                        cast_light(cx, cy, i + 1, start_slope, l_slope,
                                   radius, xx, xy, yx, yy)
                        new_start = r_slope

            if blocked_flag:
                break


    multipliers = [
        (1,0,0,1),
        (0,1,1,0),
        (0,1,-1,0),
        (1,0,0,-1),
        (-1,0,0,-1),
        (0,-1,-1,0),
        (0,-1,1,0),
        (-1,0,0,1)
    ]

    for xx,xy,yx,yy in multipliers:
        cast_light(start_x, start_y, 1, 1.0, 0.0, radius, xx, xy, yx, yy)

    visible.discard((start_x, start_y))

    return visible