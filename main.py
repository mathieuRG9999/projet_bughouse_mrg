import affichage
import bughouse


class Main:

    def __init__(self):
        self.jeu = bughouse.bughouse()

    def run(self):
        tab1 = self.jeu.quellePlateau(1)
        tab2 = self.jeu.quellePlateau(2)

        # Les réserves : à récupérer depuis ton objet bughouse
        reserve1 = self.jeu.quelleListe(1)
        reserve2 = self.jeu.quelleListe(2)

        # Une seule fenêtre avec les deux plateaux côte à côte
        affichage.affichageDouble(self.jeu, tab1, tab2, reserve1, reserve2)


if __name__ == "__main__":
    main = Main()
    main.run()