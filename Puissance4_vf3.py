# -*- coding: utf-8 -*-
"""
Created on Sat May  2 18:19:47 2020

@author: cheic
"""
import time 
import numpy as np 
import pygame
import sys
import math
import random 
BLEU = (0,0,255)
NOIR = (0,0,0)
ROUGE = (255,0,0)
JAUNE = (255,255,0)
NOMBRES_LIGNES= 6
NOMBRES_COLONNES=12
PIECE_JOUEUR=1
PIECE_IA=2
LONGUEUR_FENETRE=4
JOUEUR = 0
IA= 1
EMPTY=0

# Création d'une grille de zeros de taille nombres_lignes , nombrees_colonnes
def Creation_Grille():
    grille= np.zeros((NOMBRES_LIGNES,NOMBRES_COLONNES))
    return grille
#Placer une pièce dans la grille
def tomber_une_piece(grille,ligne,colonne,piece):
    grille[ligne][colonne]= piece
#Vérifier si une colonne n'est pas remplie    
def position_valide(grille,colonne):
    return grille[NOMBRES_LIGNES-1][colonne]==0
#Vérification de la prochaine ligne libre dans une colonne donnée
def prochaine_ligne_libre(grille,colonne):
    for l in range(NOMBRES_LIGNES):
        if grille[l][colonne]==0:
            return l
#Fliper la grille de telle sorte à ce qu'on est pas à décrementer les indices dans le parcours de la grille
def retourner_grille(grille):
    print(np.flip(grille,0))

# Retourne un booléen pour savoir s'il y a un jeu gagné 
def jeu_gagnant(grille,piece):
    # Vérification des positions horizontales gagnantes
    for c in range(NOMBRES_COLONNES-3):
        for l in range(NOMBRES_LIGNES):
            if grille[l][c] == piece and grille[l][c+1]== piece and grille[l][c+2]==piece and grille[l][c+3]==piece:
                return True
    # Vérification des positions verticales gagnantes
    for c in range(NOMBRES_COLONNES):
        for l in range(NOMBRES_LIGNES-3):
            if grille[l][c] == piece and grille[l+1][c] == piece and grille[l+2][c]== piece and grille[l+3][c]==piece:
                return True
    # Vérification des positions diagonales positives gagnantes
    for c in range(NOMBRES_COLONNES-3):
        for l in range(NOMBRES_LIGNES-3):
            if grille[l][c] == piece and grille[l+1][c+1] == piece and grille[l+2][c+2]== piece and grille[l+3][c+3]==piece:
                return True
    # Vérification des positions diagonales négatives gagnantes
    for c in range(NOMBRES_COLONNES-3):
        for l in range(3,NOMBRES_LIGNES):
            if grille[l][c] == piece and grille[l-1][c+1] == piece and grille[l-2][c+2]== piece and grille[l-3][c+3]==piece:
                return True
#Affectation du scoring suivant les cas de jeux
def fenetre_score(fenetre,piece):
    score=0
    adversaire_piece= PIECE_JOUEUR
    if piece== PIECE_JOUEUR:
        adversaire_piece=PIECE_IA
        
    if fenetre.count(piece)==4:
        score+=100
    elif fenetre.count(piece)==3 and fenetre.count(EMPTY)==1:
        score+=5
    elif fenetre.count(piece)==2 and fenetre.count(EMPTY)==2:
        score+=2
    
    if fenetre.count(adversaire_piece)==3 and fenetre.count(EMPTY)==1:
        score-=4
    if fenetre.count(adversaire_piece)==2 and fenetre.count(EMPTY)==2:
        score-=1.5
    return score
    
        
    
