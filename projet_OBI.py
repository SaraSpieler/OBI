
#read_fasta (fasta_file)
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

def count_word(seq,word):
    word_count=0
    for i in range(len(seq)):
        if seq[i] == word[0]:
            if seq[i:(i+len(word))] == word:
                      word_count+=1
    return word_count 
    
#match_id(r,fasta_file)
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
    
#unique_match_set(peptide_file, db_file)
def unique_match_set(peptide_file, prot_file):
    key="None"
    peptide_dico= read_fasta(peptide_file)
    #print("Dictionnaire read fasta => Peptide : ",peptide_dico)
    prot_dico = read_fasta(prot_file)
    #print("Dictionnaire read fasta => Proteine : ",prot_dico)
    the_dico = {}
    for peptide in peptide_dico : 
        match = match_id(peptide_dico[peptide],prot_file) 
        #retourne pour chaque peptide une liste avec toute les proteines ou ce trouve le peptides
        '''donc pour etre sure que 1 peptides soit associer a une seul proteine, 
        il suffit de regarder la longeur de la liste,
        si elle a plus d'un element alors il ne faut pas la prendre en compte'''
        #print("Liste match_id : \nPeptides : ", peptide, "\n", match)
        
        for i in range(len(match)): 
            """ ici on vas creer un dictionnaire :
                clef = Id proteine 
                valeur = une/plusieur sequence peptidiques """
            if len(match) == 1:
                for y ,z  in prot_dico.items(): 
                    ''' recupere l'Id de la proteine '''
                    if z == match[i] :
                        key = y
        
                if key in the_dico.keys():
                    ''' Si l'Id de la proteine est dans le dictionnaire 
                    alors on ajoute le peptides a la suite dans la liste deja créer '''
                    the_list = the_dico[key]
                    the_list.append(peptide_dico[peptide])
                    the_dico[key]=the_list
                    key="None"

                else:
                    ''' Sinon, 
                    on cree une liste, dans laquel on met la/les sequence(s) peptidique(s)
                    ensuite on l'ajoute ensuite dans le dictionnaire, qui a comme clef l'Id de la proteine '''
                    the_list = []
                    the_list.append(peptide_dico[peptide])
                    the_dico[key]=the_list
                    key="None"

            else : 
                None

    #ENLEVE NONE
    #grace a la une compréhension de dictionnaire, on vas pouvoir enlever les None 
    #comme si tu cree un nouveau the_dico mais sans None
    print("Avant supressions None : \n", the_dico)
    the_dico = {k: v for k, v in the_dico.items() if k != 'None'}

    print("Avant supressions proteine avec moins de deux peptides : \n", the_dico)
    ##ENLEVE PROT AVEC MOINS DE 2 PEPTIDES 
    #pareil grace a la comprehension de dictionnaire.
    the_dico = {k: v for k, v in the_dico.items() if len(v) >= 2}
    
    return the_dico #return le dico trier a la fin
                    
##    Fonctions d'overlap    ###

#overlap(r1, r2)
def overlap(first_peptide,second_peptide):
    #On initialise a 0 
    count = 0
    
    #On compare les extrémitées pour en incrémentant la longeure de 1 
    for i in range(len(first_peptide)):

        #Si les extrémitées sont égale, on sauvegarde l'indice
        if first_peptide[-i:] == second_peptide[:i]: 
            count = i 
    return count
#best_overlap(sequence, seq_dico)
def best_overlap(sequence, seq_dico):
    #La fonction retourne la clé de la séquence qui overlap le mieux
    best_overlap = 0 
    for sequences in seq_dico :
        
        #Pour chaque éléments, on regarde l'overlap
        new_overlap = overlap(seq_dico[sequences],sequence)
        new_overlap_other_side = overlap(sequence,seq_dico[sequences])
        if new_overlap_other_side > new_overlap:
            new_overlap = new_overlap_other_side
        
        #On sauvegarde l'overlap dans les deux sens
        if new_overlap > best_overlap :
            best_overlap = new_overlap
            best_sequence = sequences
            
    if best_overlap == 0 :
        return
    else : 
        return best_sequence

