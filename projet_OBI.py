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


seq_pep = read_fasta('test_peptide.fa')
seq_prot = read_fasta('test_prot.fa')

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
    the_dico = {k: v for k, v in the_dico.items() if k is not 'None'}
    


    print("Avant supressions proteine avec moins de deux peptides : \n", the_dico)
    ##ENLEVE PROT AVEC MOINS DE 2 PEPTIDES 
    #pareil grace a la comprehension de dictionnaire.
    the_dico = {k: v for k, v in the_dico.items() if len(v) >= 2}

                
    return the_dico #return le dico trier a la fin
            
            
a = unique_match_set('test_peptide.fa', 'test_prot.fa')
print("\n Dictionnaire : ", a)