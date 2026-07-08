from Screen_controller_funk_draw.ScreenController import *
from clasu.vse_personagu import *
from clasu.dwer import *
from clasu.brona import *
from clasu.inwentori import *
from clasu.sunduk import *
from clasu.sumki import *
from clasu.ItemLying import *
from clasu.parameters import *

from funk.draw_hud import *
from funk.a_star_idti_k_celi import *
from funk.sprawka import *
from funk.kwadrat_pod_musko import *
from funk.bar_poloski_spr import *
from funk.otrisowka_leg_pred import *
from funk.dobowlenia_w_spisok import *



from data.game_items.armor.creation_armor import *
from data.game_items.weapons.weapons_sozdanie import *
from data.game_items.living_creatures.liwing_creatures import *

from config.config import *



def new_unit(x , y , plear , name  , telo_ful , izb_mr , trup , shadow , ekwip_shmot = None , ikn_mordu = ikn_mordu ):
    unit = Vse_personagu( x , y, telo_ful , izb_mr , sumka_igroka , name , trup , shadow , ikn_mordu = ikn_mordu  )

    unit.sklil_list.append(reartion)
    unit.sozdan_tel()

    igrowoe_okrugenie_personag.append(unit)
    unit_list.append(unit)
    atributu_dla_class_spraw.append((plear , unit ))
    
    if ekwip_shmot != None:
        for shmot in ekwip_shmot:
            unit.eqwip_plear(shmot)

    return unit