import tkinter as tk
import plateau as pl
import mouvement as mv


# ─────────────────────────────────────────────
#  CONSTANTES
# ─────────────────────────────────────────────
TAILLE_CASE   = 80   # pixels par case (plateau 8x8 = 640px)
TAILLE_PLATEAU = TAILLE_CASE * 8
COULEUR_CASE_CLAIRE = "#F0D9B5"
COULEUR_CASE_SOMBRE = "#B58863"
COULEUR_PIECE_BLANC = "#FFFDE7"
COULEUR_PIECE_NOIR  = "#212121"
COULEUR_SELECTION   = "#F6F669"


# ─────────────────────────────────────────────
#  EMOJI DES PIÈCES
# ─────────────────────────────────────────────
def emoticoneVal(val):
    # Lettres de notation françaises au lieu des symboles unicode ♙♞... :
    # certains environnements Tk/Fedora n'ont aucune police capable d'afficher
    # ces glyphes rares et retombent sur l'affichage littéral du code (\u2658).
    # Les lettres classiques marchent avec n'importe quelle police, partout.
    correspondance = {
         1: "P",  -1: "p",   # pion
         2: "C",  -2: "c",   # cavalier
         3: "F",  -3: "f",   # fou
         4: "T",  -4: "t",   # tour
         5: "D",  -5: "d",   # dame
         6: "R",  -6: "r",   # roi
    }
    return correspondance.get(val, "")


# ─────────────────────────────────────────────
#  DESSIN DE L'ÉCHIQUIER
# ─────────────────────────────────────────────
def affichageEchequier(canvas):
    for i in range(8):
        for j in range(8):
            couleur = COULEUR_CASE_CLAIRE if (i + j) % 2 == 0 else COULEUR_CASE_SOMBRE
            x0, y0 = j * TAILLE_CASE, i * TAILLE_CASE
            canvas.create_rectangle(x0, y0, x0 + TAILLE_CASE, y0 + TAILLE_CASE,
                                    fill=couleur, outline="")


def surlignerCase(canvas, ligne, col):
    x0, y0 = col * TAILLE_CASE, ligne * TAILLE_CASE
    canvas.create_rectangle(x0, y0, x0 + TAILLE_CASE, y0 + TAILLE_CASE,
                             fill=COULEUR_SELECTION, outline="")


# ─────────────────────────────────────────────
#  DESSIN DES PIÈCES SUR LE PLATEAU
# ─────────────────────────────────────────────
def affichageTableau(canvas, tab):
    for i in range(8):
        for j in range(8):
            val = tab[i][j]
            if val != 0:
                x = j * TAILLE_CASE + TAILLE_CASE // 2
                y = i * TAILLE_CASE + TAILLE_CASE // 2
                rayon = TAILLE_CASE // 2 - 8
                if val > 0:
                    fond, contour, texte = "#FFFDE7", "#8A8A8A", "#111111"
                else:
                    fond, contour, texte = "#3A3A3A", "#000000", "#FFFDE7"
                canvas.create_oval(x - rayon, y - rayon, x + rayon, y + rayon,
                                   fill=fond, outline=contour, width=2)
                canvas.create_text(x, y, text=emoticoneVal(val),
                                   font=("DejaVu Sans", 28, "bold"), fill=texte)


def redessinerPlateau(canvas, tab, selection=None):
    canvas.delete("all")
    affichageEchequier(canvas)
    if selection is not None:
        surlignerCase(canvas, selection[0], selection[1])
    affichageTableau(canvas, tab)


# ─────────────────────────────────────────────
#  DESSIN DE LA RÉSERVE (liste 1D de pièces)
# ─────────────────────────────────────────────
def affichageReserve(canvas, reserve, index_selectionne=None):
    """Affiche la liste des pièces capturées disponibles à poser."""
    canvas.delete("all")
    canvas.create_rectangle(0, 0, canvas.winfo_width(), canvas.winfo_height(),
                             fill="#2E2E2E", outline="")
    canvas.create_text(10, 10, anchor="nw", text="Réserve :",
                       font=("Arial", 11, "bold"), fill="#AAAAAA")
    for i, val in enumerate(reserve):
        x = 30 + i * 55
        y = 40
        couleur = COULEUR_PIECE_BLANC if val > 0 else COULEUR_PIECE_NOIR
        canvas.create_oval(x - 22, y - 22, x + 22, y + 22, fill="#444444", outline="#888888")
        canvas.create_text(x, y, text=emoticoneVal(val),
                           font=("DejaVu Sans", 24, "bold"), fill=couleur)
        if index_selectionne == i:
            canvas.create_oval(x - 24, y - 24, x + 24, y + 24,
                               outline=COULEUR_SELECTION, width=3)


