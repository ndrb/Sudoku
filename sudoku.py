# -*- coding: utf-8 -*-

import argparse
import copy
import re
import os
import time
import numpy as np

from importlib.machinery import SourceFileLoader

# Enable command line history


regex_action = r'^\(([0-8]),([0-8])\)\s*=\s*([0-9])$'


def est_coup_legal(X, v, etat):
    estLegal = True
    estLegal &= v not in etat.tableau[X[0], :]  # Contraintes de ligne
    estLegal &= v not in etat.tableau[:, X[1]]  # Contraintes de colonnes
    blocY, blocX = (X[0]//3)*3, (X[1]//3)*3
    # Contraintes de blocs
    estLegal &= v not in etat.tableau[blocY:blocY+3, blocX:blocX+3]
    return estLegal


def joueur_humain(etat_depart, fct_but, fct_transitions, fct_heuristique):
    etat = etat_depart
    yield etat
    while not fct_but(etat):
        action = input(
            "Entrer une coordonnée et une valeur. (ex. '(Y,X) = V'). " +
            "Pour effacer mettez V à 0.\n")
        while True:
            try:
                y, x, v = re.match(regex_action, action).groups()
                y, x = int(y), int(x)

                if v == '0':
                    v = ' '
                    break

                if not est_coup_legal((y, x), v, etat):
                    print(
                        "Coup non légal! [ ({0},{1}) = {2} ]".format(y, x, v))
                    raise NameError('Coup non légal!')

                break
            except:
                action = input(
                    "L\'action n\'est pas valide. Réessayer à nouveau, puis" +
                    " appuyer sur Enter\n")

        etat = etat.placer((y, x), v)
        yield etat


class Jeu:
    """
    Classe de jeu.

    Initialisation à partir de la fonction but,
    fonction transitions et l'état inital du jeu.

    La méthode "jouer_partie" simule une partie.
    """

    def __init__(
        self,
        etat_depart,
        fct_but,
        fct_transitions,
        fct_heuristique,
        verbose=False
    ):
        self.etat_initial = etat_depart
        self.but = fct_but
        self.transitions = fct_transitions
        self.heuristique = fct_heuristique
        self.verbose = verbose

    def jouer_partie(self, joueur):
        etat = self.etat_initial

        for etat in joueur(etat, self.but, self.transitions, self.heuristique):
            self.afficher(etat)

        if self.but(etat):
            print('Vous avez gagné!')
        else:
            print('Vous avez perdu!')

    def afficher(self, msg):
        if self.verbose:
            print(msg)


#####
# Etat, but, et Constraint Satisfaction Problem (CSP) #
#  pour le sudoku.
###
# Permet de conserver l'ordre des résolutions de contraintes pour
# l'évaluation du devoir (ne pas utiliser!).
g_evaluation = []


class CSP:
    def __init__(self, variables, domaines, contraintes):
        self.variables = variables
        self.domaines = domaines
        self.contraintes = contraintes

    def arcs(self):
        return [(Xi, Xj) for Xi in self.contraintes
                for Xj in self.contraintes[Xi]]

    def copy(self):
        g_evaluation.append(self.domaines)
        return CSP(
            self.variables, copy.deepcopy(self.domaines), self.contraintes)

    def __eq__(self, autre):
        return all([v1 == v2
                    for v1, v2
                    in zip(self.variables, autre.variables)]) \
            and all([v1 == v2
                     for v in self.variables
                     for v1, v2 in zip(self.domaines[v], autre.domaines[v])]) \
            and all([c1 == c2
                     for v in self.variables
                     for c1, c2 in zip(
                         self.contraintes[v], autre.contraintes[v])])

    def __ne__(self, autre):
        return not self == autre


class SudokuEtat:
    def __init__(self, tableau=None):
        self.tableau = tableau
        if self.tableau is None:
            self.tableau = np.zeros([9, 9], dtype='S1')
            self.tableau[:] = ' '

    def find(self, case):
        """Trouve les coordonnées de la pièce désirée."""
        return np.array(np.where(self.tableau == case))

    def findNot(self, case):
        """Trouve les coordonnées des cases sauf celle de la pièce désirée."""
        return np.array(np.where(self.tableau != case))

    def placer(self, coordonnee, valeur):
        """Place une valeur dans la grille à la position donnée."""
        etat = SudokuEtat()
        etat.tableau = np.copy(self.tableau)
        etat.tableau[coordonnee] = valeur
        return etat

    def __eq__(self, other):
        return (self.tableau == other.tableau).all()

    def __ne__(self, other):
        return not self == other

    def __hash__(self):
        return hash("".join(self.tableau.flat))

    def __str__(self):
        t = """
  012 345 678

0 {0}{1}{2}|{3}{4}{5}|{6}{7}{8}
1 {9}{10}{11}|{12}{13}{14}|{15}{16}{17}
2 {18}{19}{20}|{21}{22}{23}|{24}{25}{26}
  ---+---+---
3 {27}{28}{29}|{30}{31}{32}|{33}{34}{35}
4 {36}{37}{38}|{39}{40}{41}|{42}{43}{44}
5 {45}{46}{47}|{48}{49}{50}|{51}{52}{53}
  ---+---+---
6 {54}{55}{56}|{57}{58}{59}|{60}{61}{62}
7 {63}{64}{65}|{66}{67}{68}|{69}{70}{71}
8 {72}{73}{74}|{75}{76}{77}|{78}{79}{80}
"""
        return \
            t.format(*self.tableau.flat).replace('b\'', '').replace('\'', '')


class SudokuUtil:
    @staticmethod
    def generate(seed):
        if seed is None:
            # Initialisation du Sudoku pour validation (Difficile).
            txt = "     4  7" + \
                  " 1       " + \
                  "796 3    " + \
                  "4    2   " + \
                  " 3  6  5 " + \
                  "   7    1" + \
                  "    5 932" + \
                  "       6 " + \
                  "2  8     "
        elif seed == 1:
            # Sudoku - Débutant
            txt = "  74  1  " + \
                  " 4 8   2 " + \
                  " 8  29 7 " + \
                  "  5    41" + \
                  "  2   6  " + \
                  "93    5  " + \
                  " 2 75  1 " + \
                  " 5   6 3 " + \
                  "  8  34  "
        elif seed == 2:
            # Sudoku - Moyen
            txt = "  53     " + \
                  "8      2 " + \
                  " 7  1 5  " + \
                  "4    53  " + \
                  " 1  7   6" + \
                  "  32   8 " + \
                  " 6 5    9" + \
                  "  4    3 " + \
                  "     97  "
        elif seed == 3:
            # Sudoku - Très difficile
            txt = "85   24  " + \
                  "72      9" + \
                  "  4      " + \
                  "   1 7  2" + \
                  "3 5   9  " + \
                  " 4       " + \
                  "    8  7 " + \
                  " 17      " + \
                  "    36 4 "
        else:
            # Sudoku - Très débutant
            txt = "3 1286 75" + \
                  "47 359 8 " + \
                  "86 174392" + \
                  "6 7823 1 " + \
                  "238 41567" + \
                  "9 47  238" + \
                  "7 349 156" + \
                  "1 65 7 49" + \
                  "54  18723"

        return SudokuEtat(SudokuUtil.convertir(str(txt)))

    @staticmethod
    def convertir(txt):
        return np.array(list(txt), dtype="S1").reshape(9, 9)

    @staticmethod
    def assignations2etat(assignations):
        etat = SudokuEtat()
        for pos, v in assignations.items():
            etat = etat.placer(pos, v)

        return etat


def tousUniques(sequence):
    sequence = sequence.flatten()
    for i, valeur in enumerate(sequence):
        if valeur in sequence[i+1:]:
            return False

    return True


def sudoku_but(etat):
    if etat.find(' ').shape[1] != 0:
        return False

    estTermine = True
    for i in range(9):
        estTermine &= tousUniques(etat.tableau[i, :])
        estTermine &= tousUniques(etat.tableau[:, i])
        subY, subX = i // 9, (i % 3) * 3
        estTermine &= tousUniques(etat.tableau[subY:subY+3, subX:subX+3])

    return estTermine


def sudoku_solution(etat, noPartie):
    if noPartie is None:
        # dbg()
        return "".join(map(str, etat.tableau.flatten())).replace("b'", '').replace("'", "") == "382514697514976823796238514451392786837461259629785341148657932975123468263849175" # noqa E501

    if noPartie == 1:
        return "".join(map(str, etat.tableau.flatten())).replace("b'", '').replace("'", "") == "297435168143867925586129374865392741712548693934671582329754816451986237678213459" # noqa E501

    if noPartie == 2:
        return "".join(map(str, etat.tableau.flatten())).replace("b'", '').replace("'", "") == "145327698839654127672918543496185372218473956753296481367542819984761235521839764" # noqa E501

    if noPartie == 3:
        return "".join(map(str, etat.tableau.flatten())).replace("b'", '').replace("'", "") == "859612437723854169164379528986147352375268914241593786432981675617425893598736241" # noqa E501

    return "".join(map(str, etat.tableau.flatten())).replace("b'", '').replace("'", "") == "391286475472359681865174392657823914238941567914765238783492156126537849549618723" # noqa E501


def creerCSP(etat):
    # Les variables représentent les cases vides
    variables = list(zip(*etat.find(b' ')))

    # Le domaine des cases libres est toutes les possibilités [1-9]
    domaines = {}
    for V in variables:
        domaines[V] = [bytes(str(i), 'utf-8') for i in range(1, 10)]

    # Pour les cases déjà remplies, le domaine est seulement la valeur
    # de la case
    for V in zip(*etat.findNot(b' ')):
        domaines[V] = [etat.tableau[V], ]
        variables.append(V)

    # Les contraintes sont ajoutées pour toutes les variables associées.
    contraintes = {}
    for V in variables:
        y, x = V
        contraintes[V] = []
        contraintes[V] += [(y, i) for i in range(9)]  # Contraintes de ligne
        contraintes[V] += [(i, x) for i in range(9)]  # Contraintes de colonne

        blocY, blocX = (y//3)*3, (x//3)*3
        contraintes[V] += [(blocY+i//3, blocX+i % 3)
                           for i in range(9)]  # Contraintes de bloc

        # Les contraintes doivent être uniques
        contraintes[V] = set(contraintes[V])
        contraintes[V].remove(V)  # Aucune contrainte avec soi-même

    return CSP(variables, domaines, contraintes)


def evaluation(no_partie, solution_file):
    etat_depart = SudokuUtil.generate(no_partie)

    nbCasesVides = len(etat_depart.find(b' ')[0])
    nbCoups = len(g_evaluation)
    nbBacktracks = nbCoups - nbCasesVides

    print("\n#########\n# Infos #\n#########")
    print("Nb. cases vides au départ: {0}".format(nbCasesVides))
    print("Nb. coups: {0}".format(nbCoups))

    if nbCoups == 0:
        print("* Attention, l'objet CSP doit être passé à AC3 par copie! " +
              " -> csp.copy() <-")
        return

    print("Nb. backtracks: {0}".format(nbBacktracks))

    assignations = dict([(k, v[0]) for k, v in g_evaluation[-1].items()])
    solutionTrouve = SudokuUtil.assignations2etat(assignations)

    if not sudoku_but(solutionTrouve):
        print("* La solution trouvée n'est pas valide!")
        print(solutionTrouve)

    if not sudoku_solution(solutionTrouve, no_partie):
        print("* La solution trouvée n'est pas la bonne!")
        print("-> Assurez vous de sélectionner les variables dans " +
              "`csp.variables` ")
        print(
            "   et les valeurs de domaine dans `csp.domaines[X]` selon l'ordre ")
        print("   dans lequel ils apparaissent. <-")

    if no_partie is None:
        print("\n##############\n# Validation #\n##############")
        import pickle
        sol_nbCoups, sol_nbBacktracks = pickle.load(open(solution_file, 'rb'))

        print("Nb. coups: {0} (vous) vs. {1} (solution)".format(
            nbCoups, sol_nbCoups))
        if sol_nbCoups < nbCoups:
            print(
                ("* Votre nombre d'essais ({0}) peut être amélioré " +
                 "(Objectif: {1})!").format(nbCoups, sol_nbCoups))
            return

        print("Nb. backtracks: {0} (vous) vs. {1} (solution)".format(
            nbBacktracks, sol_nbBacktracks))
        if sol_nbBacktracks < nbBacktracks:
            print(("* Votre nombre de backtracks ({0}) peut être réduit " +
                   " (Objectif: {1})!").format(
                nbBacktracks, sol_nbBacktracks))
            return

        if not sudoku_but(solutionTrouve):
            return

        # print "Bravo, vous n'avez pas d'erreur."
    else:
        print("Pour valider le nombre de coups et de backtracks, " +
              "n'utilisez pas l'option `-no_partie`.")


#####
# Execution en tant que script
###
def player_factory(player):
    if player == 'humain':
        return joueur_humain

    if player.endswith('.py'):
        player = os.path.abspath(player)
        name = player.replace('/', '.').replace('.', '_')

        solution = SourceFileLoader(name, player).load_module(name)

        # Coquille simulant un joueur à partir des assignations retournées
        # par backtracking_search
        def joueurAgent(
            etat_depart, fct_estEtatFinal,
            fct_transitions, fct_heuristique
        ):
            assignations = solution.backtracking_search(creerCSP(etat_depart))

            # Générateur d'états à partir des assignations
            def iterEtats():
                etat = etat_depart
                yield etat
                for pos, v in assignations.items():
                    etat = etat.placer(pos, v)
                    yield etat

            return iterEtats()

        return joueurAgent

    return None


DESCRIPTION = "Lancer une partie de sudoku."


def buildArgsParser():
    p = argparse.ArgumentParser(description=DESCRIPTION,
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    # Paramètres globaux
    p.add_argument('-joueur', dest="player", metavar="JOUEUR", action='store',
                   type=str, required=False, default="solution_sudoku.py",
                   help="'humain' ou le fichier contenant votre solution.")

    p.add_argument('-no_partie', dest="no_partie", metavar="INT",
                   action='store', type=int, required=False,
                   help="numéro de partie à jouer [0-3].", choices=[0, 1, 2, 3])

    p.add_argument('-valider', dest="validation_file", metavar="FICHIER",
                   action='store', type=str, required=False, default='sudoku_validation.pkl',
                   help="fichier permettant de valider votre joueur pour un jeu donné.")

    p.add_argument('-v', dest='verbose', action='store_true', required=False,
                   help='activer le mode verbose')

    return p


#####
# Execution en tant que script
###
def main():
    parser = buildArgsParser()
    args = parser.parse_args()
    player = args.player
    no_partie = args.no_partie
    validation_file = args.validation_file
    verbose = args.verbose

    if player == "humain":
        verbose = True  # Afficher les grilles si c'est un joueur humain.

    if player not in ['aleatoire', 'humain'] and not player.endswith('.py'):
        parser.error('Joueur doit être [humain, solution_sudoku.py]')

    if no_partie is None and not os.path.isfile(validation_file):
        parser.error("Fichier introuvable: '{0}'".format(validation_file))

    # Obtenir l'état de départ à partir du numéro de partie
    etat_depart = SudokuUtil.generate(no_partie)

    # Jouer une partie de sudoku
    sudoku = Jeu(etat_depart, sudoku_but, None, None, verbose=verbose)

    start_time = time.time()
    sudoku.jouer_partie(player_factory(player))
    print("Temps écoulé: %0.2f sec." % (time.time()-start_time))

    evaluation(no_partie, validation_file)


if __name__ == "__main__":
    main()
