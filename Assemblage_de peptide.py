#OBI Project, Overlap function
from os import chdir
chdir("C:\\Users\\Lucien\\Desktop\\test_data")
#Peptides de test 
pep1 = "HELLOHELLOCHIEN"
pep2 = "ZEBIHELLOHELLO"
pep3 = "HELLOBG"
pep4 = "BONJOURHELLO"
pep5 = "HELLOBONJOUR"
adn = "ATCGGCTA"


def overlap(first_peptide, second_peptide): 
    #Fonction Overlap
    count_forward = count_back = 0  
    # Initialise deux conteurs pour chaque coté des peptides
    
    for i in range(len(first_peptide)): 
    #Boucle de la longeur des peptides (les peptides peuvent avoir des tailles différentes)
    
        if first_peptide[-i:] == second_peptide[:i]: 
        #Test si les des extrémités de taille i sont identiques dans un sens
            
            count_forward = i 
            #Si oui, saugearde la valeure de i 
            
        if second_peptide[-i:] == first_peptide[:i]: 
            count_back = i   
            #Identique mais pour les autres extrémités 
    
    #Compare la valeur des deux compteurs et retourne la plus haute 
    if first_peptide == second_peptide:
        return len(first_peptide)
    if count_forward > count_back :
        return count_forward
    else :
        return count_back
    
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

def match_id(peptide,prot_file):
    prot_dico=read_fasta(prot_file)
    list_match = []
    for prot in prot_dico:
        n=count_word(prot_dico[prot],peptide)
        if n > 0 :
            list_match.append(prot_dico[prot])
    if list_match == [] :
        list_match.append('None')
    return list_match

def write_fasta(seq_dico,filename):
    #Fonction pour écrire un fichier fasta a partir d'un dictionnaire
    
    #On commence par créer le fichier a modifier
    new_file = open(filename, 'w')
    
    #On parce ce dictionnaire 
    for key in seq_dico :
        #On écrit la clée correspondant a l'ID sur une ligne
        new_file.write((">"+key+'\n'))
        
        #On ecrit la séuence sur une autre linge
        #On ajoute \n tous les 60 lettres pour avoir un fichier lisible (falcutatif) et a la fin
        new_file.write(('\n'.join(seq_dico[key][i:i+60] for i in range(0, len(seq_dico[key]), 60)))+'\n')
   
def stack_peptide(first_peptide,second_peptide,overlap):
    #Stack peptides based on the best overlap between them
    
    #Retrun none if there is no overlap
    if overlap == 0 :
        return 
    
    #Check for the side of the overlap
    if first_peptide[-overlap:] == second_peptide[:overlap]:
        stacked_peptide = first_peptide[:-overlap]+second_peptide
    else :
        stacked_peptide = second_peptide[:-overlap]+first_peptide
        
    #Retrun a stacked peptide 
    return stacked_peptide
        
def best_overlap(sequence, seq_dico):
    #Function that check for the best overlap between a sequence and sequences in a dico
    #Return the key of the best outcome
    #In case of a tie, retrun the first encountered 
    
    best_overlap = 0 
    #Set the counter as 0

    for sequences in seq_dico :
        #Parce the whole dico 
        
        #Check for the overlap
        new_overlap = overlap(seq_dico[sequences],sequence)
        
        #Save the best overlap
        if new_overlap > best_overlap :
            best_overlap = new_overlap
            best_sequence = sequences
            
    #If there is no overlap, return none 
    if best_overlap == 0 :
        return
    
    #Else, return the sequence ID
    else : 
        return best_sequence
        
       

def assembely_peptide(pep_file, overlap_min):
    #Fonction d'assemblage des peptides 
    
    #On crée un nouveau dictionnaire vide pour placer nos peptides
    stacked_dico = {}
    num_name = 1
    
    #Ouverture du fichier et transformation en dictionnaire
    peptide_dico = read_fasta(pep_file)
    
    
    #On parcours le dico entier pour faire des assemblages avec chaque peptides 
    for peptide_ref in peptide_dico:

        #On ouvre un nouveau dictionnaire afin de servir de banque de peptides
        #Cela permet de ne pas avoir de doublons
        peptide_dico_bank = read_fasta(pep_file)        


        #On crée la base de notre assemblage 
        stacked = peptide_dico_bank.pop(peptide_ref)
        
        is_stacked = False
        
        
        ## DEBUT DE L'ASSEMBLAGE
        
        #On ouvre une boucle qui vas additioner les peptides tant que l'overlap est suffisant
        while True :
            
            #On évite les erreures de dictionnaires vides en fin de boucle
            if len(peptide_dico_bank) == 0:
                break
            
            #On trouve le meilleur peptide dans le dico 
            peptide_candidat = best_overlap(stacked,peptide_dico_bank)
            
            #On évite les erreures en manque de candidat
            if peptide_candidat == None :
                break
            
            #On mesure l'overlap actuel 
            curent_overlap = overlap(stacked,peptide_dico_bank[peptide_candidat])
            
            #On test si l'overlap est suffisant pour continuer
            if curent_overlap >= overlap_min:
                is_stacked = True
                
                #Si oui, on additione le peptide candidat a notre super peptide
                stacked = stack_peptide(stacked, peptide_dico_bank[peptide_candidat], curent_overlap)
                
                #On oublie pas d'enlever le peptide de notre liste de peptides potentiels
                peptide_dico_bank.pop(peptide_candidat)
                
            #Si on a pas d'overlap suffisant, on termine l'assemblage    
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


print(assembely_peptide('test_peptide.fa',1))


    
    
    

 