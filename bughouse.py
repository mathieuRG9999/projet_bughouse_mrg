import mouvement
import plateau
import random 

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

    def quelleListeAUtiliser(self, numPlateau) :
        p=[]
        if (numPlateau==1) :
            p=self.listestockagePlateau2
        if (numPlateau==2) :
            p=self.listestockagePlateau1
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
    
    def ajoutListe(self, numPlateau, valeur) :
        self.quelleListeAUtiliser(numPlateau).append(valeur)
    
    def removeListe(self, numPlateau, valeur) :
        self.quelleListeAUtiliser(numPlateau).remove(valeur)
    
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
        reserveNum = 2 if numPlateau == 1 else 1  # MODIFICATION : Le plateau 1 pioche dans la réserve 2 (et inversement)
        listeFinale= []
        tab=self.quellePlateau(numPlateau)
        couleur=self.getCouleur(numPlateau)
        liste=self.quelleListe(reserveNum)
        for i1 in set(liste) : #pour ne pas regarder plusieurs fois la même pièce
            for (i, j) in mouvement.listeCaseLibre(tab) :
                if (self.validerAjoutPiece(reserveNum, numPlateau, i1, i, j)) :
                    depart= (-1, i1) #on met -1 pour rester sur des nombres et se diff des autres 
                    arrivee= (i, j)
                    listeFinale.append((depart, arrivee))
        return listeFinale
            
    def getAllMouvement(self, numPlateau) :
        liste=self.listeCoupClassique(numPlateau)
        liste.extend(self.listePose(numPlateau)) # MODIFICATION : Ajout de 'self.' et utilisation de '.extend()' au lieu de '.append()'
        return liste

    #################################################################################################################################################################################################################################################################################

    def joueAleatoire(self, numPlateau) :
        listeCoups = self.getAllMouvement(numPlateau)
        tab=self.quellePlateau(numPlateau)
        coup_aleatoire =random.choice(listeCoups)
        print("le coup aléatoire est \n")
        mouvement.mouvement_to_string(tab, coup_aleatoire )
        print("pour le plateau ", numPlateau)
        return coup_aleatoire

    def joueMieuxQuAleatoire(self, numPlateau) :
        listeCoups = self.getAllMouvement(numPlateau)
        tab=self.quellePlateau(numPlateau)
        listeCoups.sort(
            key=lambda coup: mouvement.valeurMouvement(tab, coup[0][0], coup[0][1], coup[1][0], coup[1][1]), 
            reverse=True
        )
        return listeCoups

        
    def appliquerCoup(self, numPlateau, coup) :
        arrivee, final = coup
        i1, j1=arrivee
        i2, j2= final
        if (i1==-1) : #cas ou on doit récuperer une valeur
            valeur=j1
            self.removeListe(numPlateau, valeur)
            mouvement.poserSurPlateau(self.quellePlateau(numPlateau), i2, j2, valeur)
        else :
            valeur=mouvement.appliquer_mouvement_classique(self.quellePlateau(numPlateau), i1, j1, i2, j2)
            if (valeur==0):
                return
            self.ajoutListe(numPlateau, -valeur) #on inverse le signe de la pièce capturer
        
    def appliquerCoupAleatoire(self, numPlateau) :
        # On récupère la liste complète des coups triés
        liste_coups = self.joueMieuxQuAleatoire(numPlateau)
        
        # On s'assure qu'il y a au moins un coup possible
        if liste_coups:
            # On sélectionne le coup que l'on veut garder (ici, le meilleur qui est à l'indice 0)
            coup_a_jouer = liste_coups[0]
            
            # On applique uniquement ce coup
            self.appliquerCoup(numPlateau, coup_a_jouer)
        else:
            print(f"Aucun coup possible pour le plateau {numPlateau}")

        