class DossierPersonnel:
    def __init__(self, etat_civil, coordonnees):
        self.etat_civil = etat_civil
        self.coordonnees = coordonnees

class Professeur:
    def __init__(self, nom, dossier):
        self.nom = nom
        self.dossier_personnel = dossier

class Eleve:
    def __init__(self, nom, dossier):
        self.nom = nom
        self.dossier_personnel = dossier

class Classe:
    def __init__(self, professeur):
        self.professeur = professeur
        self.eleves = []

    def ajouter_eleve(self, eleve):
        if len(self.eleves) < 30:
            self.eleves.append(eleve)
        else:
            raise ValueError("Nombre maximum d'élèves atteint")
