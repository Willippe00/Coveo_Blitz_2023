from game_message import *
from actions import *


class Bot:
    Hauteur = 0
    Largeur = 0
    MiLageur = 0
    def __init__(self):
        self.direction = 1
        print("Initializing your super mega duper bot")
        self.tick =0




    def get_next_move(self, game_message: GameMessage):
        if(self.tick == 0):
            self.firstTick(game_message)

        Target = game_message.meteors[0]
        TargetInterest = 0
        for meteor in game_message.meteors:
           print(meteor.id)
           meteorInterest =  self.InterestIndext(meteor.position.y, meteor.position.x)
           if(meteorInterest>TargetInterest):
               Target = meteor
               TargetInterest = meteorInterest

        position = Vector(x=int(Target.position.x), y=int(Target.position.y))

        return [LookAtAction(position),ShootAction(),]


        """
        Here is where the magic happens, for now the moves are not very good. I bet you can do better ;)
        """
        """

        if game_message.cannon.orientation >= 45:
            self.direction = -1
        elif game_message.cannon.orientation <= -45:
            self.direction = 1

        return [
            RotateAction(angle=15 * self.direction),
            ShootAction(),
        ]
        """
    def firstTick(self, game_message: GameMessage):
        self.Hauteur = game_message.constants.world.height
        self.Largeur = game_message.constants.world.width
        self.MiLageur = self.Largeur/2


    def InterestIndext(self, HauteurActuel, LargeurActuel):

        proportionHauteur = HauteurActuel/self.Hauteur
        valeurHauteur = proportionHauteur /1

        distValMilieu = abs(LargeurActuel - self.MiLageur)
        valeuLargeur = distValMilieu/1

        return valeuLargeur + valeurHauteur