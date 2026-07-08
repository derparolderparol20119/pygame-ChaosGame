import pygame
import uuid

LAYER_GROUND = 0

LAYER_WORLD_RADIS = 7
LAYER_WORLD_CELL = 8
LAYER_WORLD_ITEM = 9
LAYER_WORLD = 10
LAYER_EFFECT_BELOW = 5
LAYER_EFFECT_ABOVE = 30



def def_spisok_ostatkow(context):
    if not context.spisok_ostatkow:
        return

    for ostatok in context.spisok_ostatkow:
        img, x, y = ostatok
        context.add_image(
            y,
            LAYER_WORLD_ITEM,
            img,
            x - (1 * 16),
            y + (7 * 16)
        )


def def_unit_list_death(context):
    if not context.unit_list_death:
        return

    for unit in context.unit_list_death:
        context.add_object(unit.feet_rect.bottom, LAYER_WORLD_ITEM, unit)


def def_spisok_predmetow(context):
    if not context.spisok_predmetow:
        return

    for item in context.spisok_predmetow:
        context.add_object(item.rect.bottom, LAYER_WORLD_ITEM, item)


def def_player_aktiw_cards(context):
    if context.player.aktiw_cards:
        card = context.player.aktiw_cards[0]
        choice = card.choice_target

        if choice.cache_surface:
            context.add_image(
                choice.draw_pos_y,
                LAYER_EFFECT_BELOW,
                choice.cache_surface,
                choice.draw_pos_x,
                choice.draw_pos_y
            )


def def_units_podswetka_itd(context):
    if not context.npcs:
        return

    if context.player.aktiw_cards:
        card = context.player.aktiw_cards[0]
        choice = card.choice_target
        damage = card.method_damage

        for npc in context.npcs:
            for rect_atak in choice.spisok_cell_atak:

                if npc.xit_boks.colliderect(rect_atak):

                    if not any(u is npc for u, _ in context.spis_podswetok_oy_musu):
                        context.spis_podswetok_oy_musu.append((npc, npc.podswetka))

                        if npc.team is None:
                            npc.podswetka = (True, (235, 235, 235), (235, 235, 235))
                        elif npc.team == 0:
                            npc.podswetka = (True, (70, 120, 255), (50, 30, 15))
                        else:
                            npc.podswetka = (True, (180, 20, 20), (180, 20, 20))

                if damage.animation_tekush >= 1 and not damage.atak_committed:
                    if npc.xit_boks.colliderect(rect_atak):

                        damage.damage_get(choice , context , npc)


            npc.update_rects()
            context.add_object(npc.feet_rect.bottom, LAYER_WORLD, npc)

        if damage.animation_tekush >= 1:
            damage.atak_committed = True

    else:
        for npc in context.npcs:
            npc.update_rects()
            context.add_object(npc.feet_rect.bottom, LAYER_WORLD, npc)


def def_plear(context):
    context.player.update_rects()
    context.add_object(context.player.feet_rect.bottom, LAYER_WORLD, context.player)


def def_player_aktiw_cards_finish(context):
    if context.player.aktiw_cards:
        card = context.player.aktiw_cards[0]
        damage = card.method_damage

        if damage.cache_surface_anima:
            effect_bottom = damage.draw_y2 + damage.cache_surface_anima.get_height()

            context.add_image(
                effect_bottom,
                LAYER_WORLD,
                damage.cache_surface_anima,
                damage.draw_x2,
                damage.draw_y2
            )

            if damage.animation_tekush >= len(damage.animation) + damage.frame_ostatki_na_zemle:
                context.spisok_ostatkow.add((
                    damage.ostatki_na_zemle,
                    damage.draw_x2,
                    damage.draw_y2
                ))


def def_player_range(context):
    pl = context.player
    npcs = context.npcs
    if pl.variable_draw_attack_range == True and pl.attack_range_offset != None:
        context.add_image(
            10,
            LAYER_WORLD_RADIS,
            pl.attack_range_surface,
            pl.attack_range_offset[0],
            pl.attack_range_offset[1]
        )

    for nps in npcs:
        if nps.variable_draw_attack_range == True and nps.attack_range_offset != None:
            context.add_image(
                10,
                LAYER_WORLD_RADIS,
                nps.attack_range_surface,
                nps.attack_range_offset[0],
                nps.attack_range_offset[1]
            )


def def_cell_path(context):
    pl = context.player
    npcs = context.npcs

    for cell in pl.plit_leng :
        context.add_image(
            10,
            LAYER_WORLD_CELL,
            cell["frame"],
            cell["cx"],
            cell["cy"]
        )
    for nps in  npcs:
        if nps.path != (None , []):
            for cell in nps.plit_leng :
                context.add_image(
                    10,
                    LAYER_WORLD_CELL,
                    cell["frame"],
                    cell["cx"],
                    cell["cy"]
                )