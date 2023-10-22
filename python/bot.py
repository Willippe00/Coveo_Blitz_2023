from game_message import *
from actions import *



class Bot:
    Hauteur = 0
    Largeur = 0
    MiHauteur = 0
    InfosAsteroide = 0
    PosCanon = 0
    VitesseMissile = 0

    def __init__(self):
        self.direction = 1
        print("Initializing your super mega duper bot")
        self.tick =0




    def get_next_move(self, game_message: GameMessage):
        if(self.tick == 0):
            self.firstTick(game_message)

        Target = game_message.meteors[0]
        TargetInterestValue = 0
        for meteor in game_message.meteors:
           print(meteor.id)
           meteorInterest =  self.InterestIndext(game_message, meteor.position.y, meteor.position.x, meteor.meteorType)
           if(meteorInterest>TargetInterestValue):
               Target = meteor
               TargetInterestValue = meteorInterest

        position = self.AimBot(Target)

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
        self.MiHauteur = self.Hauteur/2
        self.InfosAsteroide = game_message.constants.meteorInfos
        self.PosCanon = game_message.cannon.position
        self.VitesseMissile = game_message.constants.rockets.speed


    def InterestIndext(self,gamemessage ,HauteurActuel, LargeurActuel, TypeAsteroide):

        proportionLargeur =  (LargeurActuel/self.Largeur)


        distValMilieu = abs(HauteurActuel - self.MiHauteur) /3
        distValMilieu = 1


        facteur = 1
        if(LargeurActuel < 120):
            facteur = 0
        elif(TypeAsteroide == MeteorType.Large):
            facteur = 0.9
        elif(TypeAsteroide == MeteorType.Medium):
            facteur = 0.72
        elif (TypeAsteroide == MeteorType.Small ):
            facteur = 0.8

        else:
            facteur = 0.7

        return (distValMilieu + proportionLargeur) * facteur

    def AimBot(self,  AsteroideCible : Meteor):
        diffVitesse = self.soustractionVecteur(AsteroideCible.velocity , Vector(x=self.VitesseMissile/1.90, y=self.VitesseMissile/1.2))
        diffPosition = self.soustractionVecteur(self.PosCanon, AsteroideCible.position)
        TempsColision = self.produitScalaire(diffPosition, diffVitesse) / self.produitScalaire(diffVitesse, diffVitesse)

        posIntercept = self.additionVecteur(AsteroideCible.position, self.multiplicationVecteur(AsteroideCible.velocity, TempsColision))

        return posIntercept


    def produitScalaire(self,v1, v2):
        return v1.x * v2.x + v1.y * v2.y


    def soustractionVecteur(self, v1, v2):
        return Vector(v1.x - v2.x, v1.y - v2.y)


    def additionVecteur(self,v1, v2):
        return Vector(v1.x + v2.x, v1.y + v2.y)


    def multiplicationVecteur(self, v, scalaire):
        return Vector(v.x * scalaire, v.y * scalaire)
