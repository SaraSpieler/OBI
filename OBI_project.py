#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def read_fasta(filename):
    dico ={}
    content=""
    id=""
    seq = open(filename, "r")
    for i in seq.readlines():
        if i[0]==">" : 
            if id!="":
                dico[id]=content
            id = i.strip("\n")
            id = id.strip(">")
            
            content = ""  
        else : 
            content=content+i.strip('\n')
    dico[id]=content
    return dico


seq_pep = read_fasta('test_pep.fasta')
seq_prot = read_fasta('test_prot.fasta')

def count_word(seq,word):
    word_count=0
    for i in range(len(seq)):
        if seq[i] == word[0]:
            if seq[i:(i+len(word))] == word:
                      word_count+=1
                      
    
    return word_count 

def match_id(peptide,prot_file):
    match_dico = {}
    prot_dico=read_fasta(prot_file)
    list_match = []
    for prot in prot_dico:
        n=count_word(prot_dico[prot],peptide)
        if n > 0 :
            list_match.append(prot_dico[prot])
    if list_match == [] :
        list_match.append('None')
    return list_match

def unique_match_set(peptide_file, prot_file):
    key="None"
    peptide_dico= read_fasta(peptide_file)
    prot_dico = read_fasta(prot_file)
    the_dico = {}
    for peptide in peptide_dico : 
        match = match_id(peptide_dico[peptide],prot_file) #retourne une liste de prot
        for i in range(len(match)): 
            
            for y ,z  in prot_dico.items(): 
                if z == match[i] :
                    key = y 
      
            if key in dict.keys(the_dico):
                the_list = the_dico[key]
                the_list.append(peptide_dico[peptide])
                the_dico[key]=the_list
                key="None"
            else:
                the_list = []
                the_list.append(peptide_dico[peptide])
                the_dico[key]=the_list
                key="None"
    
    ### Return for at least 2 pep
    
        ##Enlever les none 
        ##Enlever les peptides plusieurs fois représentés 
            #Chercher le peptide 
            #On count le peptide et on check si il est présent
            #Le supprimer de TOUTES les protéines en meme temps
           
        ##Enlever les prot avec moins de deux pep
    
                    
                
    return the_dico #return le dico trier a la fin
            
            
a = unique_match_set('test_pep.fasta', 'test_prot.fasta')
