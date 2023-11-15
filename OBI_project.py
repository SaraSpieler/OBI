#!/usr/bin/env python3
# -*- coding: utf-8 -*-


def readFasta(filename):
    dico ={}
    content=""
    id=""
    seq = open(filename, "r")
    for i in seq.readlines():
        if i[0]==">" : 
            if id!="":
                dico[id]=content
            id = i
            content = ""  
        else : 
            content=content+i.strip('\n')
    dico[id]=content
    return dico


seq = readFasta('test2.fa')
print(seq)










