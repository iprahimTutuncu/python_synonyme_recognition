import numpy as np

def initFichier(argv):
	f = open("resultat.txt",'w+',encoding='utf-8')
	
	f.write(str(argv)+"\n\n")
	
	f.close()
	
def ecrireClusterMatrice(clusterMatrice):
	f = open("resultat.txt",'a',encoding='utf-8')
	nb = 1
	for c in clusterMatrice:
		f.write("Cluster"+str(nb)+"\n")
		for val in c:
			f.write(str(val)+" ")
		f.write("\n")
		nb += 1
	
	f.write("\n")
	
	f.close()

def ecrireResultats(clusterContainer,clusterMatrice,nbMotsAffichage,dictionnaire,matrice,nbIteration,time):
	f = open("resultat.txt",'a',encoding='utf-8')
	
	f.write("------------------------------------------------------------------------\n")
	f.write("                             RÉSULTATS\n")
	f.write("------------------------------------------------------------------------\n\n")
	
	noCluster = 1
	indexDict = {}
	
	f.write("\ntemps de l'opération : "+str(time)+" sec.")
	f.write("\nfait en "+str(nbIteration)+" iterations\n\n")
	
	for mot in dictionnaire:
		indexDict[dictionnaire[mot]] = mot
	
	for j in range(len(clusterContainer)):
		cluster = sortCluster(clusterContainer[j],clusterMatrice[j],dictionnaire,matrice)
		
		nbMot = len(cluster)
		
		f.write("------------------------------------\n")
		f.write("Cluster "+str(noCluster)+" - "+str(len(cluster))+" mots"+"\n")
		f.write("------------------------------------\n")
		
		i = 0
		while (i < nbMot) and (i < int(nbMotsAffichage)):
			f.write(indexDict[cluster[i][0]]+" >>>>>>>>>> "+str(cluster[i][1])+"\n")
			i += 1
			
		noCluster += 1
		
	f.close()
	
def ecrireIteration(clusterContainer,temps,iteration,nbChangement):
	f = open("resultat.txt",'a',encoding='utf-8')
	
	f.write("Iteration "+str(iteration)+"\n")
	f.write("fait en "+str(temps)+" sec.\n")
	f.write("nombre de changements de clusters : "+str(nbChangement)+"\n")
	
	for i in range(len(clusterContainer)):
		cluster = clusterContainer[i]
		nbMots = len(cluster)
		
		f.write("Cluster "+str(i+1)+", "+str(nbMots)+" mots\n")
	
	f.write("----------------------------------------------------\n\n")
	
	f.close()
	
def sortCluster(cluster,clusterMatrice,dictionnaire,matrice):
	for i in range(len(cluster)):
		index = cluster[i]
		vecMot = matrice[index]
	
		diff = vecMot - clusterMatrice
		length = np.dot(diff, diff)
		
		cluster[i] = (index,length)
	
	cluster = sorted(cluster,key=takeSecond)

	return cluster
	
def takeSecond(elem):
    return elem[1]
	