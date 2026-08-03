import plateau
import math
#on doit faire en sorte de pourvoir bouger de plusieurs manière avec la ligne de commande

#la premiere maniere c'est en disant uniquement ou on veut aller, on regarde les différents moyens et on au hasard
#a partit

# couleur =0

tabBoolRoi= [False, False]
tabBoolTour=[False, False, False, False] #  TB1, TB2, TN1, TN2

tabBoolPionB=[False, False, False, False, False, False, False, False] # pion blanc en Passant possible
tabBoolPionN=[False, False, False, False, False, False, False, False] # pion blanc en Passant possible


def verifLimitHauteur(tab, i) :
    return not (i<0 or i>= len(tab)) 

def verifLimitLargeur(tab, i, j) :
    return not (j<0 or j>= len(tab[i])) 

def signe(val) :
    if (val==0) :
        return 0
    return abs(val)//val

#on fera après le en passant, le coup du rock et le timer

def PionMange(tab, i,j) :
    liste =[]
    i=i+1*signe(tab[i][j])
    j1= j+1
    j2=j-1
    if (not verifLimitHauteur(tab, i)) :
        return liste
    if (limiteEchequierUnique(j1) and tab[i][j1]!=0) :
        liste.append((i, j1))
    if  (limiteEchequierUnique(j2) and tab[i][j2]!=0) : 
        liste.append((i, j2))
    return liste

def mouvementPion(tab, i, j) :
    liste= PionMange(tab, i, j)
    val =tab[i][j]
    direction = signe(val)
    if (abs(val)==1) :
        if (((i==1) and (direction>0)) or ((i==6) and (direction<0))) :
            if (verifLimitHauteur(tab, i+direction) and tab[i+direction][j]==0) :
                liste.append((i+direction, j))
                if (verifLimitHauteur(tab, i+2*direction) and tab[i+direction*2][j]==0) :
                    liste.append((i+2*direction, j))
        else  :
            if (verifLimitHauteur(tab, i+direction) and tab[i+1][j]==0) :
                liste.append((i+direction, j))
    return liste

def changement(tab, i, j, val, direction) :
    tab[i][j]=val*direction
    return tab[i][j]

def promotionPion(tab, i, j) :
    reponse=0
    while (reponse==0):
        direction = signe(tab[i][j])
        reponse = input("Quel promotion veut tu faire R (reine), T (tour), F (fou), C (cheval): ")
        changement(tab, i, j, letter_to_troops(reponse), direction)
        reponse = letter_to_troops(reponse)
    print("vous avez fait la promotion d'un pion")

def promotion(tab, i, j, val) : #a verifier si c'est correct
    changement(tab, i, j, val, direction)


def letter_to_troops(reponse) :
    if (reponse == "R") :
        return 5
    if (reponse == "T") :
        return 4
    if (reponse =="F") :
        return 3
    if (reponse=="C") :
        return 2
    return 0

def mouvementFou(tab, i, j) :
    caseDispo = []
    directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)] # Les 4 diagonales
    
    for dx, dy in directions:
        x, y = i + dx, j + dy
        # Tant qu'on reste sur le plateau
        while limiteEchequier(x, y):
            caseDispo.append((x, y))
            # Si on croise une pièce (qu'elle soit à 0 ou non), on s'arrête
            if tab[x][y] != 0: 
                break
            # Sinon, on continue d'avancer d'une case dans la même direction
            x += dx
            y += dy
            
    return caseDispo

def mouvementTour(tab, i, j) :
    caseDispo = []
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)] # Les 4 lignes droites
    
    for dx, dy in directions:
        x, y = i + dx, j + dy
        while limiteEchequier(x, y):
            caseDispo.append((x, y))
            if tab[x][y] != 0: 
                break
            x += dx
            y += dy
            
    return caseDispo

def mouvementReine(tab, i, j) :
    # La reine combine simplement les mouvements du Fou et de la Tour
    return mouvementFou(tab, i, j) + mouvementTour(tab, i, j)


def rajoutEnPassant(tab, i, j) :
    if (tab[i][j]>0) :
        return rajoutEnPassantNeutre(tab, i, j, tabBoolPionN, 1)
    else :
        return rajoutEnPassantNeutre(tab, i, j, tabBoolPionB, -1)


def rajoutEnPassantNeutre(tab, i, j, tabATester ,signe) :
    liste=[]
    if (tab[i+1*signe][j+1]==0 and tabATester[j+1]==True) :
        liste.append((i+1, j+1))
    if (tab[i+1*signe][j-1]==0 and tabATester[j-1]==True) :
        liste.append((i+1,j-1))
    return liste

