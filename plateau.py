#1 pour pion
#2 pour cheval
#3 pour fou
#4 pour tour
#5 pour reine
#6 pour roi


#1 pour le plateau 1
#2 pour le plateau 2


#valeur positive pour les blancs
#valeur négatives pour les noirs


    

def remplissageEchequierCouleur(i, echequier) : #i 1=blanc, -1=noir
    u=7
    if (i==1) :
        u=0
    echequier[u][0]= 4*i
    echequier[u][7]=4*i
    echequier[u][1]=2*i
    echequier[u][6]=2*i
    echequier[u][2]=3*i
    echequier[u][5]=3*i
    echequier[u][3]=5*i
    echequier[u][4]=6*i


def remplissagePionCouleur(i, echequier) :
    u=6
    if (i==1) :
        u=1
    for p in range(8) :
        echequier[u][p]=1*i

def remplissageDeTab(echequier) :
    remplissageEchequierCouleur(1, echequier)
    remplissageEchequierCouleur(-1, echequier)
    remplissagePionCouleur(1, echequier)
    remplissagePionCouleur(-1, echequier)
    return echequier

def remplissage() :
    return remplissageDeTab(creationTableau(8,8))

def remplissageInverse() :
    tab = remplissageDeTab(creationTableau(8,8))
    return inversion(tab)

def inversion(tab) :
    for i in range (8) :
        for j in range (8) :
            tab[i][j]= (-1)*tab[i][j]
    return tab

def creationTableau(ligne, colonne ) :
    echequier = []
    for i in range(ligne):
        rangee =[0]*colonne
        echequier.append(rangee)
    return echequier


def affichageTableau(echequier) :
    print(echequier)


def finDeMatch(echequier, couleur) :
    for i in range (8) :
        for j in range (8) :
            if (tab[i][j]==6*couleur) :
                return false
    if (couleur==1) :
        print("Les noirs ont gagnés, felicitations !")
    else :
        print("Les blancs ont gagnés, felicitations")
    return true

# def main() :
#     tab =creationTableau(8,8)
#     remplissage(tab)
#     affichageTableau(tab)

# if __name__ == "__main__":
#     main()