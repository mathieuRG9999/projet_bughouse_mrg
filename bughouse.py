import mouvement
import plateau

class bughouse:

    listestockagePlateau1 = []
    listestockagePlateau2 = []
    couleur1=0
    couleur2=1

    def __init__(self):
        self.plateau1 = plateau.remplissage()
        self.plateau2= plateau.remplissageInverse()


    def remplirListe(self, xInitial, yInitial, xFutur, yFutur, numPlateau) :
        liste=self.quelleListe(numPlateau)
        plateau=self.quellePlateau(numPlateau)
        liste.append(mouvement.recupererValeurSupp(plateau, xInitial, yInitial, xFutur, yFutur))

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
        return not mouvement.caseEstOccupe(p, i, j)
    
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

    def validerAjoutPiece(self, numPlateau, valeur, i , j) :
        return self.valeurPresente(numPlateau, valeur) and self.caseLibrePlateau(numPlateau, i, j) and self.ajoutPionDansLesLimites(i, j)
    
    def ajoutPionDansLesLimites(self, i, j) :
        return (0<=j<8 and 0<i<7) 