# def rajoutEnPassantBlanc(tab, i, j) :
#     liste=[]
#     if (tab[i+1][j+1]==0 and tabBoolPionB[j+1]==True) :
#         liste.append((i+1, j+1))
#     if (tab[i+1][j-1]==0 and tabBoolPionB[j+1]==True) :
#         liste.append((i+1,j-1))
#     return liste

# def rajoutEnPassantBlanc(tab, i, j) :
#     liste=[]
#     if (tab[i-1][j+1]==0 and tabBoolPionN[j+1]==True) :
#         liste.append((i+1, j+1))
#     if (tab[i-1][j-1]==0 and tabBoolPionN[j+1]==True) :
#         liste.append((i+1,j-1))
#     return liste

def casRoqueVerif(tab, i, j, positionIBoucle, positionFBoucle, indice) :
    for u in range (positionIBoucle, positionFBoucle) :
        if (tab[indice][u]!=0) :
            return False
    return True

def ajoutMouvementRoque(tab, i, j) :
    liste= []
    indice=1
    if (tab[i][j]>0) :
        indice=0
    if ((not tabBoolRoi[indice])) :
        if ((not tabBoolTour[indice*2]) and casRoqueVerif(tab, i, j,1, 4, indice)) :
            liste.append((i, j-2))
        if ((not tabBoolTour[indice*2+1]) and casRoqueVerif(tab, i, j,5, 7, indice)) :
            liste.append((i, j+2))
    return liste

def mouvementRoi(tab, i, j) :
    liste= []
    for x in range (-1,2) :
        for y in range(-1, 2) :
            if (i+x,j+y)!=(i, j) :
                liste.append((x+i, y+j))
    return liste

def limiteEchequierUnique(x) :
    return 0<=x<8

def limiteEchequier(x, y) :
    return limiteEchequierUnique(x) and limiteEchequierUnique(y)

def verifCheval(x, y) :
    return (abs(x)==1 and abs(y)==2)

def verifChevalComplet(x, y , i, j) :
    return (verifCheval(x, y) or verifCheval(y,x )) and limiteEchequier(x+i, y+j)

def mouvementCheval(i, j) :
    liste=[]
    for x in range (-2, 3) :
        for y in range (-2, 3) :
            if (verifChevalComplet(x,y, i, j)) :
                liste.append((i+x,j+ y))
    return liste

def mouvementPossibleEchequierVide(tab, i, j, couleur) :
    caseDispo= []
    valeur =abs(tab[i][j])
    if (not verifLimitHauteur(tab, i) or not verifLimitLargeur(tab, i, j)) :
        return caseDispo
    if (valeur==1) : # cas ou on a un pion
        return mouvementPion(tab, i, j)
    if (valeur==2) : #cas ou on a un cheval
        return mouvementCheval(i, j)
    if (valeur==3) :#cas fou
        return mouvementFou(tab, i, j)  # <-- Ajout de 'tab' ici
    if (valeur==4) : #cas tour
        return mouvementTour(tab, i, j) # <-- Plus besoin de 'couleur', juste 'tab'
    if (valeur==5) : #cas reine
        return mouvementReine(tab, i, j) # <-- Ajout de 'tab' ici
    if (valeur==6) : #cas roi
        liste=mouvementRoi(tab, i, j)
        liste.extend(ajoutMouvementRoque(tab, i, j))
        return liste
    return caseDispo

def mouvementDansLesLimites(listeXY, tab) : #cette méthode pourra être optimiser afin de limiter les cases regarder, mais est ce que ca change vraiment qqch ?
    case= []
    for x,y in listeXY :
        if (verifLimitHauteur(tab, x) and verifLimitLargeur(tab, x, y)) : #on fait la supposition que l'echiquier est carré
            case.append((x,y))
    return case

def caseEstOccupe(tab, i, j, couleur) : #maintenant on regarde si on peut manger quelque chose
    if (couleur==0 and tab[i][j]>0) :
        return True
    if (couleur==1 and tab[i][j]<0) :
        return True
    return False

def mangerTroupeAdverse(tab, i, j, couleur) :
    return (caseEstOccupe(tab, i, j, couleur) and tab[i][j]!=0)

def valeurMange(tab, i, j) :
    return tab[i][j]

# def recupererValeurSupp(tab, xInitial, yInitial, xFutur, yFutur) :
#     ancienneValeur=tab[xFutur][yFutur]
#     tab[xFutur][yFutur] = tab[xInitial][yInitial]
#     tab[xInitial][yInitial] = 0
#     return ancienneValeur #elle est à 0 s'il n'y avait rien

