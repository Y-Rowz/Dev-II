class FichierJoint:
    def __init__(self, nom, contenu):
        self.nom = nom
        self.contenu = contenu

class Email:
    def __init__(self, expediteur, destination, titre=None, texte=None):
        self.titre = titre
        self.texte = texte
        self.expediteur = expediteur
        self.destination = destination
        self.fichiers_joints = []

    def ajouter_fichier_joint(self, fichier):
        self.fichiers_joints.append(fichier)