# ─────────────────────────────────────────────
#  ÉTAT GLOBAL DE SÉLECTION
# ─────────────────────────────────────────────
class EtatJeu:
    def __init__(self):
        self.piece_plateau   = None   # (ligne, col) de la pièce sélectionnée sur l'échiquier
        self.piece_reserve   = None   # index dans la liste réserve, ou None
        self.source_active   = None   # "plateau" ou "reserve"


# Un état par "camp" de sélection :
# - etat1 gère : les coups joués sur le plateau 1, ET la pose sur le plateau 1
#   des pièces sélectionnées dans la réserve 2 (reserve capturée sur le plateau 2)
# - etat2 gère : les coups joués sur le plateau 2, ET la pose sur le plateau 2
#   des pièces sélectionnées dans la réserve 1 (reserve capturée sur le plateau 1)
etat1 = EtatJeu()
etat2 = EtatJeu()


# ─────────────────────────────────────────────
#  CLIC SUR L'ÉCHIQUIER (déplacement normal ou pose depuis la réserve)
# ─────────────────────────────────────────────
def clicPlateau(etat, jeu, numPlateau, reserveNum, event, canvas, reserve_canvas1, reserve_canvas2):
    tab = jeu.getPlateau(numPlateau)
    reserve = jeu.getListe(reserveNum)

    # CORRECTION ICI :
    # Si on est sur le Plateau 1, on pose depuis la Réserve 2 (affichée sur reserve_canvas1 sous le plateau 1)
    # Si on est sur le Plateau 2, on pose depuis la Réserve 1 (affichée sur reserve_canvas2 sous le plateau 2)
    canvas_reserve_pose = reserve_canvas1 if numPlateau == 1 else reserve_canvas2
    
    # Quand on mange sur le Plateau 1, la pièce va dans la Réserve 1 (qui est affichée sous le Plateau 2)
    # Quand on mange sur le Plateau 2, la pièce va dans la Réserve 2 (qui est affichée sous le Plateau 1)
    canvas_reserve_capture = reserve_canvas2 if numPlateau == 1 else reserve_canvas1

    col   = event.x // TAILLE_CASE
    ligne = event.y // TAILLE_CASE

    if not (0 <= ligne < 8 and 0 <= col < 8):
        return

    # ── CAS 1 : une pièce de la réserve est déjà sélectionnée ──
    if etat.source_active == "reserve" and etat.piece_reserve is not None:
        val = reserve[etat.piece_reserve]
        if jeu.validerAjoutPiece(reserveNum, numPlateau, val, ligne, col):
            jeu.retirerDeReserve(reserveNum, etat.piece_reserve)
            tab[ligne][col] = val
            affichageReserve(canvas_reserve_pose, reserve)
        etat.piece_reserve  = None
        etat.source_active  = None
        redessinerPlateau(canvas, tab)
        return

    # ── CAS 2 : premier clic → sélection d'une pièce sur le plateau ──
    if etat.source_active is None:
        if tab[ligne][col] != 0:
            etat.piece_plateau = (ligne, col)
            etat.source_active = "plateau"
            redessinerPlateau(canvas, tab, selection=(ligne, col))
        return

    # ── CAS 3 : deuxième clic → déplacement ──
    if etat.source_active == "plateau" and etat.piece_plateau is not None:
        li, co = etat.piece_plateau
        if (li, co) != (ligne, col):
            couleur = jeu.getCouleur(numPlateau)
            cases_possibles = mv.mouvement(tab, li, co, couleur)
            if (ligne, col) in cases_possibles:
                valeurMangee = mv.recupererValeurSupp(tab, li, co, ligne, col)
                if valeurMangee != 0:
                    liste_reserve = jeu.getListe(numPlateau)
                    liste_reserve.append(valeurMangee)
                    affichageReserve(canvas_reserve_capture, liste_reserve)
                jeu.incrementerCouleur(numPlateau)
        etat.piece_plateau = None
        etat.source_active = None
        redessinerPlateau(canvas, tab)

# ─────────────────────────────────────────────
#  CLIC SUR LA RÉSERVE
# ─────────────────────────────────────────────
def clicReserve(etat, reserve, canvas_reserve, event):
    index = event.x // 55   # même espacement que dans affichageReserve
    if 0 <= index < len(reserve):
        etat.piece_reserve  = index
        etat.piece_plateau  = None
        etat.source_active  = "reserve"
        affichageReserve(canvas_reserve, reserve, index_selectionne=index)
        print(f"Réserve : pièce sélectionnée → {emoticoneVal(reserve[index])}")


