# -*- coding: utf-8 -*-

#####
# Nader Baydoun (20156885)
###

from pdb import set_trace as dbg  # Utiliser dbg() pour faire un break dans votre code.

import numpy as np
import random
import sudoku

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
    choice = random.randrange(0,1)
    if choice is 0:
        return False
    else:
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
    if not csp.variables:
        return assignations
    x = csp.variables
    for v in x:
        if est_compatible(x,v,assignations,csp):
            assignations[x] = v
            cspCopy = csp.copy()
            cspCopy = v
            cspCopy, ok = inference(x, csp)
            if ok:
                result = backtrack(assignations, cspCopy)
                if result is not False:
                    return result
            assignations.pop(x)
    return False

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
    final_result = backtrack({}, csp)
    return final_result

def inference(x,csp):
    for xk in csp.arcs():
        change,csp = reviser(xk, x, csp)
        if change and not csp.domaines:
            return None, False
        return csp, True