

class Attribute():
    def __init__(self, name , value , description , influence_part , influence_main_system , impact_factories):
        self.name = name
        self.value = value
        self.modifier = 1.0
        self.description = description


        self.influence_part = influence_part
        self.influence_main_system = influence_main_system 


        self.influence_part_finish = None
        self.influence_main_system_finish = None

        self.update_influence()

        self.impact_factories = impact_factories

    
    def update_influence(self):
        self.influence_part_finish = self.influence_part

        for key, value in self.influence_part.items():
            if isinstance(value, dict):
                for key2, value2 in value.items():
                    self.influence_part_finish[key][key2] = [value2[0] * self.value * self.modifier , value2[1]]
            else:
                self.influence_part_finish[key] = value * self.value * self.modifier


        self.influence_main_system_finish = self.influence_main_system


        for key, value in self.influence_main_system.items():
            if isinstance(value, dict):
                for key2, value2 in value.items():
                    self.influence_main_system_finish[key][key2] = [value2[0] * self.value * self.modifier , value2[1]]
            else:
                self.influence_main_system_finish[key] = value * self.value * self.modifier



stoikost = Attribute(name = "стойкость" , value = 10 , description = "повышает физическую стойкость и переносимые нагрузки" , 
                    influence_part = {
                    "spr_wozdeistwiam_test": {
                        "режущий":[0.1 , 0 ] ,  
                        "дробящий": [0.15 , 0 ]  ,       
                        "колющий":[0.1 , 0 ] ,  
                    },

                    "spr_wozdeistwiam_impuls": { 
                        "дробящий": [0.15 , 0 ]  ,       
                    },

                    "impulse_damping": 0.05 ,
                    },

                     
                    influence_main_system = {
                        "carry_weight_max":0.1 ,
                    },
                    impact_factories = "tkani")


sila = Attribute(name = "сила" , value = 10 , description = "повышает физическую силу и переносимые нагрузки" , influence_part = {}, influence_main_system = {"carry_weight_max":0.5 },
                impact_factories = "tkani")

kordinatio = Attribute(name = "моторика" , value = 10 , description = "повышает точность движений" , influence_part = {}, influence_main_system = {},
                impact_factories = "tkani")

spead = Attribute(name = "скорость" , value = 10 , description = "повышает скорость движений" , influence_part = {}, influence_main_system = {},
                impact_factories = "tkani")






#print(strength.influence_part_finish)
#print(strength.influence_main_system_finish)