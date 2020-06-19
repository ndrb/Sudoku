# -*- coding: utf-8 -*-

#####
# Nader Baydoun (20156885)
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np

#####
# reviser: Fonction utilisée par AC3 afin de réduire le domaine de Xi en fonction des contraintes de Xj.
#
# Xi: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# Xj: Variable (tuple (Y,X)) dont ses domaines seront réduit, si possible.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant un booléen indiquant si il y a eu des changements et le csp.
###
def reviser(Xi, Xj, csp):
    change = False
    for x in csp.domaines:
        if csp.contraintes[x] is not None:  # Might need to change it to a negation
            csp.domaines.remove(x)
            change = True
    return change, csp


#####
# AC3: Fonction s'occupant de réduire les domaines des variables selon l'algorithme AC3.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un tuple contenant le csp optimisé et un booléen indiquant si aucune contrainte n'est violée.
###
def AC3(csp):
    file_arcs = csp.arcs()
    while (file_arcs):
        (xi, xj) = file_arcs.pop(0)
        change, csp = reviser(xi,xj,csp)
        if change:
            if not csp.domaines:
                return None, False
            for xk in file_arcs: # it should be xk in voisins
                if xk != xj:
                    file_arcs.append(xk,xj)
    return csp, True


#####
# est_compatible: Fonction vérifiant la légalité d'une affectation.
#
# X: Tuple contenant la position en y et en x de la case concernée par l'affectation.
#
# v: String représentant la valeur (entre [1-9]) concernée par l'affectation.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Un booléean indiquant si l'affectation de la valeur v à la case X est légale.
###
def est_compatible(X, v, assignations, csp):
    # TODO: .~= À COMPLÉTER =~.
    count = 0

    # for each of the cells that can be in conflict with cell
    #for related_c in sudoku.related_cells[cell]:

        # if the value of related_c is not found yet AND the value we look for exists in its possibilities
        #if len(sudoku.possibilities[related_c]) > 1 and value in sudoku.possibilities[related_c]:
            # then a conflict exists
            #count += 1

    #return count
    return True


#####
# backtrack : Fonction s'occupant de trouver les assignations manquantes de la grille de Sudoku
#             en utilisant l'algorithme de Backtracking Search.
#
# assignations: dict mappant les cases (tuple (Y,X)) vides à une valeur.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku.
#      Pour plus d'information, voir doc de la fonction 'backtracking_search'.
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtrack(assignations, csp):
    # TODO: .~= À COMPLÉTER =~.

    return assignations


#####
# backtracking_search : Fonction coquille pour la fonction 'backtrack'.
#
# csp: Objet de la classe CSP contenant tous les informations relative aux problème
#      de satisfaction de contraintes pour une grille de Sudoku. Les variables membres sont
#      'variables'   : list de cases (tuple (Y,X)) vides
#      'domaines'    : dict mappant une case à une liste des valeurs possibles
#      'contraintes' : dict mappant une case à une liste de cases dont leur valeur doivent être différentes
#
# retour: Le dictionnaire des assignations (case => valeur)
###
def backtracking_search(csp):
    return backtrack({}, csp)