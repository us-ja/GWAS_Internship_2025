dat<-read.csv("NAM_genos_imputed.csv",header=T,skip=2,dec=",",sep=";")
head(dat)

as.numeric(dat[,3])

gendat<-apply(dat[,-1],2,as.numeric)