# ─────────────────────────────────────────────
#  FENÊTRE PRINCIPALE (mode bughouse double plateau)
# ─────────────────────────────────────────────
def affichageDouble(jeu, tab1, tab2, reserve1, reserve2):
    """
    Affiche deux échiquiers côte à côte avec leurs réserves respectives.
    - reserve1 : pièces capturées par l'équipe du plateau 1 (disponibles sur plateau 2)
    - reserve2 : pièces capturées par l'équipe du plateau 2 (disponibles sur plateau 1)
    """
    fenetre = tk.Tk()
    fenetre.title("Bughouse Chess")
    fenetre.configure(bg="#1A1A1A")

    # ── Plateau 1 ──
    canvas1 = tk.Canvas(fenetre, width=TAILLE_PLATEAU, height=TAILLE_PLATEAU, highlightthickness=0)
    canvas1.grid(row=0, column=0, padx=10, pady=10)

    hauteur_reserve = 80
    largeur_reserve = TAILLE_PLATEAU
    reserve_canvas1 = tk.Canvas(fenetre, width=largeur_reserve, height=hauteur_reserve,
                                bg="#2E2E2E", highlightthickness=0)
    reserve_canvas1.grid(row=1, column=0, padx=10, pady=(0, 10))

    # ── Plateau 2 ──
    canvas2 = tk.Canvas(fenetre, width=TAILLE_PLATEAU, height=TAILLE_PLATEAU, highlightthickness=0)
    canvas2.grid(row=0, column=1, padx=10, pady=10)

    reserve_canvas2 = tk.Canvas(fenetre, width=largeur_reserve, height=hauteur_reserve,
                                bg="#2E2E2E", highlightthickness=0)
    reserve_canvas2.grid(row=1, column=1, padx=10, pady=(0, 10))

    # ── Dessin initial ──
    redessinerPlateau(canvas1, tab1)
    redessinerPlateau(canvas2, tab2)
    affichageReserve(reserve_canvas1, reserve1)
    affichageReserve(reserve_canvas2, reserve2)

    # ── Bindings plateau 1 : coups + pose des pièces de la réserve2 ──
    canvas1.bind("<Button-1>",
        lambda e: clicPlateau(etat1, jeu, 1, 2, e, canvas1, reserve_canvas1, reserve_canvas2))
    reserve_canvas2.bind("<Button-1>",
        lambda e: clicReserve(etat1, reserve2, reserve_canvas2, e))

    # ── Bindings plateau 2 : coups + pose des pièces de la réserve1 ──
    canvas2.bind("<Button-1>",
        lambda e: clicPlateau(etat2, jeu, 2, 1, e, canvas2, reserve_canvas1, reserve_canvas2))
    reserve_canvas1.bind("<Button-1>",
        lambda e: clicReserve(etat2, reserve1, reserve_canvas1, e))

    fenetre.mainloop()


# ─────────────────────────────────────────────
#  MODE SIMPLE (un seul plateau, debug — sans réserve/bughouse)
# ─────────────────────────────────────────────
def affichageComplet(tab):
    fenetre = tk.Tk()
    fenetre.title("Échecs")
    canvas = tk.Canvas(fenetre, width=TAILLE_PLATEAU, height=TAILLE_PLATEAU, highlightthickness=0)
    canvas.pack()
    redessinerPlateau(canvas, tab)

    etat = EtatJeu()
    couleur = {"valeur": 0}

    def clic(event):
        col   = event.x // TAILLE_CASE
        ligne = event.y // TAILLE_CASE
        if not (0 <= ligne < 8 and 0 <= col < 8):
            return
        if etat.piece_plateau is None:
            if tab[ligne][col] != 0:
                etat.piece_plateau = (ligne, col)
                redessinerPlateau(canvas, tab, selection=(ligne, col))
            return
        li, co = etat.piece_plateau
        if (li, co) != (ligne, col):
            cases_possibles = mv.mouvement(tab, li, co, couleur["valeur"])
            if (ligne, col) in cases_possibles:
                mv.recupererValeurSupp(tab, li, co, ligne, col)
                couleur["valeur"] = (couleur["valeur"] + 1) % 2
        etat.piece_plateau = None
        redessinerPlateau(canvas, tab)

    canvas.bind("<Button-1>", clic)
    fenetre.mainloop()