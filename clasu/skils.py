
class Skill():
    def __init__(self , name , opisanie , value , interest_level , influence_main_system , influence_parameters  ):
        self.name = name
        self.opisanie = opisanie
        self.value = value

        self.interest_level = interest_level

        self.influence_main_system = influence_main_system 

        self.influence_parameters = influence_parameters 









reartion = Skill(name = "реакция" , opisanie = "повышает скорость реакции и точность действий" , value = 25 , interest_level = 1.0 ,
                    influence_main_system = ["reaction"],
                    influence_parameters = {"All":{"сила":0.01 , "скорость":0.2 , "моторика":0.3}}, )



sword_obr = Skill(name = "обращение с мечом" , opisanie = "повышает скорость реакции и точность действий" , value = 25, interest_level = 1.0 ,
                    influence_main_system = [],
                    influence_parameters = {"ЛЕГК":{"сила":0.2 , "скорость":0.8 , "моторика":0.3},
                                            "владение шашками":{"сила":1.7 , "скорость":1.8 , "моторика":1.3}} , 
                    )



sword_masa = Skill(name = "обращение с тяжелым оружием" , opisanie = "повышает скорость реакции и точность действий" , value = 25 , interest_level = 1.0 ,
                    influence_main_system = [],
                    influence_parameters = {"ТЯЖ":{"сила":1.7 , "скорость":0.8 , "моторика":0.3}} , )


