
import move

def plantPumpkin():
    if get_ground_type() == Grounds.Grassland:
        till()
        move.DoEnding = False
        plant(Entities.Pumpkin)
    if get_entity_type() == Entities.Dead_Pumpkin:
        move.DoEnding = False
        plant(Entities.Pumpkin)
    if get_entity_type() == None:
        move.DoEnding = False
        plant(Entities.Pumpkin)

def plantCarrot():
    move.DoEnding = False
    if get_ground_type() == Grounds.Grassland:
        till()
        plant(Entities.Carrot)
    if can_harvest():
        harvest()
        plant(Entities.Carrot)

def plantTree():
    if (get_pos_x()+get_pos_y())%4 == 0:
        if get_ground_type() == Grounds.Grassland:
            till()
            plant(Entities.Tree)
        if can_harvest():
            harvest()
            plant(Entities.Tree)
    else:
        if can_harvest():
            harvest()

def plantGrass():
    if can_harvest():
        harvest()

def pumpkinEnding():
    use_item(Items.Weird_Substance)
    harvest()