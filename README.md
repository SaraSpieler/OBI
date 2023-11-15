# OBI
#read fasta
def readFasta(filename):
    dico ={}
    content=""
    id=""
    seq = open(filename, "r")
    for i in seq.readlines():
        if i[0]==">" : 
            if id!="":
                dico[id]=content
            element = i.split("|")
            id = element[1]
        else : 
            content=content+i.strip('\n')
    dico[id]=content    
    return dico

seq = readFasta('my_sequence.fasta')
print(seq)



 #Read fasta small pep 

def readFasta(filename):
    dico ={}
    content=""
    id=""
    seq = open(filename, "r")
    for i in seq.readlines():
        if i[0]==">" : 
            if id!="":
                dico[id]=content
            
            id = i.strip('\n')
            id = id.strip('>')
        else : 
            content=i.strip('\n')
    dico[id]=content    
    return dico
