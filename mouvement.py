import plateau
#on doit faire en sorte de pourvoir bouger de plusieurs manière avec la ligne de commande

#la premiere maniere c'est en disant uniquement ou on veut aller, on regarde les différents moyens et on au hasard
#a partit

# couleur =0

def verifLimitHauteur(tab, i) :
    return not (i<0 or i>= len(tab)) 

def verifLimitLargeur(tab, i, j) :
    return not (i<0 or j>= len(tab[i])) 

def signe(val) :
    return abs(val)//val

#on fera après le en passant

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
            if (verifLimitHauteur(tab, i+direction)) :
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

def mouvementFou(i, j) :
    caseDispo= []
    for p in range(8) :
        caseDispo.append((i+p, j+p)) 
        caseDispo.append((i+p, j-p))
        caseDispo.append((i-p, j+p))
        caseDispo.append((i-p, j-p))
    return caseDispo

def conditionAjoutMvtTour(verif, i, j, liste) :
    if (verif) :
        liste.append((i, j))

def mouvementTour(tab, i, j, couleur) :
    caseDispo= []
    coord =[]
    precedent =[True, True, True, True]
    for p in range(8) :
        i1=i+p
        i2=i-p
        j1=j-p
        j2=j+p
        coord=[(i1, j), (i2, j), (i, j1), (i, j2)]

        for u in range (4) :
            x,y = coord[u]
            verif =limiteEchequier(x, y)
            precedent[u]=(verif and caseEstOccupe(tab,x, y, couleur )) and precedent[u]
            if (verif and tab[x][y]!=0) :
                precedent[u]= False
            conditionAjoutMvtTour(precedent[u], x, y, caseDispo)
    return caseDispo  

def mouvementReine(tab, i, j, couleur) :
    caseDispo= []
    caseDispo= mouvementFou(i, j)
    caseDispo+= (mouvementTour(tab, i , j, couleur))
    return caseDispo

def mouvementRoi(i, j) :
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
        return mouvementFou(i, j)
    if (valeur==4) : #cas tour
        return mouvementTour(tab, i, j, couleur)
    if (valeur==5) : #cas reine
        return mouvementReine(tab, i, j, couleur)
    if (valeur==6) : #cas roi
        return mouvementRoi(i, j)
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

def recupererValeurSupp(tab, xInitial, yInitial, xFutur, yFutur) :
    ancienneValeur=tab[xFutur][yFutur]
    tab[xFutur][yFutur] = tab[xInitial][yInitial]
    tab[xInitial][yInitial] = 0
    return ancienneValeur #elle est à 0 s'il n'y avait rien

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
    if (couleurBlanche(tab, i, j, couleur)) :
        print("la couleur actuelle est ", couleur)
        case =mouvementPossibleEchequierVide(tab, i, j, couleur)
        case =mouvementDansLesLimites(case, tab)
        return mouvementLogique(tab, case, couleur)

    print("ce n'est pas à votre tour")
    return []

def mouvementLegal(tab, i, j) :
    return not (verifLimitHauteur(tab, i) or verifLimitLargeur(tab, i, j))

def listeCaseLibre(tab) :
    liste=[]
    for i in range (8) :
        for j in range (8) :
            if (tab[i][j]==0) :
                liste.append((i,j))
    return liste