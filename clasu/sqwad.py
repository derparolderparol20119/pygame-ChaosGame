import pygame
from config.config import *
import random 
import math


class Squad():
    def __init__(self , name , prikaz_liders , standard , squad  ):
        self.name = name
        self.prikaz_liders  = prikaz_liders  
        self.standard = standard 
        self.squad = squad


class Squad_soldier():
    def __init__(self , unit , priority , role , where_to_go , where_to_hit):
        self.unit = unit
        self.priority = priority
        self.role = role
        self.where_to_go = where_to_go
        self.where_to_hit = where_to_hit
    
    def gou_tu(self):
        self.unit.idti_k(self.where_to_go[0] , self.where_to_go[1] , units_kletki_zanatu , pretendeimue_kletki  , True)
        

 