def deposerPiece(tab, val, x, y) :
    tab[x][y]=val

def couleurPaireOuImpaire(couleur) :
    if (couleur ==10) :
        couleur=0
    return couleur%2

def mouvementLogique(tab, listeXY, couleur) :
    case=[]
    for x,y in listeXY :
        if (not caseEstOccupe(tab, x, y, couleur)) :
            case.append((x, y))
    return case

def couleurBlanche(tab, i, j, couleur) :
    return (((couleur %2) ==0) and tab[i][j]>0) or (((couleur %2) !=0) and tab[i][j]<0)

def mouvement(tab, i, j, couleur) :
    if (plateau.finDeMatch(tab, couleur)) :
        print("le match est fini, un roi est mort, il n'est plus possible de jouer")
        return
    if (couleurBlanche(tab, i, j, couleur)) :
        #print("la couleur actuelle est ", couleur)
        case =mouvementPossibleEchequierVide(tab, i, j, couleur)
        case =mouvementDansLesLimites(case, tab)
        return mouvementLogique(tab, case, couleur)

    print("ce n'est pas à votre tour")
    return []

def mouvementEnsembleEchequierPourUneCouleur(tab, couleur) : #permet d'avoir l'ensemble des coups (case dep->case z)
    liste= []
    for i in range (8):
        for j in range (8):
            if (tab[i][j]!=0 and couleurBlanche(tab, i, j, couleur)) :
                depart=(i, j)
                destination=mouvement(tab, i, j, couleur)

                for dest in destination :
                    pieceMangee=tab[dest[0]][dest[1]]
                    liste.append((depart, dest, pieceMangee))
    return liste

def mouvementLegal(tab, i, j) :
    return not (verifLimitHauteur(tab, i) or verifLimitLargeur(tab, i, j))

def listeCaseLibre(tab) :
    liste=[]
    for i in range (8) :
        for j in range (8) :
            if (tab[i][j]==0) :
                liste.append((i,j))
    return liste

def valeurMouvement(tab, i, j, i1, j1) : #pour l'instant, on suppose que les pièces valent strictement la même chose
    #je pense qu'elles ont un poids évolutif en fonction de l'avancement de la partie, mais à vérifier
    if (i==-1) :
        return heuristiquePoserTroupe(tab, j, i1, j1)
    signePieceInitial =signe(tab[i][j])
    signePieceFinale =signe(tab[i1][j1])
    if (abs(tab[i1][j1])==6) : #cas ou on peut manger le roi
        return math.sup
    return min(abs(tab[i1][j1]), mauvaisMouvementValeur(tab, i, j, i1, j1))

def heuristiquePoserTroupe(tab, valeur, x, y) :
    return valeur*1.5 #on fera quelque chose d'un peu plus détaillé par la suite

def mauvaisMouvementValeur(tab, i, j, i1, j1) :
    if (abs(tab[i][j])==1) :
        if ((i==1) or (i==6) and j==5) :
            return -10 # c'est une valeur arbitraire pour le moment, pour pas qu'il ne le fasse
    return 0

def forcer_mouv_tour_cas_roque(tab, i2, j2) :
    indice=1
    if (i2==-1) :
        indice=1
    if (j2==2) :
        tab[i2][3]=4*indice
        tab[i2][0]=0
    if (i2==0 and j2==6) :
        tab[i2][5]=4*indice
        tab[i2][7]=0

def activationEnPassant(tab, i, j) :
    if (tab[i][j]==1) : #cas d'un pion
        tabBoolPionB[j]=True
    if (tab[i][j]==-1) : #cas d'un pion
        tabBoolPionN[j]=True





def peut_on_appliquer_mvt_en_passant(tab, i1, j1, i2, j2) :
    indiceJDroite=j1+1
    indiceJGauche=j1-1

    indiceMonter=i1+1
    tabATester=tabBoolPionN
    valeurATester=-1
    val=tab[i1][j1]

    if (tab[i1][j1]==1): #pour les noits
        indiceMonter=i1-1
        tabATester=tabBoolPionB
        valeurATester=1

    return (tab[i1][indiceJDroite]==valeurATester and tabATester[indiceJDroite]==True and tab[indiceMonter][indiceJDroite]==0 and i2==indiceMonter and j2==indiceJDroite) or (tab[i1][indiceJGauche]==valeurATester and tabATester[indiceJGauche]==True and tab[indiceDescendre][indiceJGauche]==0 and i2)
    



