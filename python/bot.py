from game_message import *
from actions import *



class Bot:
    Hauteur = 0
    Largeur = 0
    MiHauteur = 0
    InfosAsteroide = 0
    PosCanon = 0
    VitesseMissile = 0
    shotLastTick = []
    shotLastTick2 = []
    shotLastTick3 = []
    shotLastTick4 = []
    shotLastTick5 = []



    def __init__(self):
        self.direction = 1
        print("Initializing your super mega duper bot")
        self.tick =0




    def get_next_move(self, game_message: GameMessage):
        if(self.tick == 0):
            self.firstTick(game_message)


        Target = game_message.meteors[0]
        Target2 = game_message.meteors[0]




        TargetInterestValue = 0

        for meteor in game_message.meteors:
           meteorInterest =  self.InterestIndext(game_message, meteor.position.y, meteor.position.x, meteor.meteorType)
           if (meteorInterest > TargetInterestValue and
                   meteor.id not in self.shotLastTick and
                   meteor.id not in self.shotLastTick2 and
                   meteor.id not in self.shotLastTick3 and
                   meteor.id not in self.shotLastTick4 and
                   meteor.id not in self.shotLastTick5):

               Target2 = Target
               Target = meteor
               TargetInterestValue = meteorInterest

        self.shotLastTick5.clear()
        self.shotLastTick5 = self.shotLastTick4.copy()
        self.shotLastTick4.clear()
        self.shotLastTick4 = self.shotLastTick3.copy()
        self.shotLastTick3.clear()
        self.shotLastTick3 = self.shotLastTick2.copy()
        self.shotLastTick2.clear()
        self.shotLastTick2 = self.shotLastTick.copy()
        self.shotLastTick.clear()


        positionTarget = self.AimBot(Target)
        positionTarget2 = self.AimBot(Target2)



        print(game_message.score)
        self.shotLastTick.append(Target.id)
        self.shotLastTick.append(Target2.id)



        return [LookAtAction(positionTarget),ShootAction(),LookAtAction(positionTarget2),ShootAction(),]


    def firstTick(self, game_message: GameMessage):
        self.Hauteur = game_message.constants.world.height
        self.Largeur = game_message.constants.world.width
        self.MiHauteur = self.Hauteur/2
        self.InfosAsteroide = game_message.constants.meteorInfos
        self.PosCanon = game_message.cannon.position
        self.VitesseMissile = game_message.constants.rockets.speed


    def InterestIndext(self,gamemessage ,HauteurActuel, LargeurActuel, TypeAsteroide):

        proportionLargeur =  (LargeurActuel/self.Largeur) *2.5


        distValMilieu =  3*(1/ abs(HauteurActuel - self.MiHauteur))
        #distValMilieu = 1


        facteur = 1
        if(LargeurActuel < gamemessage.cannon.position.x + 100):
            facteur = 0
        elif (TypeAsteroide == MeteorType.Small and LargeurActuel < self.Largeur / 2 and HauteurActuel> self.Hauteur/6 and HauteurActuel< 5*self.Hauteur/6):
            facteur = 120
        elif (TypeAsteroide == MeteorType.Small and LargeurActuel < self.Largeur / 2 and HauteurActuel> self.Hauteur/6 and HauteurActuel< 5*self.Hauteur/6):
            facteur = 70

        elif (TypeAsteroide == MeteorType.Medium  ):
            facteur = 25
        elif (TypeAsteroide == MeteorType.Large ):
            facteur = 9




        return (distValMilieu + proportionLargeur) * facteur

    def AimBot(self,  AsteroideCible : Meteor):
        diffVitesse = self.soustractionVecteur(AsteroideCible.velocity , self.volicityApproxyMissil(AsteroideCible))
        diffPosition = self.soustractionVecteur(self.PosCanon, AsteroideCible.position)
        TempsColision = self.produitScalaire(diffPosition, diffVitesse) / self.produitScalaire(diffVitesse, diffVitesse)

        posIntercept = self.additionVecteur(AsteroideCible.position, self.multiplicationVecteur(AsteroideCible.velocity, TempsColision))

        return posIntercept

    def volicityApproxyMissil(self, AsteroideCible : Meteor):
        positionEstimee = AsteroideCible.position

        for _ in range(60):  # 10 itérations pour convergence (ajuster si nécessaire)
            vecteur_vitesse_missile = self.volicityApproxyMissil_vers_position(positionEstimee)
            delta_temps = self.tempsImpact(positionEstimee, self.PosCanon, self.norme(vecteur_vitesse_missile))
            positionEstimee = self.estimerPosition(AsteroideCible.position, AsteroideCible.velocity, delta_temps)
        return self.volicityApproxyMissil_vers_position(positionEstimee)

    def volicityApproxyMissil_vers_position(self, position):
        """Version originale de la fonction pour obtenir la vélocité du missile vers une position donnée."""
        VecteurDirection = self.soustractionVecteur(position, self.PosCanon)
        longueur = self.norme(VecteurDirection)
        VecteurUnitaire = Vector(VecteurDirection.x / longueur, VecteurDirection.y / longueur)
        return Vector(self.VitesseMissile * VecteurUnitaire.x, self.VitesseMissile * VecteurUnitaire.y)

    def estimerPosition(self,positionAsteroide, vitesseAsteroide, delta_temps):
        """Estime la nouvelle position de l'astéroïde après un certain temps."""
        return Vector(positionAsteroide.x + vitesseAsteroide.x * delta_temps,
                      positionAsteroide.y + vitesseAsteroide.y * delta_temps)

    def tempsImpact(self,position_cible, position_lanceur, vitesse_missile):
        """Estime le temps nécessaire pour que le missile atteigne la cible."""
        vecteur_direction = self.soustractionVecteur(position_cible, position_lanceur)
        longueur = self.norme(vecteur_direction)
        return longueur / vitesse_missile

    def norme(self,v):
        return (v.x**2 + v.y**2)**0.5
    def produitScalaire(self,v1, v2):
        return v1.x * v2.x + v1.y * v2.y


    def soustractionVecteur(self, v1, v2):
        return Vector(v1.x - v2.x, v1.y - v2.y)


    def additionVecteur(self,v1, v2):
        return Vector(v1.x + v2.x, v1.y + v2.y)


    def multiplicationVecteur(self, v, scalaire):
        return Vector(v.x * scalaire, v.y * scalaire)
