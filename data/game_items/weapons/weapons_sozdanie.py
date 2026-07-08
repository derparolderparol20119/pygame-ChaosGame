import pygame
from clasu.melee_weapons import *


ikn_sword_shel1 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_sword_shel1.png').convert_alpha() 
ikn_sword_shel1_poworot = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_sword_shel1_powort.png').convert_alpha() 
ikn_sword_shel1_big = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_sword_shel1_big.png').convert_alpha() 


ikn_sword_shel2 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_sword_shel2.png').convert_alpha() 
ikn_sword_shel2_big = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_sword_shel2_big.png').convert_alpha() 


ikn_pika_shel1 = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_pika_shel1.png').convert_alpha() 
ikn_pika_shel1_big = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_pika_shel1_big.png').convert_alpha() 


ikn_stalca = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_stalca.png').convert_alpha() 
ikn_stalca_big = pygame.image.load(r'e:\py.game_proektu\igra xaosa\data\game_items\weapons\ikn_stalca_big.png').convert_alpha() 





asa = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть правая")
sword = Melee_weapons(name = "шашка", tip = "ОДНОРУЧНОЕ ОРУЖЫЕ",  hp= 35, hp_max = 35 , length = 0.6 , hit_point = 0.4 ,  contact_area = 3 ,  izb = ikn_sword_shel1_big, izb_na_sheloweke = ikn_sword_shel1, 
spisok_shastei_wepon = [asa], masa = 4 , twerdost= 30 , two_handed = False , influence_attributes = {"сила":0.2 , "скорость":0.5} ,influence_skills = 
{"ЛКГК":1.5 , "владение шашками":1.3 }, draw_layer = 45 )


asa2 = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть левая")
sword2 = Melee_weapons(name = "шашка", tip = "ОДНОРУЧНОЕ ОРУЖЫЕ",  hp= 35, hp_max = 35,  length = 0.6 , hit_point = 0.4 ,  contact_area = 3  , izb = ikn_sword_shel1_big, izb_na_sheloweke = ikn_sword_shel1_poworot, 
spisok_shastei_wepon = [asa2], masa = 4 , twerdost= 30 , two_handed = False , influence_attributes = {"сила":0.2 , "скорость":0.5}  ,influence_skills = 
{"ЛКГК":1.5 , "владение шашками":1.3 }, draw_layer = 45 )


asa3 = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть правая")
asa4 = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть левая")


sword3 = Melee_weapons(name = "Цальдойский Шварцтек", tip = "ДВУРУЧНОЕ ОРУЖЫЕ",  hp= 35, hp_max = 35, length = 1.1 , hit_point = 0.9 ,  contact_area = 8 ,  izb = ikn_stalca_big, izb_na_sheloweke = ikn_stalca, 
spisok_shastei_wepon = [asa3 , asa4], masa = 14 , twerdost= 30 , two_handed = True , influence_attributes = {"сила":0.9 , "скорость":0.1} ,
influence_skills = {"ТЯЖ":1.5 , "владение топорами":1.1 }, draw_layer = 45  )



asa5 = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть правая")
asa6 = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть левая")

pika1 = Melee_weapons(name = "глефа", tip = "ДВУРУЧНОЕ ОРУЖЫЕ",  hp= 35, hp_max = 35, length = 1.2 , hit_point = 0.5 ,  contact_area = 1 ,  izb = ikn_pika_shel1_big , izb_na_sheloweke = ikn_pika_shel1, 
spisok_shastei_wepon = [asa5 , asa6], masa = 2 , twerdost= 30 , two_handed = True , influence_attributes = {"сила":0.4 , "скорость":0.4} ,
influence_skills = {"ТЯЖ":1.5, "владение глефами":1.1 }, draw_layer = 45  )



asa7 = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть правая")
asa8 = Elem_wepon(name = "надететь",  ekwip_name ="оружые", ekwip_name_na_shto ="кисть левая")

sword4 = Melee_weapons(name = "Кислотный Нагольхольм", tip = "ДВУРУЧНОЕ ОРУЖЫЕ",  hp= 35, hp_max = 35, length = 0.7 , hit_point = 0.5 ,  contact_area = 3 ,  izb = ikn_sword_shel2_big , izb_na_sheloweke = ikn_sword_shel2 , 
spisok_shastei_wepon = [asa7 , asa8], masa = 4 , twerdost= 30 , two_handed = True , influence_attributes = {"сила":0.8 , "скорость":0.1} ,
influence_skills = {"ТЯЖ":1.5 ,"владение клинками":1.3 }, draw_layer = 45  )

