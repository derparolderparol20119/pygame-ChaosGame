import pygame
from copy import deepcopy

LIMB_TEMPLATES = {
    "basic_limb": {
        "name": "no name",
        "tip": "tkani",
        "glubina": 0,
        "bodi_rekt": pygame.Rect(0, 0, 0, 0),
        "x": 10,
        "y": 10,
        "fabric_depth": 0,
        "parent": None,
        "draw_lear_telo": 0,
        "slots_ekwip": [],
        "izb": None,
        "izb_tip_b": None,
        "influence": None,

        "tolshina": 5,
        "plotnost": 10,
        "kof_hp_material_strength": 1.0,
        "increasing_contact_pr": 1.0,
        "increasing_contact_kn": 1.0,
        "impulse_damping": 0.3,
        "twerdost": 5,
        "spr_wozdeistwiam_test": {
            "режущий":[5 , 2.2 ] ,  
            "дробящий": [6 , 2 ]  ,       
            "колющий":[3 , 1.5 ] ,  
        },

        "spr_wozdeistwiam_impuls": { 
            "дробящий": [6 , 0.8 ]  ,       
        },

        "softening_prn": 1,
        "contact_profile": 1

    },
    "basic_bone": {
        "name": "no name",
        "tip": "bone",
        "glubina": 0,
        "bodi_rekt": pygame.Rect(0, 0, 0, 0),
        "x": 10,
        "y": 10,
        "fabric_depth": 0,
        "parent": None,
        "draw_lear_telo": 0,
        "slots_ekwip": [],
        "izb": None,
        "izb_tip_b": None,
        "influence": None,

        "tolshina": 5,
        "plotnost": 10,
        "kof_hp_material_strength": 3.0,
        "increasing_contact_pr": 1.0,
        "increasing_contact_kn": 1.0,
        "impulse_damping": 0.3,
        "twerdost": 5,
        "spr_wozdeistwiam_test": {
            "режущий":[8 , 2.2 ] ,  
            "дробящий": [7 , 2 ]  ,       
            "колющий":[5 , 1.5 ] ,  
        },

        "spr_wozdeistwiam_impuls": { 
            "дробящий": [7 , 0.8 ]  ,       
        },

        "softening_prn": 1,
        "contact_profile": 1

    },




}



