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
    peptide_dico= read_fasta(peptide_file)
    prot_dico = read_fasta(prot_file)
    the_dico = {}
    for peptide in peptide_dico : 
        match = match_id(peptide_dico[peptide],prot_file) #retourne une liste de prot
        for i in range(len(match)): 
            
            
            for y ,z  in prot_dico.items(): #WARNING 
                if z == match[i] :
                    key = y 
             ### /!\ Inverser le dico pour avoir l'ID de la prot en clé ###
            
            if match[i] in dict.keys(the_dico):
                the_list = the_dico[match[i]]
                the_list.append(peptide_dico[peptide])
                the_dico[match[i]]=the_list
            else:
                the_list = []
                the_list.append(peptide_dico[peptide])
                the_dico[match[i]]=the_list
    return the_dico
            
a = unique_match_set('test_pep.fasta', 'test_prot.fasta')
