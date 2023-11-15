#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def read_fasta(filename):
    """ Fonction qui prend en entré un fichier eet renvoie un dicotionnaire, 
    avec en clef l'identifiant et en valeur la sequence d'acide amine """
    dico ={}
    content=""
    id=""
    seq = open(filename, "r")
    for i in seq.readlines():
        if i[0]==">" : 
            if id!="":
                dico[id]=content
            id = i.strip('\n') #enleve les retour a la ligne de la clef du dictionnaire.
            id = id.strip('>') #enleve les cheverons a la ligne de la clef du dictionnaire.
            content = ""  #reinitialise la chaine.
        else : 
            content=content+i.strip('\n') #incremente la chaine a chaque retour de ligne.
    dico[id]=content
    return dico

seq = read_fasta('test_prep.fa')
print(seq)
seq = read_fasta('test_prot.fa')
print(seq)