#Scoring suivant les positions
def position_score(grille,piece):
    score=0
    
    #Score colonne centrale
    tableau_centre=[int(i) for i in list(grille[:,NOMBRES_COLONNES//2])]
    nombre_centre= tableau_centre.count(piece) 
    score+=nombre_centre*3
    
    
    #Score horizontal
    
    for l in range(NOMBRES_LIGNES):
        tableau_ligne=[int(i) for i in list(grille[l,:])]
        for c in range(NOMBRES_COLONNES-3):
            fenetre= tableau_ligne[c:c+LONGUEUR_FENETRE]
            score+=fenetre_score(fenetre,piece)
    #Score vertical
    for c in range(NOMBRES_COLONNES):
        tableau_colonne=[int(i)for i in list(grille[:,c])]
        for l in range(NOMBRES_LIGNES-3):
            fenetre=tableau_colonne[l:l+LONGUEUR_FENETRE]
            score+=fenetre_score(fenetre,piece)
    #Score diagonale positive
    for l in range(NOMBRES_LIGNES-3):
        for c in range(NOMBRES_COLONNES-3):
            fenetre=[grille[l+i][c+i] for i in range(LONGUEUR_FENETRE)]
            score+=fenetre_score(fenetre,piece)
    #Score diagonale negative
    for l in range(NOMBRES_LIGNES-3):
        for c in range(NOMBRES_COLONNES-3):
            fenetre=[grille[l+3-i][c+i]for i in range(LONGUEUR_FENETRE)]
            score+=fenetre_score(fenetre,piece)
    return score
# Booléen qui retourne s'il y a fin du jeu 
def fin_du_jeu(grille):
    return jeu_gagnant(grille,PIECE_JOUEUR) or jeu_gagnant(grille,PIECE_IA) or len(liste_positions_valides(grille))==0
#Mise en place du minimax            
def minimax(grille, profondeur,alpha,beta,maximizingPlayer):
    position_valide=liste_positions_valides(grille)
    findujeu=fin_du_jeu(grille)
    if profondeur==0 or findujeu:
        if findujeu:
            if jeu_gagnant(grille,PIECE_IA):
                return (None,10000000000)
            elif jeu_gagnant(grille,PIECE_JOUEUR):
                return (None,-10000000000)
            else: #Fin du jeu, on ne peut plus faire tomber de pion
                return (None,0)
        else: # Profondeur vaut 0 
            return (None,position_score(grille,PIECE_IA))
    if maximizingPlayer:
        value= -math.inf
        colonne= random.choice(position_valide)
        for c in position_valide:
            ligne= prochaine_ligne_libre(grille,c)
            tempogrille= grille.copy()
            tomber_une_piece(tempogrille,ligne,c,PIECE_IA)
            new_score=minimax(tempogrille,profondeur-1,alpha,beta,False)[1]
            if new_score>value:
                value=new_score
                colonne= c
            alpha=max(alpha,value)
            if alpha>=beta:
                break
        return colonne,value
               
    else: #minimizing player 
        value= math.inf
        colonne= random.choice(position_valide)
        for c in position_valide:
            ligne= prochaine_ligne_libre(grille,c)
            tempogrille= grille.copy()
            tomber_une_piece(tempogrille,ligne,c,PIECE_JOUEUR)
            new_score=minimax(tempogrille,profondeur-1,alpha,beta,True)[1]
            if new_score<value:
                value=new_score
                colonne=c
            beta= min(beta,value)
            if alpha>=beta:
                    break
        return colonne,value
        
                   
#Retourne l'ensemble des positions colonnes dans lesquelles on peut jouer               
def liste_positions_valides(grille):
    positions_valides=[]
    for c in range(NOMBRES_COLONNES):
        if position_valide(grille,c):
            positions_valides.append(c)
    return positions_valides
# Semblant de minimax
def choisir_meilleur_mouv(grille,piece):
    positions_valides= liste_positions_valides(grille)
    best_score=-10000
    best_colonne= random.choice(positions_valides)
    for c in positions_valides:
        ligne=prochaine_ligne_libre(grille,c)
        tempogrille=grille.copy()
        tomber_une_piece(tempogrille,ligne,c,piece)
        score= position_score(tempogrille,piece)
        if score>best_score:
            best_score=score
            best_colonne=c
    return best_colonne
    
    
#Modélisation de la grille avec pygame    
def modelisation_grille(grille):
    for c in range(NOMBRES_COLONNES):
        for l in range(NOMBRES_LIGNES):
            pygame.draw.rect(screen,BLEU,(c*TAILLECERCLE,l*TAILLECERCLE + TAILLECERCLE,TAILLECERCLE,TAILLECERCLE ))
            pygame.draw.circle(screen,NOIR,(int(c*TAILLECERCLE + TAILLECERCLE/2),int(l*TAILLECERCLE + TAILLECERCLE+ TAILLECERCLE/2)),RAYON)
    for c in range(NOMBRES_COLONNES):
        for l in range(NOMBRES_LIGNES):
            if grille[l][c]==PIECE_JOUEUR:
                pygame.draw.circle(screen,JAUNE,(int(c*TAILLECERCLE + TAILLECERCLE/2),longueur-int(l*TAILLECERCLE + TAILLECERCLE/2)),RAYON)
            elif grille[l][c]==PIECE_IA:
                pygame.draw.circle(screen,ROUGE,(int(c*TAILLECERCLE + TAILLECERCLE/2),longueur-int(l*TAILLECERCLE+ TAILLECERCLE/2)),RAYON)
    pygame.display.update()           
grille= Creation_Grille()
retourner_grille(grille)
game_over= False


pygame.init()
TAILLECERCLE= 100

largeur= NOMBRES_COLONNES*TAILLECERCLE
longueur= (NOMBRES_LIGNES+1)*TAILLECERCLE

size= (largeur,longueur)

RAYON = int(TAILLECERCLE/2 -5)
screen= pygame.display.set_mode(size)
modelisation_grille(grille)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 75)
#tour= random.randint(JOUEUR, IA)
tour=1
while not game_over: 
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, NOIR,(0,0,largeur,TAILLECERCLE))
            coordonneesx= event.pos[0]
            if tour==JOUEUR:
                pygame.draw.circle(screen,JAUNE,(coordonneesx,int(TAILLECERCLE/2)),RAYON)
            
        pygame.display.update()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, NOIR, (0,0, largeur, TAILLECERCLE))
            
            
           
            # On attend une entrée du joueur 1
            if tour==JOUEUR:
                coordonnees_x= event.pos[0]
                colonne= int(math.floor(coordonnees_x/TAILLECERCLE))   
                
                
                if position_valide(grille,colonne):
                    ligne=prochaine_ligne_libre(grille,colonne)
                    tomber_une_piece(grille,ligne,colonne,PIECE_JOUEUR)
                    
                    if jeu_gagnant(grille,PIECE_JOUEUR):
                        victoire= myfont.render("Victoire du Joueur 1",1,JAUNE)
                        screen.blit(victoire, (40,10))
                        game_over= True
                    tour+=1
                    tour=tour % 2
                    retourner_grille(grille)
                    modelisation_grille(grille)
                    
    # On attend une entrée du joueur 2
    if tour== IA and not game_over :
        #colonne= random.randint(0,NOMBRES_COLONNES-1)
        #colonne= choisir_meilleur_mouv(grille,PIECE_IA)
        t=time.time()
        colonne,minimax_score= minimax(grille,4,-math.inf,math.inf,True)
        position=(colonne)
        print(round(time.time()-t,3),"colonne:" + str(colonne+1))
        #pygame.time.wait(500)
        
        if position_valide(grille,colonne):
            ligne=prochaine_ligne_libre(grille,colonne)
            tomber_une_piece(grille,ligne,colonne,PIECE_IA)
            
            if jeu_gagnant(grille,PIECE_IA):
                victoire= myfont.render("Victoire du Joueur 2",1,ROUGE)
                screen.blit(victoire, (40,10))
                game_over=True
            retourner_grille(grille)
            modelisation_grille(grille)
            
            tour+=1
            tour=tour % 2
    if game_over:
        pygame.time.wait(3000)
                
               