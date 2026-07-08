import pygame
from clasu.brona import *

from data.game_items.armor.helmets.loading_helmet import *
from data.game_items.armor.chest_armor.loading_shest_armor import *
from data.game_items.armor.limb_armor.loading_limb_armor import *



wozdeistwiam_test = {
    "режущий":[21 , 2.2 ] ,  
    "дробящий": [9 , 0.8 ]  ,       
    "колющий":[12 , 2 ] ,  
}   


wozdeistwiam_impuls = { 
    "дробящий": [9 , 0.8 ]  ,       
}



verx_gambeson = Elem_Broni(
    name="гамбезон верх торса",
    ekwip_name="средний слой",
    ekwip_name_na_shto="верх торса",
    xit_boks=[pygame.Rect(90, 89, 45, 30)],
    izb=chest_armor_gambezon_verx_torsa,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1
    

)

niz_gambeson = Elem_Broni(
    name="гамбезон низ торса",
    ekwip_name="средний слой",
    ekwip_name_na_shto="низ торса",
    xit_boks=[pygame.Rect(93, 118, 40, 30)],
    izb=chest_armor_gambezon_niz_torsa,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1
)

plesho_praw_gambeson = Elem_Broni(
    name="гамбезон плечо правое",
    ekwip_name="средний слой",
    ekwip_name_na_shto="плечо правое",
    xit_boks=[pygame.Rect(79, 89, 10, 35)],
    izb=chest_armor_gambezon_izb_plesho_praw,
    izb_two_hend=chest_armor_gambezon_plesho_praw_type_b,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1

)

plesho_lew_gambeson = Elem_Broni(
    name="гамбезон плечо левое",
    ekwip_name="средний слой",
    ekwip_name_na_shto="плечо левое",
    xit_boks=[pygame.Rect(79 + 57, 89, 10, 35)],
    izb=chest_armor_gambezon_izb_plesho_lew,
    izb_two_hend=chest_armor_gambezon_izb_plesho_lew_type_b,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1

)

plesho_p_praw_gambeson = Elem_Broni(
    name="гамбезон предплечье правое",
    ekwip_name="средний слой",
    ekwip_name_na_shto="предплечье правое",
    xit_boks=[pygame.Rect(79, 122, 10, 27)],
    izb=chest_armor_gambezon_pred_p_praw,
    izb_two_hend=chest_armor_gambezon_pred_p_praw_type_b,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1

)

plesho_p_lew_gambeson = Elem_Broni(
    name="гамбезон предплечье левое",
    ekwip_name="средний слой",
    ekwip_name_na_shto="предплечье левое",
    xit_boks=[pygame.Rect(79 + 57, 122, 10, 27)],
    izb=chest_armor_gambezon_pred_p_lew,
    izb_two_hend=chest_armor_gambezon_pred_p_lew_type_b,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1

)


bedro_praw_gambeson = Elem_Broni(
    name="гамбезон бедро правое",
    ekwip_name="средний слой",
    ekwip_name_na_shto="бедро правое",
    xit_boks=[pygame.Rect(92, 146, 20, 45)],
    izb=chest_armor_gambezon_bedro_praw,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1

)

bedro_lew_gambeson = Elem_Broni(
    name="гамбезон бедро левое",
    ekwip_name="средний слой",
    ekwip_name_na_shto="бедро левое",
    xit_boks=[pygame.Rect(92 + 22, 146, 20, 45)],
    izb=chest_armor_gambezon_bedro_lew,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls ,
    softening_prn = 1,
    contact_profile = 1

)




gambeson = Brona(
    name="гамбезон",
    tip="ОДЕЖДА",
    izb=chest_armor_gambezon_big,
    spisok_shastei_broni=[
        verx_gambeson,
        niz_gambeson,
        plesho_praw_gambeson,
        plesho_lew_gambeson,
        plesho_p_praw_gambeson,
        plesho_p_lew_gambeson,
        bedro_praw_gambeson,
        bedro_lew_gambeson,
    ]
)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------


wozdeistwiam_test2 = {
    "режущий":[21 , 2.2 ] ,  
    "дробящий": [9 , 0.8 ]  ,       
    "колющий":[12 , 2 ] ,  
}   


wozdeistwiam_impuls2 = { 
    "дробящий": [9 , 0.8 ]  ,       
}



verx_latna_kirasa = Elem_Broni(
    name="латная кираса верх торса",
    ekwip_name="броне жылет",
    ekwip_name_na_shto="верх торса",
    xit_boks=[pygame.Rect(90, 89, 45, 30)],
    izb=chest_armor_lat_kirasa_verx_torsa,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test2  ,  
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls2 ,
    softening_prn = 1,
    contact_profile = 1
    

)

niz_latna_kirasa = Elem_Broni(
    name="латная кираса низ торса",
    ekwip_name="броне жылет",
    ekwip_name_na_shto="низ торса",
    xit_boks=[pygame.Rect(93, 118, 40, 30)],
    izb=chest_armor_lat_kirasa_niz_torsa,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test2  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls2 ,
    softening_prn = 1,
    contact_profile = 1
)

plesho_praw_latna_kirasa = Elem_Broni(
    name="латная кираса плечо правое",
    ekwip_name="наплечник",
    ekwip_name_na_shto="плечо правое",
    xit_boks=[pygame.Rect(79, 89, 10, 35)],
    izb=chest_armor_lat_kirasa_plesho_praw,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test2  ,
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls2 ,
    softening_prn = 1,
    contact_profile = 1

)

plesho_lew_latna_kirasa = Elem_Broni(
    name="латная кираса плечо левое",
    ekwip_name="наплечник",
    ekwip_name_na_shto="плечо левое",
    xit_boks=[pygame.Rect(79 + 57, 89, 10, 35)],
    izb=chest_armor_lat_kirasa_plesho_lew,
    izb_two_hend=None,
    tolshina= 6,
    plotnost=50 ,
    kof_hp_material_strength= 1.0 ,
    increasing_contact_pr = 1.1,
    increasing_contact_kn = 1.1,
    impulse_damping = 0.3,
    twerdost = 5   ,
    spr_wozdeistwiam_test = wozdeistwiam_test2  ,  
    spr_wozdeistwiam_impuls = wozdeistwiam_impuls2 ,
    softening_prn = 1,
    contact_profile = 1

)



latna_kirasa = Brona(
    name="латная кираса с наплечами",
    tip="ОДЕЖДА",
    izb=chest_armor_lat_kirasa_big,
    spisok_shastei_broni=[
        verx_latna_kirasa,
        niz_latna_kirasa,
        plesho_praw_latna_kirasa,
        plesho_lew_latna_kirasa,

    ]
)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------



kolshuga = Brona(
    name="длинная кольчуга",
    tip="ОДЕЖДА",
    izb=chest_armor_kol_shuga_big,
    spisok_shastei_broni=[

    ]
)

