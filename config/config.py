import pygame
import sys

world_move = False
skipping_a_move = False


mx, my = 0 , 0 
spiok_sprawki = None
dwigenie = True
running = True
pokraska = False
klik = None
wind_inwentori = None
peremenshen_musk_kw_sost = None
sprawka_aktiw = False
spisok_iasheki = None
otrisowka_podswetki = None
wuborka = None
spis_pridm_spr = None
wuzow_sprawki = None
ikona_wsa = None
atributu_dla_class_spraw = []
wuzow = False
klik_po_oknu = False
parasmert = False

selected_items = []      # [(predmet, id, iasheki)]
drag_group = []          # [(predmet, id, iasheki)]
drag_from_iasheki = None
mouse_hold = False
popali_ne_xodit = False
popali_ne_xodit2 = False
moved = False
unit_ataked_not_sprawka = False

igrowoe_okrugenie_personag = []
predmetu_leg = []

unit_list = []

units_kletki_zanatu = []
pretendeimue_kletki = []
unit_list_death = []

key_buttun = None

a = False


general_podswetka = False

spis_podswetok_oy_musu = []
spisok_ostatkow = set()

