# ysort_ , ground , colision


# C:\Users\Oleg\AppData\LocalLow\Sandbox Interactive GmbH\Albion Online Client


# ------------------ CONFIG ------------------
import pygame
import sys
from config.config import *
import math

pygame.init()


#screen = pygame.display.set_mode((1800, 900), pygame.RESIZABLE)
info = pygame.display.Info()
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.SCALED | pygame.NOFRAME )

pygame.display.set_caption("Igra Xaosa")
clock = pygame.time.Clock()


from Screen_controller_funk_draw.ScreenController import *
from clasu.vse_personagu import *
from clasu.dwer import *
from clasu.brona import *
from clasu.inwentori import *
from clasu.sunduk import *
from clasu.sumki import *
from clasu.ItemLying import *
from clasu.parameters import *
from clasu.Ui_interfese import *
from clasu.player_cards import *
from clasu.sqwad import *
from clasu.inicuotiwa import *
from clasu.fight_batle import *
from clasu.character_parameters import *

from funk.draw_hud import *
from funk.a_star_idti_k_celi import *
from funk.sprawka import *
from funk.kwadrat_pod_musko import *
from funk.bar_poloski_spr import *
from funk.otrisowka_leg_pred import *
from funk.dobowlenia_w_spisok import *
from funk.new_unit import *



from data.Maps.katra_tmx import *

from data.game_items.armor.creation_armor import *
from data.game_items.weapons.weapons_sozdanie import *
from data.game_items.living_creatures.liwing_creatures import *
from data.game_items.cards_Haus.cards_haus_sozdanie import *
from data.gaming_assets.dors.dors_zagruzka_izb import *
from data.game_items.coat_of_arms_gerbs.loadind_gerb import *




BASE_W, BASE_H = tmx_map.width * tmx_map.tilewidth, tmx_map.height * tmx_map.tileheight
base_surface = pygame.Surface((BASE_W, BASE_H), pygame.SRCALPHA).convert_alpha()
controller = ScreenController(screen, base_surface )

# ------------------ Init ekwip ------------------

#brona_shampiona2 = ItemLying(x= 100 , y = 25, image = brona_shempion.izb_na_sheloweke , prudmet = brona_shempion , rotate=34 )
#shlem_stai2 = ItemLying(x= 100 , y = 220, image = shlem_stai.izb_na_sheloweke , prudmet = shlem_stai , rotate= 9 )

print(pygame.version.ver)

# ------------------ ПЕРСОНАЖ ------------------



player = Vse_personagu (30, 16, telo_ful_izb , [shelust_izb , shelust_izb_mr1 , shelust_izb_mr1] , sumka_igroka , name= "cvadkovskii" , ikn_mordu =  shadow    )

player.sklil_list.append(reartion )
player.sklil_list.append(sword_obr)
player.sklil_list.append(sword_masa)

player.sozdan_tel()
player.inwentor = inwentar
player.inwentor_add_iasheka([])

inwentar.priwazka_inwentara = player

spisko_dobawitel(player.aktiwator , [atrim , atrim , atrim , atrim , atrim  , atrim , atrim ])


atributu_dla_class_spraw.append((player , player)) 


# ------------------ Ui_interfes ------------------

#ekw_shmot = [pika1 ,  noga_kolushgu ,  stopa_stal , plesho_polkowodca  , pewshatki_nekromanta , shlem_stai  ,  brona_steganka , kirasa_nagrudnik]

# ------------- sqwad uints  ------------------
zanatosti_cletki = []

#new_unit(x  = 34 , y = 35, plear = player, name = "cargon" , telo_ful = telo_ful_izb , izb_mr = [] , trup = trup_izb , shadow = shadows_izb , ekwip_shmot = ekw_shmot )

