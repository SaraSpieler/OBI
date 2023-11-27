#Stats OBI 

nb_prot_totales <- 100
nb_prot_identifies <- 90
c = matrix(c(c(nb_prot_totales,nb_prot_identifies),c(0,(nb_prot_totales-nb_prot_identifies))),nrow = 2, ncol = 2)
p = prop.test(c,alternative = c("less"))
print(p)