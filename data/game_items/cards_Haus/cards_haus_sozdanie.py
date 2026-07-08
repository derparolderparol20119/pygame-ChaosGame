from clasu.player_cards import *

import pygame



atrim_izb = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\atrim_izb.png').convert_alpha() 
atrim_ramka = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\atrim_ramka.png').convert_alpha() 


atrim_anim_1 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\animed/1.png').convert_alpha() 
atrim_anim_2 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\animed/2.png').convert_alpha() 
atrim_anim_3 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\animed/3.png').convert_alpha() 
atrim_anim_4 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\animed/4.png').convert_alpha() 
atrim_anim_5 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\animed/5.png').convert_alpha() 
atrim_anim_6 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\animed/6.png').convert_alpha() 


atrim_ostatok = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\cards_Haus\atrim\ostatok.png').convert_alpha() 


atrim_choice = Choice_target_1(
    range=15,
    cell_blow=[
        (0, 0), (1, 0), (-1, 0),
        (0, 1), (0, -1),
        (1, 1), (-1, 1),
        (1, -1), (-1, -1)
    ]
)

atrim_damage = Method_damage_and_draw(
    animation=[
        atrim_anim_1,
        atrim_anim_2,
        atrim_anim_3,
        atrim_anim_4,
        atrim_anim_5,
        atrim_anim_6
    ],
    time_animation=23,
    range=15 ,
    smesh_lishnoe_x= 0 ,
    smesh_lishnoe_y= 4  ,
    ostatki_na_zemle=atrim_ostatok,
    frame_ostatki_na_zemle=-4,
    duration_atak=40,
    range_px=5,
    hold=20
)


#atrim_damage.duration_atak = 40
#atrim_damage.range_px = 5
#atrim_damage.hold = 10


atrim = Cards(
    name="атриум",
    type="боевая карта",
    rang=12,
    determining_rang="золото",
    int_activeted_cards=500,
    coldung=1000,
    img=atrim_izb,
    ramka=atrim_ramka,
    choice_target=atrim_choice,
    method_damage_and_draw=atrim_damage

)