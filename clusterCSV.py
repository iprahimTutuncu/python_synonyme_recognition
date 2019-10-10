import random
import numpy as np
import synonym as s
#from ConnexionCxOracle import *
import ecrireFichier as ecf
from datetime import datetime
import math
import CSVData as csv


def cluster(nbClusters, fenetre, listemots, nbMotsAffichage):
	#matrice, dictionnaire = generateMatrix(fenetre)
	dictionnaire = csv.creerDictionnaire()
	matrice = csv.genererMatrice(csv.creerMatrice(fenetre),dictionnaire)
	#listeMots, nbMots, longueurMatrice, dictionnary, matrice
	#clusterMatrice = randomSeed(nbClusters,  len(matrice), matrice)
	#clusterMatrice = randomCluster(nbClusters,len(matrice), matrice)
	if listemots == "random":
		clusterMatrice = randomCluster(nbClusters,  len(matrice), matrice)
	else:
		clusterMatrice = wordSeed(nbClusters, len(matrice), dictionnaire, matrice)

	clusterContainer = []
	prevClusterContainer = []

	for n in range(nbClusters):
		clusterContainer.append([])
		prevClusterContainer.append([])
	time = datetime.now()
	clusterContainer,nbIteration,clusterMatrice = reCluster(matrice, dictionnaire, clusterMatrice, clusterContainer, prevClusterContainer, nbClusters)
	time = datetime.now() - time
	print("FIN")
	for n in range(nbClusters):
		print( "cluster" + str(n) + ": " + str(len(clusterContainer[n])))

		
	ecf.ecrireResultats(clusterContainer,clusterMatrice,nbMotsAffichage,dictionnaire,matrice,nbIteration,time)


def reCluster(matrice, dictionnaire, clusterMatrice, clusterContainer, prevClusterContainer, nbClusters):
	#parse les mots dans le bon cluster
	allEqual = False
	it = 0
	while not allEqual:
		print("Iteration", it)
		it+=1
		t = datetime.now()

		clusterContainer = []
		for n in range(nbClusters):
			clusterContainer.append([])

		allEqual = True
		indexMot = 0
		for indexMot in range(len(dictionnaire)):
		#for mot in dictionnaire.keys():
			#chercher le bon vecteur du mot
			#et mettre réiinit les valeurs
			vecMot = matrice[indexMot]
			closestCluster = 0
			score = float('Inf')

			#chercher le cluster le plus proche
			for clusterRow in range(len(clusterMatrice)):
				diff = vecMot - clusterMatrice[clusterRow]
				length = np.square(diff)
				length = np.sum(length)
				if(length < score):
					closestCluster = clusterRow
					score = length

			#ajouter le mot au cluster
			clusterContainer[closestCluster].append(indexMot)
			
		nbChangement = 0
			
		#verifier si les clusters ont changés
		for i in range(nbClusters):
			if(len(prevClusterContainer) != 0):
				clusterChangement = math.fabs(len(prevClusterContainer[i]) - len(clusterContainer[i]))
				if not np.array_equal(prevClusterContainer[i], clusterContainer[i]):
				#if clusterChangement > 0:
					print("ho aio!")
					nbChangement += clusterChangement
					allEqual = False

					
					
					#break
			else:
				allEqual = False
		#if allEqual:
		#	return

		#ancien cluster
		prevClusterContainer = list(clusterContainer)

		#centrer les cluster
		"""
		j = 0
		for cluster in clusterContainer:
			i = 0
			total = np.zeros(clusterMatrice[i].shape[0])
			for c in cluster:
				index = c
				vecteur = matrice[index]
				i+=1
				total += vecteur
			if i > 0:
				clusterMatrice[j] = (1/i) * total
			j+=1

		for n in range(nbClusters):
			print( "cluster" + str(n) + ": " + str(len(clusterContainer[n])))
		
		t = datetime.now() - t
		
		if it > 1:
			nbChangement = nbChangement / 2
		"""
		clusterMatrice = centrerCluster(clusterContainer,clusterMatrice,matrice)
		t = datetime.now() - t
		for n in range(nbClusters):
			print( "cluster" + str(n) + ": " + str(len(clusterContainer[n])))
		
		if it > 1:
			nbChangement = nbChangement / 2
		
		ecf.ecrireIteration(clusterContainer,t,it,nbChangement)
			
			
			
	return clusterContainer,it,clusterMatrice
	
def centrerCluster(clusterContainer,clusterMatrice,matrice):
	j = 0
	for cluster in clusterContainer:
		i = 0
		total = np.zeros(clusterMatrice[i].shape[0])
		for c in cluster:
			index = c
			vecteur = matrice[index]
			i+=1
			total += vecteur
		if i > 0:
			clusterMatrice[j] = (1/i) * total
		j+=1
		
		
			
	return clusterMatrice
			
		
def compareToCluster(cluster, mot):
	pass
	
def randomCluster(nbClusters, longueurMatrice, matrice):
	"""
	if nbClusters > 0:
		grandeur = int(longueurMatrice / nbClusters)

	generateur = np.random.randint(0,high=longueurMatrice,size=(nbClusters,grandeur))
	
	clusterMatrice = []
	for i in range(nbClusters):
		clusterMatrice.append(np.zeros(longueurMatrice))
		
	clusterMatrice = centrerCluster(generateur,clusterMatrice,matrice)
	"""
	clusterMatrice = []
	for i in range(nbClusters):
		clusterMatrice.append(np.zeros(longueurMatrice))
	generateur = []
	for i in range(nbClusters):
		generateur.append([])
		
	liste = np.random.randint(0,high=nbClusters,size=longueurMatrice)
	for i in range(longueurMatrice):
		generateur[liste[i]].append(i)
		
	clusterMatrice = centrerCluster(generateur,clusterMatrice,matrice)
	for c in range(nbClusters):
		print("cluster",c,len(generateur[c]))
	return clusterMatrice


def positionnementOrthogonalSeed(nbClusters, longueurMatrice, matrice):
	
	avgTotal = 0
	avgVec = np.zeros(longueurMatrice)
	for i in range(longueurMatrice):
		length = np.square(matrice[i])
		avgTotal += np.sum(length)
		avgVec += length
	avgTotal /= longueurMatrice

	avgVec /= longueurMatrice

	clusters = np.zeros((nbClusters, longueurMatrice))
	i = 0;
	for cluster in clusters:
		cluster[i] += avgTotal
		cluster += avgVec
		i += 1

	
	"""
	valMax = matrice.max(axis=0)
	valMin = matrice.min(axis=0)
	
	clusters = np.zeros((nbClusters, longueurMatrice))
	
	for c in clusters:
		for i in range(len(c)):
			c[i] = random.randint(valMin[i],valMax[i])
	"""
	return clusters
	
def wordSeed(listeMots, longueurMatrice, dictionnary, matrice):
	clusters = np.zeros((len(listeMots), longueurMatrice))
	print("listemots",listeMots)
	for mot , indice in zip(listeMots, range(len(listeMots))):
		print(mot, indice)
		if mot in dictionnary.keys():
			clusters[indice] = matrice[dictionnary[mot]]
	return clusters