solider1 = new_unit(x  = 34 , y = 37, plear = player, name = "cargon1" , telo_ful = telo_ful_izb , izb_mr = [shelust_izb , shelust_izb_mr1 , shelust_izb_mr1] , trup = trup_izb , shadow = shadows_izb , ikn_mordu= tereks1 , ekwip_shmot= [gambeson , sword4 , kolshuga , latna_kirasa ]  )
solider2 = new_unit(x  = 36 , y = 35, plear = player, name = "cargon2" , telo_ful = telo_ful_izb , izb_mr = [shelust_izb , shelust_izb_mr1 , shelust_izb_mr1] , trup = trup_izb , shadow = shadows_izb , ikn_mordu= shadow , ekwip_shmot= [gambeson , sword4 , kolshuga])
solider3 = new_unit(x  = 37 , y = 36, plear = player, name = "cargon3" , telo_ful = telo_ful_izb , izb_mr = [shelust_izb , shelust_izb_mr1 , shelust_izb_mr1] , trup = trup_izb , shadow = shadows_izb , ikn_mordu= tereks2 , ekwip_shmot= [gambeson , sword4 ])



soliders11 = Squad_soldier(unit = solider1, priority = 3, role = "pikiner", where_to_go = None, where_to_hit = None)
soliders21 = Squad_soldier(unit = solider2, priority = 1, role = "pikiner", where_to_go = None, where_to_hit = None)
soliders31 = Squad_soldier(unit = solider3, priority = 3, role = "pikiner", where_to_go = None, where_to_hit = None)


# ------------- sqwad ui_interfes fight ------------------


#otrad = Squad(name = "легион смерети", prikaz_liders = None, standard = standarter, squad = [soliders11 , soliders21  , soliders31 ,soliders41 ,soliders51 ,soliders61 ,soliders71 ,soliders81  ,soliders91  ,soliders111 ,soliders121 ,soliders131]  )

skala_iniceatiwa = Initiative()
ui_interfes = Ui_interfes(x = 0  , y = 0 , key_buttun  = None, klilk = None, plear = player , surface = screen , iniciatiw = skala_iniceatiwa ,  controller = controller )
fight = Fight(Ui_interfese = ui_interfes , iniceatiw_skal = skala_iniceatiwa)


#fight.start_batel([[player ] , [solider1 , solider2 , solider3]])

# ------------- init_font ------------------aaac

inwentar.init_font()
obshai.init_font()

font = pygame.font.Font(None, 24)
font2 = pygame.font.Font(None, 21)

# ------------- inwentori init ------------------

spisko_dobawitel(igrowoe_okrugenie_personag , [player , door , sunduk , sunduk2 ])
spisko_dobawitel(predmetu_leg , [])
   
# ----------- build_layer_cache -----------

controller.build_layer_cache()

for sunduk in sunduki.values():
    sunduk.colison_poaw()

# ------------------ ИГРОВОЙ ЦЫКЛ ------------------

print(TILE_SIZE)



