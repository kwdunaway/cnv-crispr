setwd("~/Programming/Git/cnv-crispr/")
library(ggplot2)
install.packages("vegan")
library(vegan)

#############
# Permanova #
#############


#############
# Functions #
#############
process_CNV_table = function(df){
  df$Ratio_D7R1 = df$norm_count_D7_Rep1/df$norm_count_plasmid  
  df$Ratio_D7R2 = df$norm_count_D7_Rep2/df$norm_count_plasmid  
  df$Ratio_D14R1 = df$norm_count_D14_Rep1/df$norm_count_plasmid  
  df$Ratio_D14R2 = df$norm_count_D14_Rep2/df$norm_count_plasmid  
  df$Ratio_PLX7R1 = df$norm_count_PLX7_Rep1/df$norm_count_plasmid  
  df$Ratio_PLX7R2 = df$norm_count_PLX7_Rep2/df$norm_count_plasmid  
  df$Ratio_PLX14R1 = df$norm_count_PLX14_Rep1/df$norm_count_plasmid  
  df$Ratio_PLX14R2 = df$norm_count_PLX14_Rep2/df$norm_count_plasmid
  df$Ratio_D7 = (df$norm_count_D7_Rep1+df$norm_count_D7_Rep2)/(2*df$norm_count_plasmid)
  df$Ratio_D14 = (df$norm_count_D14_Rep1+df$norm_count_D14_Rep2)/(2*df$norm_count_plasmid)
  df$Ratio_PLX7 = (df$norm_count_PLX7_Rep1+df$norm_count_PLX7_Rep2)/(2*df$norm_count_plasmid)
  df$Ratio_PLX14 = (df$norm_count_PLX14_Rep1+df$norm_count_PLX14_Rep2)/(2*df$norm_count_plasmid)
  return(df)
}

#############
# Load data #
#############
CNVtable = read.table("data/CNV_guide_table.tsv", header = TRUE, sep = "\t") 
CNVtable = process_CNV_table(CNVtable)
OStable = read.table("Shalem_2014Table_S1.txt", header = TRUE, sep = "\t")

#############
# Graph #
#############
CNVtable_sub = subset(CNVtable, CNVcount > 1 & CNVcount < 4) 
CNVtable_subhigh = subset(CNVtable_sub, Ratio_PLX14 > 1)
CNVtable_sublow = subset(CNVtable_sub, Ratio_PLX14 <= 1)

ggplot(CNVtable_sub, aes(norm_count_plasmid, Ratio_D14R2)) + theme_bw() +
  geom_point(size = .15, aes(color = factor(CNVcount)))
  geom_point(size = .5, aes(color = factor(CNVcount)))

ggplot(CNVtable_sublow, aes(factor(CNVcount), Ratio_D14)) + theme_bw() +
  geom_boxplot() + scale_y_log10()

geom_boxplot(aes(color = factor(CNVcount)))
ggplot(mtcars, aes(factor(cyl), mpg))

  geom_point(colour = "blue", size = .5) +
  geom_abline(slope = 1, intercept = 0) +
  #  scale_x_sqrt(limits = c(1,200)) +  scale_y_sqrt(limits = c(1,200)) +
  theme_bw()




CNVtable$D7 = (CNVtable$norm_count_D7_Rep1 + CNVtable$norm_count_D7_Rep2) / 2
CNVtable$D14 = (CNVtable$norm_count_D14_Rep1 + CNVtable$norm_count_D14_Rep2) / 2
CNVtable$ChangeD7 = CNVtable$D7 - CNVtable$norm_count_plasmid
CNVtable$ChangeD14 = CNVtable$D14 - CNVtable$norm_count_plasmid

#######################
# Ploting based on OS #
#######################
CNVtable2$dif = abs(log(CNVtable2$norm_count_D7_Rep1/CNVtable2$norm_count_plasmid, base = 2) - log(CNVtable2$norm_count_D7_Rep2/CNVtable2$norm_count_plasmid, base = 2))
CNVtable2$dif = CNVtable2$norm_count_D7_Rep1/CNVtable2$norm_count_plasmid - CNVtable2$norm_count_D7_Rep2/CNVtable2$norm_count_plasmid
ggplot(CNVtable2, aes(OS, dif)) +
  geom_point(colour = "blue", size = .5) +
  theme_bw()

ggplot(CNVtable2, aes(OS, norm_count_plasmid)) + geom_point(colour = "blue", size = .5) + theme_bw()

############################
# Off targe score analysis #
############################
CNVtable2highOS = subset(CNVtable2, OS > 400) #11334
CNVtable2lowOS = subset(CNVtable2, OS <= 400) #52742
genes = unique(CNVtable2$gene_name)

OShigh = subset(OStable, OS > 400) #11484
OSlow = subset(OStable, OS <= 400) #53267
genes = as.character(unique(OStable$Gene.name) )
geneshigh = as.character(unique(OShigh$Gene.name) )
geneslow = as.character(unique(OSlow$Gene.name) )

#############
# Plots #
#############
CNVtable_sub = subset(CNVtable, gene_name == "RPS19BP1")
ggplot()

CNVtable_sub = subset(CNVtable, CNVcount == "2")
summary(CNVtable_sub)
ggplot(CNVtable_sub, aes(ChangeD14, ChangeD7)) +
  geom_point(colour = "blue", size = .5) +
  geom_abline(slope = 1, intercept = 0) +
#  scale_x_sqrt(limits = c(1,200)) +  scale_y_sqrt(limits = c(1,200)) +
  theme_bw()

ggplot(CNVtable_sub, aes(norm_count_D14_Rep1, norm_count_D14_Rep2)) +
  geom_point(colour = "blue", size = .5) +
  geom_abline(slope = 1, intercept = 0) +
  scale_x_sqrt(limits = c(1,200)) +  scale_y_sqrt(limits = c(1,200)) +
  theme_bw()

ggplot(CNVtable_sub, aes(norm_count_D7_Rep1, norm_count_D7_Rep2)) +
  geom_point(colour = "blue", size = .5) +
  geom_abline(slope = 1, intercept = 0) +
  scale_x_sqrt(limits = c(1,200)) +  scale_y_sqrt(limits = c(1,200)) +
  theme_bw()

ggplot(CNVtable_sub, aes(norm_count_plasmid, norm_count_D14_Rep1)) +
  geom_point(colour = "blue") +
  geom_abline(slope = 1, intercept = 0) +
  scale_x_sqrt(limits = c(1,200)) +  scale_y_sqrt(limits = c(1,200)) +
  theme_bw()