#stack_peptide(first peptide, second peptide, overlap)
def stack_peptide(first_peptide, second_peptide, overlap):
    #Additione les peptides en fonction de l'overlap

    if overlap == 0 :
        return 
    
    #On test le coté de l'overlap et on additione 
    if first_peptide[-overlap:] == second_peptide[:overlap]:
        stacked_peptide = first_peptide[:-overlap]+second_peptide
    else :
        stacked_peptide = second_peptide[:-overlap]+first_peptide
    
    return stacked_peptide

#write_fasta(seq_dico,filename)
def write_fasta(seq_dico,filename):
    #Fonction pour écrire un fichier fasta a partir d'un dictionnaire
    
    #On commence par créer le fichier a modifier
    new_file = open(filename, 'w')
    
    #On parce ce dictionnaire 
    for key in seq_dico :
        #On écrit la clée correspondant a l'ID sur une ligne
        new_file.write((">"+key+'\n'))
        
        #On ecrit la séquence sur une autre linge
        #On ajoute \n tous les 60 lettres pour avoir un fichier lisible (falcutatif) et a la fin
        new_file.write(('\n'.join(seq_dico[key][i:i+60] for i in range(0, len(seq_dico[key]), 60)))+'\n')
    
#assembly_peptides(peptide_file, overlap_min)
def assembely_peptide(pep_file, overlap_min):
    #Fonction d'assemblage des peptides 
    
    stacked_dico = {}
    num_name = 1
    
    #Ouverture du fichier et transformation en dictionnaire
    peptide_dico = read_fasta(pep_file)
    
    #On parcours le dico entier pour faire des assemblages avec chaque peptides 
    for peptide_ref in peptide_dico:

        #On ouvre un nouveau dictionnaire afin de servir de banque de peptides. Cela permet de ne pas avoir de doublons.
        peptide_dico_bank = read_fasta(pep_file)        

        #On crée la base de notre assemblage 
        stacked = peptide_dico_bank.pop(peptide_ref)
        
        is_stacked = False
        
        
        # DEBUT DE L'ASSEMBLAGE
        #On ouvre une boucle qui vas additioner les peptides tant que l'overlap est suffisant
        while True :
            
            if len(peptide_dico_bank) == 0:
                break
            
            #On trouve le meilleur peptide dans le dico 
            peptide_candidat = best_overlap(stacked,peptide_dico_bank)
            if peptide_candidat == None :
                break
            
            #On mesure l'overlap actuel 
            curent_overlap = overlap(stacked,peptide_dico_bank[peptide_candidat])
            curent_overlap_other_side = overlap(peptide_dico_bank[peptide_candidat],stacked)
            if curent_overlap_other_side > curent_overlap :
                curent_overlap = curent_overlap_other_side
            
            #On test si l'overlap est suffisant pour continuer
            if curent_overlap >= overlap_min:
                is_stacked = True
                
                #Si oui, on additione le peptide candidat a notre super peptide
                stacked = stack_peptide(stacked, peptide_dico_bank[peptide_candidat], curent_overlap)
                
                #On oublie pas d'enlever le peptide de notre liste de peptides potentiels
                peptide_dico_bank.pop(peptide_candidat)
                
            else :
                break 
                
        ##EXTRACTION DES ASSEMBLAGES
         
        #On regarde si on a obetnu un assemblage
        if is_stacked:
    
            #Si oui, on vérifie que le peptide n'est pas déja représenté
            if stacked not in dict.values(stacked_dico):
                stacked_dico['PEpNew0'+str(num_name)]=stacked
                
                #Cette variable permet de générer des noms pour les peptides
                num_name+=1 
                
   #Ici, on recommence la boucle avec un nouveau peptide        
        
    #Finalement on écrit le dictionnaire dans un fichier            
    write_fasta(stacked_dico, 'stacked_pep.fasta')           
    return stacked_dico

#assembely_peptide('test_peptide.fa',1)
#unique_match_set('test_peptide.fa','test_prot.fa')

