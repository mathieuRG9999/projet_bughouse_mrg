import tkinter as tk
import plateau as pl
import mouvement as mv
import bughouse as bg


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
    correspondance = {
         1: "♙",  -1: "♟",
         2: "♘",  -2: "♞",
         3: "♗",  -3: "♝",
         4: "♖",  -4: "♜",
         5: "♕",  -5: "♛",
         6: "♔",  -6: "♚",
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
                couleur = COULEUR_PIECE_BLANC if val > 0 else COULEUR_PIECE_NOIR
                canvas.create_text(x, y, text=emoticoneVal(val),
                                   font=("Arial", 36), fill=couleur)


def redessinerPlateau(canvas, tab):
    canvas.delete("all")
    affichageEchequier(canvas)
    affichageTableau(canvas, tab)


# ─────────────────────────────────────────────
#  DESSIN DE LA RÉSERVE (liste 1D de pièces)
# ─────────────────────────────────────────────
def affichageReserve(canvas, reserve):
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
                           font=("Arial", 28), fill=couleur)


# ─────────────────────────────────────────────
#  ÉTAT GLOBAL DE SÉLECTION
# ─────────────────────────────────────────────
class EtatJeu:
    def __init__(self):
        self.piece_plateau   = None   # (ligne, col) de la pièce sélectionnée sur l'échiquier
        self.piece_reserve   = None   # index dans la liste réserve, ou None
        self.source_active   = None   # "plateau" ou "reserve"

etat1 = EtatJeu() #pour le plateau1
etat2 = EtatJeu() #pour le plateau2

# ─────────────────────────────────────────────
#  CLIC SUR L'ÉCHIQUIER (déplacement normal)
# ─────────────────────────────────────────────
def clicPlateau(etat, event, tab, canvas, canvas_reserve, reserve):
    col   = event.x // TAILLE_CASE
    ligne = event.y // TAILLE_CASE

    if not (0 <= ligne < 8 and 0 <= col < 8):
        return

    # ── CAS 1 : une pièce de la réserve est déjà sélectionnée ──
    if etat.source_active == "reserve" and etat.piece_reserve is not None:
        if tab[ligne][col] == 0:   # on ne pose que sur une case vide
            val = reserve[etat.piece_reserve]
            if bg.validerAjoutPiece(val, ligne, col):
                tab[ligne][col] = val
                reserve.pop(etat.piece_reserve)
                affichageReserve(canvas_reserve, reserve)
        etat.piece_reserve  = None
        etat.source_active  = None
        redessinerPlateau(canvas, tab)
        return

    # ── CAS 2 : premier clic → sélection d'une pièce sur le plateau ──
    if etat.source_active is None:
        if tab[ligne][col] != 0:
            etat.piece_plateau = (ligne, col)
            etat.source_active = "plateau"
            redessinerPlateau(canvas, tab)
            surlignerCase(canvas, ligne, col)
            affichageTableau(canvas, tab)
        return

    # ── CAS 3 : deuxième clic → déplacement ──
    if etat.source_active == "plateau" and etat.piece_plateau is not None:
        li, co = etat.piece_plateau
        if (li, co) != (ligne, col):
            cases_possibles = mv.mouvement(tab, li, co)
            if (ligne, col) in cases_possibles:
                mv.recupererValeurSupp(tab, li, co, ligne, col)
                mv.incrementerCouleur()
        etat.piece_plateau = None
        etat.source_active = None
        redessinerPlateau(canvas, tab)


# ─────────────────────────────────────────────
#  CLIC SUR LA RÉSERVE
# ─────────────────────────────────────────────
def clicReserve(event, reserve, canvas_reserve):
    index = event.x // 55   # même espacement que dans affichageReserve
    if 0 <= index < len(reserve):
        etat.piece_reserve  = index
        etat.piece_plateau  = None
        etat.source_active  = "reserve"
        # Surligner la pièce sélectionnée dans la réserve
        affichageReserve(canvas_reserve, reserve)
        x = 30 + index * 55
        canvas_reserve.create_oval(x - 24, 16, x + 24, 64,
                                   outline=COULEUR_SELECTION, width=3)
        print(f"Réserve : pièce sélectionnée → {emoticoneVal(reserve[index])}")


# ─────────────────────────────────────────────
#  FENÊTRE PRINCIPALE (mode bughouse double plateau)
# ─────────────────────────────────────────────
def affichageDouble(tab1, tab2, reserve1, reserve2):
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

    # Réserve pour plateau 1 (pièces envoyées par l'équipe du plateau 2)
    hauteur_reserve = 80
    largeur_reserve = TAILLE_PLATEAU
    reserve_canvas1 = tk.Canvas(fenetre, width=largeur_reserve, height=hauteur_reserve,
                                bg="#2E2E2E", highlightthickness=0)
    reserve_canvas1.grid(row=1, column=0, padx=10, pady=(0, 10))

    # ── Plateau 2 ──
    canvas2 = tk.Canvas(fenetre, width=TAILLE_PLATEAU, height=TAILLE_PLATEAU, highlightthickness=0)
    canvas2.grid(row=0, column=1, padx=10, pady=10)

    # Réserve pour plateau 2
    reserve_canvas2 = tk.Canvas(fenetre, width=largeur_reserve, height=hauteur_reserve,
                                bg="#2E2E2E", highlightthickness=0)
    reserve_canvas2.grid(row=1, column=1, padx=10, pady=(0, 10))

    # ── Dessin initial ──
    redessinerPlateau(canvas1, tab1)
    redessinerPlateau(canvas2, tab2)
    affichageReserve(reserve_canvas1, reserve1)
    affichageReserve(reserve_canvas2, reserve2)

    # ── Bindings plateau 1 ──
    canvas1.bind("<Button-1>",
        lambda e: clicPlateau(etat1, e, tab1, canvas1, reserve_canvas1, reserve1))
    reserve_canvas1.bind("<Button-1>",
        lambda e: clicReserve(etat2, e, reserve1, reserve_canvas1))

    # ── Bindings plateau 2 ──
    canvas2.bind("<Button-1>",
        lambda e: clicPlateau(e, tab2, canvas2, reserve_canvas2, reserve2))
    reserve_canvas2.bind("<Button-1>",
        lambda e: clicReserve(e, reserve2, reserve_canvas2))

    fenetre.mainloop()


# ─────────────────────────────────────────────
#  MODE SIMPLE (un seul plateau, debug)
# ─────────────────────────────────────────────
def affichageComplet(tab):
    fenetre = tk.Tk()
    fenetre.title("Échecs")
    canvas = tk.Canvas(fenetre, width=TAILLE_PLATEAU, height=TAILLE_PLATEAU, highlightthickness=0)
    canvas.pack()
    redessinerPlateau(canvas, tab)
    canvas.bind("<Button-1>",
        lambda e: clicPlateau(e, tab, canvas, None, []))
    fenetre.mainloop()