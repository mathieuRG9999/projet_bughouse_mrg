import affichage
import bughouse

class MainSimulation:

    def __init__(self):
        self.jeu = bughouse.bughouse()

    def run(self):
        tab1 = self.jeu.quellePlateau(1)
        tab2 = self.jeu.quellePlateau(2)
        reserve1 = self.jeu.quelleListe(1)
        reserve2 = self.jeu.quelleListe(2)

        # On appelle ta fonction exactement comme dans ton main normal, 
        # mais en activant le mode simulation !
        affichage.affichageDouble(self.jeu, tab1, tab2, reserve1, reserve2, mode_simulation=True)

if __name__ == "__main__":
    main = MainSimulation()
    main.run()