while running:
    dt = clock.tick(300)
    
    ne_tuk_po_ikona = False
    parasmert = False
    nashli_item_drag = False
    zapret_ui_interfes = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # wuborka
                mouse_x, mouse_y = event.pos

                if spiok_sprawki:
                    mx, my = pygame.mouse.get_pos()
                    for i in spiok_sprawki:
                        if i.collidepoint(mx, my):
                            klik = i


                if sprawka_parameters.rect_interaction != None and sprawka_parameters.rect_interaction.collidepoint(mouse_x, mouse_y):
                    sprawka_parameters.aktiw_moving = True

                    mouse_x, mouse_y = event.pos

                    sprawka_parameters.offset_x = mouse_x - sprawka_parameters.x
                    sprawka_parameters.offset_y = mouse_y - sprawka_parameters.y
                    
                if sprawka_parameters.rect_interaction != None and sprawka_parameters.del_ikonka.collidepoint(mouse_x, mouse_y):
                    sprawka_parameters.start = False
                    sprawka_parameters.plear = None


                if wind_inwentori and zapret_ui_interfes == False:
                    for winu in wind_inwentori:   # winu = (rect, ikona, inventar)
                        if winu[0] and winu[0].collidepoint(mouse_x, mouse_y):
                            ne_tuk_po_ikona = True
                                          
                            if winu[1].del_ikonka and winu[1].del_ikonka.collidepoint(mouse_x, mouse_y):
                                winu[1].zakruta = True
                                
                            else:
                                peremenshen_musk_kw_sost = True
                                cmeshen_x = mouse_x - winu[1].x
                                cmeshen_y = mouse_y - winu[1].y


                if spisok_iasheki and (wind_inwentori and zapret_ui_interfes == False):
                    mx, my = pygame.mouse.get_pos()

                    for winu in wind_inwentori:
                        inventar = winu[2]       

                        for iasheki in inventar.iasheki:
                            if iasheki.boks_iaseki.collidepoint(mx, my):
                                inventar.wuborka = iasheki  


                    mx, my = pygame.mouse.get_pos()

                    if ikona_wsa and ikona_wsa.collidepoint(mx , my):
                        pass
                    
                    elif ne_tuk_po_ikona == False :
                        if spiok_sprawki:
                            mx, my = pygame.mouse.get_pos()
                            for i in spiok_sprawki:
                                if i.collidepoint(mx, my):
                                    popali_ne_xodit = True   

                        if popali_ne_xodit == False:         
                            wx, wy = controller.screen_to_world(mx, my)
                            if player.aktiw_cards  != None and player.aktiw_animeshon == False : # запуск 
                                if ui_interfes.rect_ne_xodit and ui_interfes.rect_ne_xodit.collidepoint(mouse_x, mouse_y):
                                    pass
                                else:
                                    player.aktiw_animeshon = True
                                    
                            else:
                                if sprawka_parameters.rect_interaction != None and sprawka_parameters.rect_interaction.collidepoint(mouse_x, mouse_y):
                                    pass
                                else:
                                    if ui_interfes.rect_ne_xodit and ui_interfes.rect_ne_xodit.collidepoint(mouse_x, mouse_y):
                                        pass
                                    else:
                                        player.idti_k(wx, wy , units_kletki_zanatu , pretendeimue_kletki )
                

                elif ne_tuk_po_ikona == False and zapret_ui_interfes == False:
                    if spiok_sprawki:
                            mx, my = pygame.mouse.get_pos()
                            for i in spiok_sprawki:
                                if i.collidepoint(mx, my):
                                    popali_ne_xodit = True   

                    if popali_ne_xodit == False:         
                        mx, my = pygame.mouse.get_pos()
                        wx, wy = controller.screen_to_world(mx, my)
                        if player.aktiw_cards != None and player.aktiw_animeshon == False: # запуск 

                            if ui_interfes.rect_ne_xodit and ui_interfes.rect_ne_xodit.collidepoint(mouse_x, mouse_y):
                                pass
                            else:
                                player.aktiw_animeshon = True

                        else:
                            if sprawka_parameters.rect_interaction != None and sprawka_parameters.rect_interaction.collidepoint(mouse_x, mouse_y):
                                pass
                            else:
                                if ui_interfes.rect_ne_xodit and ui_interfes.rect_ne_xodit.collidepoint(mouse_x, mouse_y):
                                    pass
                                else:
                                    player.idti_k(wx, wy , units_kletki_zanatu , pretendeimue_kletki )


                if spis_pridm_spr:
                    for rect, predmet, id_ska, iasheki in spis_pridm_spr:
                        if rect.collidepoint(mx, my):
                        
                            mods = pygame.key.get_mods()
                            if spiok_sprawki:
                                mx, my = pygame.mouse.get_pos()
                                for i in spiok_sprawki:
                                    if i.collidepoint(mx, my):
                                        popali_ne_xodit2 = True   

                            item = (predmet, id_ska, iasheki)


                            if mods & pygame.KMOD_CTRL and popali_ne_xodit2 == False:
                                if item in selected_items:
                                    selected_items.remove(item)   # ← УБРАТЬ
                                else:
                                    selected_items.append(item)   # ← ДОБАВИТЬ


                            drag_group = selected_items.copy()
                            drag_from_iasheki = iasheki
                            mouse_hold = True
                            break


            elif event.button == 2:
                controller.start_drag(event.pos)
                sprawka_aktiw = False
                spiok_sprawki = None
                

            elif event.button == 3:
                mouse_x, mouse_y = event.pos

                if sprawka_parameters.rect_interaction != None and sprawka_parameters.rect_interaction.collidepoint(mouse_x, mouse_y):
                    sprawka_parameters.full_window = not sprawka_parameters.full_window

                if (wind_inwentori and wind_inwentori[0][0]and wind_inwentori[0][0].collidepoint(mouse_x, mouse_y)) or (len(wind_inwentori) > 1 and wind_inwentori[1][0]and wind_inwentori[1][0].collidepoint(mouse_x, mouse_y)):
                    for winu in wind_inwentori : 
                        if winu[0].collidepoint(mouse_x, mouse_y) or (len(winu) > 4 and winu[3].collidepoint(mouse_x, mouse_y)):
                            if winu[1].polna_ikona == False: 
                                winu[1].polna_ikona = True
                            else: 
                                winu[1].polna_ikona = False
                            
                else:
                    mx2 , my2 = pygame.mouse.get_pos()

                    if ikona_wsa and ikona_wsa.collidepoint(mx2 , my2): #
                    
                        if spis_pridm_spr:
                            igrowoe_okrugenie = spis_pridm_spr 

                        else:
                            igrowoe_okrugenie = igrowoe_okrugenie_personag

                    else:
                        igrowoe_okrugenie = igrowoe_okrugenie_personag

                    if player.variable_draw_attack_range == True: ###############################################################################
                        mx3 , my3 = pygame.mouse.get_pos()
                        mx3 , my3  = controller.screen_to_world(mx3 , my3 )
                        for unit in unit_list:
                            if unit.xit_boks.collidepoint(mx3 , my3):
                                unit_ataked_not_sprawka = True
                                for rect_atak in player.unit_attack_range :
                                    if rect_atak.colliderect(unit.xit_boks):
                                        player.hit(unit)


                    if sprawka_parameters.rect_interaction != None and sprawka_parameters.rect_interaction.collidepoint(mouse_x, mouse_y):
                        pass
                       
                    else:
                        if sprawka_aktiw == False and unit_ataked_not_sprawka == False :
                            sprawka_aktiw = True

                        else:
                            sprawka_aktiw = False
                            spiok_sprawki = None


            elif event.button == 4:  
                mx, my = pygame.mouse.get_pos()
                if ikona_wsa and ikona_wsa.collidepoint(mx , my):
                    pass
                    
                else:

                    controller.zoom_in(mouse_pos = event.pos)
                    sprawka_aktiw = False
                    spiok_sprawki = None
                

            elif event.button == 5:  
                mx, my = pygame.mouse.get_pos()
                if ikona_wsa and ikona_wsa.collidepoint(mx , my):
                    pass

                else:

                    controller.zoom_out(mouse_pos = event.pos)
                    sprawka_aktiw = False
                    spiok_sprawki = None


        elif event.type == pygame.MOUSEBUTTONUP:
            peremenshen_musk_kw_sost = False

            if sprawka_parameters.aktiw_moving == True:
                sprawka_parameters.aktiw_moving = False

            if event.button == 2:
                controller.stop_drag()
                sprawka_aktiw = False
                spiok_sprawki = None

            if event.button == 1:
                mouse_hold = False

                if drag_group:
                    mx, my = event.pos

                    for winu in wind_inwentori:
                        inventar = winu[2]

                        for to_iasheki in inventar.iasheki:
                            if to_iasheki.boks_iaseki.collidepoint(mx, my):
                            
                                # нельзя в ту же ячейку
                                if to_iasheki is drag_from_iasheki:
                                    continue
                                
                                # проверка массы
                                total_mass = sum(p.masa for p, _, _ in drag_group)
                                if to_iasheki.current_mass + total_mass <= to_iasheki.masa_max:
                                
                                    # удаляем с конца
                                    for _, idx, _ in sorted(drag_group, key=lambda x: x[1], reverse=True):
                                        del drag_from_iasheki.pridmetu[idx]

                                    # добавляем
                                    for predmet, _, _ in drag_group:
                                        to_iasheki.pridmetu.append(predmet)
                                    
                                    selected_items.clear()
     
                                break

                            elif winu[3] != None and winu[3].collidepoint(mx, my):  
                                mods = pygame.key.get_mods()
                                if not (mods & pygame.KMOD_CTRL):  
                                    to_iasheki = winu[2].wuborka

                                    if to_iasheki is drag_from_iasheki:
                                        continue

                                    total_mass = sum(p.masa for p, _, _ in drag_group)
                                    if to_iasheki.current_mass + total_mass <= to_iasheki.masa_max:

                                        for _, idx, _ in sorted(drag_group, key=lambda x: x[1], reverse=True):
                                            del drag_from_iasheki.pridmetu[idx]

                                        for predmet, _, _ in drag_group:
                                            to_iasheki.pridmetu.append(predmet)

                                        selected_items.clear()

                                    break

                    drag_group = []
                    drag_from_iasheki = None


        elif event.type == pygame.MOUSEMOTION:
            if sprawka_parameters.aktiw_moving == True:
                mouse_x, mouse_y = event.pos

                sprawka_parameters.x = mouse_x - sprawka_parameters.offset_x
                sprawka_parameters.y = mouse_y - sprawka_parameters.offset_y



            if peremenshen_musk_kw_sost and wind_inwentori:
                for winu in wind_inwentori :
                    if winu[0] and winu[0].collidepoint(mouse_x, mouse_y): # wind_inwentori = [(wind_inwentori , ikona , inwentar)]

                        mouse_x, mouse_y = event.pos
                        winu[1].x = mouse_x - cmeshen_x
                        winu[1].y = mouse_y - cmeshen_y

            else:
                controller.drag(event.pos)
                mx, my = pygame.mouse.get_pos()
                if spiok_sprawki:
                    for i in spiok_sprawki:
                        if i.collidepoint(mx, my):
                            pokraska = i
                            break
                        else:
                            pokraska = None

                else:
                    pokraska = None

            if spisok_iasheki:
                spisok_iasheki_poz_x, spisok_iasheki_poz_y = pygame.mouse.get_pos()
                for iasheki in spisok_iasheki:

                    if iasheki.boks_iaseki.collidepoint(spisok_iasheki_poz_x, spisok_iasheki_poz_y):
                        otrisowka_podswetki = (True , spisok_iasheki_poz_x, spisok_iasheki_poz_y , iasheki)
                        break
                    else:
                        otrisowka_podswetki = (False , spisok_iasheki_poz_x , spisok_iasheki_poz_y , iasheki)
                        

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_i:  # 
                if inwentar.zakruta == True:
                    inwentar.zakruta = False
                else:
                    inwentar.zakruta = True


            elif event.key == pygame.K_c and event.mod & pygame.KMOD_SHIFT:
                if player.variable_draw_attack_range == True:
                    player.variable_draw_attack_range = False

                else:
                    player.variable_draw_attack_range = True

                for unit in unit_list:
                    if unit.variable_draw_attack_range == True:
                        unit.variable_draw_attack_range = False

                    else:
                        unit.variable_draw_attack_range = True


            elif event.key == pygame.K_c:
                if player.variable_draw_attack_range == True:
                    player.variable_draw_attack_range = False

                else:
                    player.variable_draw_attack_range = True
            
            elif event.key == pygame.K_SPACE:
                if world_move == True:
                    world_move = False
                    skipping_a_move = False


                else:
                    world_move = True
                    skipping_a_move = True

            elif event.key == pygame.K_LALT:
                general_podswetka = not general_podswetka

                for unit in unit_list:
                    if general_podswetka:
                        if unit.team is None:
                            # нейтральные — слабая, тёплая
                            unit.podswetka = (True, (235,235,235) , (235,235,235))
                
                        elif unit.team == 0:
                            # союзники — мягкая синяя
                            unit.podswetka = (True, (70, 120, 255), (50, 30, 15))
                
                        else:
                            # враги — чуть плотнее красная
                            unit.podswetka = (True, (255, 60, 60), (180, 20, 20))
                    else:
                        unit.podswetka = (False, (0, 0, 0), (0, 0, 0))
                
                
                if general_podswetka:
                    # игрок — самый заметный
                    player.podswetka = (True, (80, 160, 255), (70, 40, 25))
                else:
                    player.podswetka = (False, (0, 0, 0), (0, 0, 0))
                    


        elif event.type == pygame.MOUSEWHEEL:
            if wind_inwentori:
                for winu in wind_inwentori:
                    if winu[3] and winu[3].collidepoint(mx, my):
                        winu[2].target_scroll_y += event.y * winu[2].scroll_speed

        if spis_pridm_spr and spiok_sprawki == None:

            spr_pred_x , spr_pred_y  = pygame.mouse.get_pos()
            for pridm_spr in spis_pridm_spr:
                if pridm_spr[0].collidepoint(spr_pred_x , spr_pred_y):
                    wuzow_sprawki = (pridm_spr[1] , spr_pred_x , spr_pred_y)
                    break
                else:
                    wuzow_sprawki = None
        else:
            wuzow_sprawki = None

        if predmetu_leg:
            for i in predmetu_leg:
                nx, ny = pygame.mouse.get_pos()
                nx, ny = controller.screen_to_world(nx, ny)

                if i.check_click((nx, ny )):
                    i.podswetka = True
                    
                else:
                    i.podswetka = False

        ui_interfes.ui_logik(event)


    if skipping_a_move == True:
        world_move = True

    elif player.path == [] or player.path == None: 
        world_move = False

    else:
        world_move = True


    controller.draw_world(player , dt , predmetu_leg , unit_list , None ,  world_move , fight.tile ,  unit_list_death)


    
    fight.apdete_xod()

    units_kletki_zanatu.clear()

    for unit in unit_list:
        unit.apdete(dt)

        if unit.death == True:
            unit_list.remove(unit)
            unit_list_death.append(unit)

        units_kletki_zanatu.append(unit.zanat_kletka)
    

    player.apdete(dt)

    if player.death == True:
        if player in unit_list:
            unit_list.remove(player)
            unit_list_death.append(player)
            print("вы умерли")

    units_kletki_zanatu.append(player.zanat_kletka)


    atributu_dla_class_spraw = [
        (rect, obj)
        for (rect, obj) in atributu_dla_class_spraw
        if not isinstance(obj, (Sunduk, Dweri))
    ]

    # 2️⃣ рисуем сундуки
    for (x, y), sunduk in sunduki.items():
        rect = sunduk.draw(controller.base_surface, x, y, sunduk)
        atributu_dla_class_spraw.append((rect, sunduk))

    # 3️⃣ рисуем двери
    for (x, y), door in doors.items():
        rect = door.draw_doors(controller.base_surface, x, y, door)
        atributu_dla_class_spraw.append((rect, door))
    #player.risowka_xit_boksa_tela(controller.base_surface) ##!

    x_pix, y_pix = pygame.mouse.get_pos()

    #player.risowka_xit_boksa_tela( controller.base_surface)

    x_pix , y_pix = controller.screen_to_world(x_pix, y_pix)
    x_cell, y_cell, tek, tek_anima = kw_pod_musko(controller.base_surface , x_pix, y_pix , dt , x_cell , y_cell , tek , tek_anima) ##!

    controller.draw_to_screen() ##############################!!!!!!!!

    if event.type == pygame.MOUSEBUTTONDOWN:
        klik_mouse = pygame.mouse.get_pos()
        if event.button == 1:
            mouse_klik = (klik_mouse , 1 )

        elif event.button == 2:
            mouse_klik = (klik_mouse , 2 )

        elif event.button == 3:
            mouse_klik = (klik_mouse , 3 )

        else:
            mouse_klik = None
    else:
        mouse_klik = None


    if event.type == pygame.KEYDOWN:
        key_buttun = event.key   # сюда запишется любая клавиша

    else:
        key_buttun = None


    #for unit in unit_list:
    #    #print("unit:", unit.xit_boks.topleft)
    #    pygame.draw.rect(screen, (255,0,0), unit.xit_boks, 1)#
    #
    #mx3 , my3 = pygame.mouse.get_pos()
    #pygame.draw.rect(screen, (255, 255,0), (2 , 2 , mx3 , my3), 1)#
    #for unit in unit_list:
    #    if unit.xit_boks.collidepoint(mx3 , my3):
    #        print(1)#
    #
    #mx3 , my3  = controller.screen_to_world(mx3 , my3 )
    #pygame.draw.rect(screen, (255,0,155), (2 , 2 , mx3 , my3), 1)#
    #for unit in unit_list:
    #    if unit.xit_boks.collidepoint(mx3 , my3):
    #        print(1)
    #
    #if player.aktiw_cards != None:
    #    haus_cards = player.aktiw_cards[0].active_ability
    #    for unit in unit_list:
    #        for rect_atak in haus_cards.spisok_cell_atak:
    #            pygame.draw.rect(screen, (255,80, 80), rect_atak, 1)#
    #            if unit.xit_boks.colliderect(rect_atak):
    #                print(1)



    ui_interfes.ui_display()
    ui_interfes.ui_update(poz = pygame.mouse.get_pos(), klilk = mouse_klik , key_buttun = key_buttun)

    ikona_wsa = None


    mnx , mmy = pygame.mouse.get_pos()


    wind_inwentori , ikona1  , spisok_iasheki1 , spis_pridm_spr1 , ikona_wsa1 = inwentar.ikona_print(screen , otrisowka_podswetki , wuborka , wuzow_sprawki , selected_items  )
    wind_inwentori = [(wind_inwentori ,  ikona1, inwentar , ikona_wsa1)]
    spis_pridm_spr = []
    wse_shasti_return_ikn_print = [(ikona1  , spisok_iasheki1 , spis_pridm_spr1 , ikona_wsa1 , inwentar)]


    for obektu in igrowoe_okrugenie_personag: # polna_ikona
        if hasattr(obektu, "iaseka_inwentor"):

            iaseka = obektu.iaseka_inwentor
            box = obektu.boks_inwentor

            if box.colliderect(player.xit_boks):
                if iaseka not in obshai.iasheki and obektu.is_open == True:
                    obshai.iasheki.append(iaseka)           
                    wuzow = True

                elif iaseka in obshai.iasheki and obektu.is_open == False:
                    obshai.iasheki.remove(iaseka)
                    obshai.wuborka = None
                    
                    if len(obshai.iasheki) <= 0:
                        wuzow = False
            else:
                if iaseka in obshai.iasheki:
                    obshai.iasheki.remove(iaseka)
                    obshai.wuborka = None
                    
                    if len(obshai.iasheki) <= 0:
                        wuzow = False
        

    if wuzow == True:
        wind_inwentori2 , ikona2  , spisok_iasheki2 , spis_pridm_spr2 , ikona_wsa2 = obshai.ikona_print(screen , otrisowka_podswetki , wuborka , wuzow_sprawki , selected_items )
        wind_inwentori.append((wind_inwentori2 , ikona2 , obshai , ikona_wsa2))

        if spis_pridm_spr2:
            spis_pridm_spr.extend(spis_pridm_spr2)

        wse_shasti_return_ikn_print.append((ikona2  , spisok_iasheki2 , spis_pridm_spr2 , ikona_wsa2 , obshai))

    if not wind_inwentori:
        spis_pridm_spr = []
        wuzow_sprawki = None

    if wind_inwentori:
        for winu in wind_inwentori:
            if winu[3] is not None and winu[3].collidepoint(mnx, mmy):
                for return_ikn_print in wse_shasti_return_ikn_print:
                    if winu[2] == return_ikn_print[4]:
                        parasmert = (True,winu[2],return_ikn_print[0],return_ikn_print[1],return_ikn_print[2],return_ikn_print[3])
                        break

                break   


    if parasmert and parasmert[0] == True:
        for winu in wind_inwentori : #------------
            if parasmert[1] == winu[2]:
                ikona , spisok_iasheki , spis_pridm_spr , ikona_wsa = parasmert[2] , parasmert[3] , parasmert[4] , parasmert[5]

                break


    if wind_inwentori: ######!!!           
        mnx2 , mny2 = pygame.mouse.get_pos()
        for winn in wind_inwentori:  
            if winn[3] != None :
                if winn[3].collidepoint(mnx2 , mny2):
                    wuborka_ydal = winn[2]
                    
                else:
                    wuborka_ydal = None                
            else:
                wuborka_ydal = None

        
    if sprawka_aktiw == True:
        spiok_sprawki , sprawka_aktiw2 = sprawka(mx2 , my2 , screen , igrowoe_okrugenie ,  font2 , controller , pokraska , klik ,  atributu_dla_class_spraw , player , wuborka_ydal , predmetu_leg  )

        if sprawka_aktiw2 == False:
            sprawka_aktiw = sprawka_aktiw2
            spiok_sprawki = None

    if mouse_hold and drag_group:
        mx, my = pygame.mouse.get_pos()
        for i, (predmet, _, _1) in enumerate(drag_group):

            pol_snurf2 = pygame.Surface((470 , 32), pygame.SRCALPHA) 
            pygame.draw.rect(pol_snurf2,(95, 95, 95, 215),(0, 0, 470, 32))
            screen.blit(pol_snurf2, (mx + i* 6 , my + i* 6))

            pygame.draw.rect(screen , (50, 50, 50) , (mx + i* 6 , my + i* 6 , 32 , 32) )
            pygame.draw.rect(screen , (50, 50, 50) , (mx + i* 6 , my + i* 6 ,  470, 32) , width= 1)

            screen.blit(predmet.izb, (mx + i* 6, my + i* 6)) 

            text_surf = font.render(predmet.name, True, (200, 200, 200))
            text_surf2 = font.render(predmet.tip, True, (170, 190, 220))
            screen.blit(text_surf, (mx + i* 6 + 35, my + i* 6 + 7 ) )
            screen.blit(text_surf2, (mx + i * 6 + 255, my + i* 6 + 7 ) )
            my += 25
            mx -= 6

    mx3 , my3 = pygame.mouse.get_pos()
    mx3 , my3  = controller.screen_to_world(mx3 , my3 )

    unit_list.append(player)

    for unit in unit_list:
        if unit.xit_boks.collidepoint(mx3, my3):
        
            if not any(u is unit for u, _ in spis_podswetok_oy_musu):
                spis_podswetok_oy_musu.append((unit, unit.podswetka))
    
                if unit.team is None:
                    unit.podswetka = (True, (235,235,235) , (235,235,235))
    
                elif unit.team == 0:
                    unit.podswetka = (True, (70, 120, 255), (50, 30, 15))
    
                else:
                    unit.podswetka = (True, (180, 20, 20), (180, 20, 20))

    unit_list.remove(player)

    for pd_unit in spis_podswetok_oy_musu:
        if not pd_unit[0].xit_boks.collidepoint(mx3 , my3):
            pd_unit[0].podswetka = pd_unit[1]
            spis_podswetok_oy_musu.remove(pd_unit)


    if sprawka_parameters.start == True:

        sprawka_parameters.draw_rect(screen )


    popali_ne_xodit = False
    popali_ne_xodit2 = False
    unit_ataked_not_sprawka = False

    draw_hud(font, int(clock.get_fps()) , screen)
    klik = None  
    pygame.display.flip()
    clock.tick()

#
#    for unit in unit_list:
#        #print("unit:", unit.xit_boks.topleft)
#        pygame.draw.rect(screen, (255,0,0), unit.xit_boks, 1)#
#    
#    mx3 , my3 = pygame.mouse.get_pos()
#    pygame.draw.rect(screen, (255, 255,0), (2 , 2 , mx3 , my3), 1)#
#    for unit in unit_list:
#        if unit.xit_boks.collidepoint(mx3 , my3):
#            print(1)#
#    
#    mx3 , my3  = controller.screen_to_world(mx3 , my3 )
#    pygame.draw.rect(screen, (255,0,0), (2 , 2 , mx3 , my3), 1)#
#    for unit in unit_list:
#        if unit.xit_boks.collidepoint(mx3 , my3):
#            print(1)
#    
#    if player.aktiw_cards != None:
#        haus_cards = player.aktiw_cards[0].active_ability
#        for unit in unit_list:
#            for rect_atak in haus_cards.spisok_cell_atak:
#                pygame.draw.rect(screen, (255,80, 80), rect_atak, 1)#
#                if unit.xit_boks.colliderect(rect_atak):
#                    print(1)