class Tete:
    pass

class Corps:
    pass

class Membres:
    pass

class Habitat:
    def __init__(self, nom):
        self.nom = nom

class Animal:
    def __init__(self, habitat):
        self.tete = Tete()
        self.corps = Corps()
        self.membres = [Membres() for _ in range(4)]
        self.habitat = habitat

class Herbivore(Animal):
    pass

class Carnivore(Animal):
    pass
