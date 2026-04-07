class Brick:
    def __init__(self):
        #So we need a type, could use ENUM to define them and use integers as values for every type
        #We need to know it's size, placement on screen and color
        #For multihit we need to know how much dmg it has taken and track it to change color
        #Fixed at creating is it's size and placement on screen and type
        #Changes at runtime are dmg taken and color for multihit only
        #Drawing done in __init__ because it's a one time thing for every brick object then just update state
        pass

    def damage_tracking(self):
        #Use this to track damage taken and if it's multihit we change color to represent it, if not then we remove from screen
        pass

    def update_state(self):
        #Call this from damage_tracking, maybe should create three different functions to split the three types then call each one depending
        #on what type it is
        pass

    def ball_hit(self):
        #Use this for collision detection, or maybe it should be in ball?
        pass