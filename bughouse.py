import mouvement
import plateau

class bughouse:

    def __init__(self):
        self.plateau1 = plateau.remplissage()
        self.plateau2 = plateau.remplissage()
        self.listestockagePlateau1 = []
        self.listestockagePlateau2 = []
        self.couleur1 = 0
        self.couleur2 = 1

    def remplirListe(self, xInitial, yInitial, xFutur, yFutur, numPlateau) :
        liste = self.quelleListe(numPlateau)
        tab = self.quellePlateau(numPlateau)
        valeurMangee = mouvement.recupererValeurSupp(tab, xInitial, yInitial, xFutur, yFutur)
        if (valeurMangee != 0) :
            liste.append(valeurMangee)

    def quelleListe(self, numPlateau) :
        p=[]
        if (numPlateau==1) :
            p=self.listestockagePlateau1
        if (numPlateau==2) :
            p=self.listestockagePlateau2
        return p

    def quellePlateau(self, numPlateau) :
        p=[]
        if (numPlateau==1) :
            p=self.plateau1
        if (numPlateau==2) :
            p=self.plateau2
        return p

    def caseLibrePlateau(self, numPlateau, i, j) :
        p=self.quellePlateau(numPlateau)
        return p[i][j]==0
    
    def deposerPice(self, numPlateau,  x,y,val) :
        p=self.quellePlateau(numPlateau)
        mouvement.deposerPiece(p, val,x,y)

    def getPlateau(self, numPlateau) :
        p=self.quellePlateau(numPlateau)
        return p
    
    def getListe(self, numPlateau) :
        p=self.quelleListe(numPlateau)
        return p
    
    def incrementerCouleur(self, numPlateau) :
        if (numPlateau==1) :
            self.couleur1+=1
        else :
            self.couleur2+=1

    def getCouleur(self, numPlateau) :
        if numPlateau==1 :
            self.couleur1=self.couleur1%2
            return self.couleur1
        else :
            self.couleur2= self.couleur2%2
            return self.couleur2

    def valeurPresente(self, numPlateau, val) :
        liste =self.quelleListe(numPlateau)
        taille =len(liste) 
        for i in range (taille) :
            if (liste[i]==val) :
                return True
        return False

    def validerAjoutPiece(self, reserveNum, numPlateau, valeur, i, j) :
        # reserveNum : la réserve d'où vient la pièce (listestockagePlateauX)
        # numPlateau : le plateau sur lequel on veut la poser
        return self.valeurPresente(reserveNum, valeur) and self.caseLibrePlateau(numPlateau, i, j) and self.ajoutPionDansLesLimites(i, j)

    def retirerDeReserve(self, reserveNum, index) :
        liste = self.quelleListe(reserveNum)
        if 0 <= index < len(liste) :
            return liste.pop(index)
        return None

    def ajoutPionDansLesLimites(self, i, j) :
        return (0<=j<8 and 0<i<7)

#on va maintenant récuperer l'ensemble des coups possibles

    def listeCoupClassique(self, numPlateau) :
        tab=self.quellePlateau(numPlateau)
        return mouvement.mouvementEnsembleEchequierPourUneCouleur(tab,self.getCouleur(numPlateau))

    def listePose(self, numPlateau) :
        listeFinale= []
        tab=self.quellePlateau(numPlateau)
        couleur=self.getCouleur(numPlateau)
        liste=self.quelleListe(numPlateau)
        for i1 in liste :
            for (i, j) in mouvement.listeCaseLibre(tab) :
                if (self.validerAjoutPiece(liste, numPlateau, i1, i, j)) :
                    depart= (-1, i)
                    arrivee= (i, j)
                    listeFinale.append(depart, arrivee)
        return listeFinale
            
    def getAllMouvement(self, numPlateau) :
        liste=self.listeCoupClassique(numPlateau)
        liste.append(listePose(numPlateau))
        return liste