def appliquer_mouvement_en_passant(tab, i1, j1, i2, j2) :
    indiceJDroite=j1+1
    indiceJGauche=j1-1

    indiceMonter=i1+1
    indiceDescendre=i1-1
    tabATester=tabBoolPionN
    valeurATester=-1
    val=tab[i1][j1]


    if (tab[i1][j1]==1): #pour les noits
        indiceMonter=i1-1
        tabATester=tabBoolPionB
        valeurATester=1
        # a droite
    if (tab[i1][indiceJDroite]==valeurATester and tabATester[indiceJDroite]==True and tab[indiceMonter][indiceJDroite]==0 and i2==indiceMonter and j2==indiceJDroite) :
        tab[i2][j2]=val
        tab[i1][j1]=0
        valeur=tab[i1][indiceJDroite]
        tab[i1][indiceJDroite]=0
        tabATester[indiceJDroite] =False
        return valeur

        # a gauche
    if (tab[i1][indiceJGauche]==valeurATester and tabATester[indiceJGauche]==True and tab[indiceDescendre][indiceJGauche]==0 and i2) : 
        tab[i2][j2]=val
        tab[i1][j1]=0
        valeur=tab[i1][indiceJGauche]
        tab[i1][indiceJGauche]=0
        tabATester[indiceJGauche] =False
        return valeur

def verificationCasserEnPassantFactoriser(i2, j2, aux, position) :
    if (aux[j2]==True) : #on fais d'abord le cas blanc après on passera au noir et on factorisera
        if (i2==position) :
            aux[j2]= False

def verificationCasserEnPassant(tab, i1, j1, i2, j2) :
    verificationCasserEnPassantFactoriser(i2, j2, tabBoolPionB, 2)
    verificationCasserEnPassantFactoriser(i2, j2, tabBoolPionB, 5)



    

def appliquer_mouvement_classique(tab, i1, j1, i2, j2) : #on suppose qu'uniquement des coups légaux sont données
    if (peut_on_appliquer_mvt_en_passant) :
        appliquer_mouvement_en_passant(tab, i1, j1, i2, j2)

    if (abs(tab[i1][j1])==6 and abs(j1-j2)==2) : # on est dans le cas d'un roque
        forcer_mouv_tour_cas_roque(tab, i2, j2)
    if (abs(tab[i1][j1]==1)) :
        #Cas ou on active l'en passant
        if (abs(j1-j2)==2 and i1==i2 and ((i1==1 and i2==3) or (i1==6 and i2==4))) :
            activationEnPassant(tab, i1, j1)

    verificationCasserEnPassant(tab, i1, j1, i2, j2)
    enleverRoque(tab, i1, j1)
    valeur =tab[i2][j2]
    tab[i2][j2]=tab[i1][j1]
    tab[i1][j1]=0
    return valeur




def casStupideRoqueFactorisation(c1, c2, indice) :
    if (c1 and c2) :
        tabBoolRoi[indice]=True
        return True
    return False
 
def casStupideRoque(tab, i, j) :
    indice=0
    if (tab[i][j]<0) :
        indice=1
    casStupideRoqueFactorisation(tabBoolTour[indice*2], tabBoolTour[indice*2+1], indice)
    return tabBoolRoi[indice]

def enleverRoque(tab, i, j) :
    if (casStupideRoque(tab, i, j)) :
        return
    enleverRoqueRoi(tab, i, j)
    enleverRoqueTour(tab, i, j)

def enleverRoqueTour(tab, i1, j1) :
    #on verifie si l'une des tours a bouges
    coordGenante= [(0,0), (0, 7), (7,0), (7, 7)]
    for i in range (4) :
        x, y = coordGenante[i]
        if (i1==x and j1==y) :
            tabBoolTour[i]=True

def enleverRoqueRoi(tab, i1, j1) :
    #on verifie si l'une des tours a bouges
    coordGenante= [(0,4), (7, 4)]
    for i in range (2) :
        x, y = coordGenante[i]
        if (i1==x and j1==y) :
            tabBoolRoi[i]=True



def poserSurPlateau(tab, i, j, val) :
    tab[i][j]=val

def mouvement_to_string(tab, coup) :
    depart, arrivee, pieceMangee = coup
    i1, j1 =depart
    i2, j2 = arrivee
    if (i1==-1) : #on est dans le cas ou on pose qqch
        piece = plateau.affichage_piece(j1)
        print("on place un ", piece, " en (", i2,", ", j2, ") et on a mangé un ", plateau.affichage_piece(pieceMangee))
    else :
        print("(",i1, ", ", j1, ")", "-> (", i2,",", j2,")")
    print(", valeur =", valeurMouvement(tab, i1, j1, i2, j2))
    