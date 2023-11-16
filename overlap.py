#OBI Project, Overlap function


#Peptides de test 
pep1 = "HELLOHELLOCHIEN"
pep2 = "ZEBIHELLOHELLO"
pep3 = "HELLOBG"
pep4 = "BONJOURHELLO"
pep5 = "HELLOBONJOUR"
adn = 'ATCGGCTA'

#Fonction Overlap
def overlap(first_peptide, second_peptide): 
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
    
    if count_forward > count_back :
        return count_forward
    else :
        return count_back
    #Compare la valeur des deux compteurs et retourne la plus haute 
    
    
print(overlap(pep1, pep2))
print(overlap(pep2, pep3))
print(overlap(pep4, pep5))
print(overlap(adn, pep5))

