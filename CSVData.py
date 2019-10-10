import numpy as np

fichier_mot = "mot.csv"
fichier_concurrence = "concurrence.csv"

def creerDictionnaire():
	dict = {}
	f = open(fichier_mot,'r',encoding='UTF-8')
	text = f.read()
	#print(text)
	text = text.split('\n')
	for ligne in text:
		ligne = ligne.split(';')
		if len(ligne) == 2:
			mot = ligne[0]
			index = int(ligne[1])
			
			dict[mot] = index
			#print(mot,index)
		
	f.close()
	return dict
		
def enregistreDictionnaire(dict):
	f = open(fichier_mot,'a',encoding='UTF-8')
	ligne = "{0};{1}\n"
	
	for d in dict:
		f.write(ligne.format(d,dict[d]))
		
	f.close()
	
def nouveauMot(dict):
	fichierDict = creerDictionnaire()
	nb = conteMot()
	d = {}
	
	for mot in dict:
		if mot not in fichierDict:
			d[mot] = nb
			nb += 1

	enregistreDictionnaire(d)
	
	
def conteMot():
	f = open(fichier_mot,'r',encoding='UTF-8')

	nb = 0
	
	for ligne in f:
		ligne = ligne.split(';')
		if len(ligne) == 2:
			nb += 1
		
	f.close()
	return nb
	
def creerMatrice(taille=0):
	mat = {}

	f = open(fichier_concurrence,'r',encoding='UTF-8')
	text = f.read()
	text = text.split('\n')
	for ligne in text:
		ligne = ligne.split(';')
		if len(ligne) == 4:
			#print(ligne)
			index1 = int(ligne[0])
			index2 = int(ligne[1])
			nbconcurrence = int(ligne[2])
			fenetre = int(ligne[3])
			#print(fenetre)
			
			if taille == fenetre:
				mat[(index1,index2)] = nbconcurrence
			elif taille == 0:
				mat[(index1,index2,fenetre)] = nbconcurrence
			
	f.close()
	#print(mat)
	return mat
	
def genererMatrice(concurrances,dictionnaire):
	
	#remplir matrice
	matrice = np.zeros((len(dictionnaire), len(dictionnaire)))
	for conc in concurrances:
		matrice[conc[0]][conc[1]] = concurrances[conc]
		matrice[conc[1]][conc[0]] = concurrances[conc]
		
	return matrice
	
	
def enregistreMatrice(mat):
	f = open(fichier_concurrence,'w+',encoding='UTF-8')
	
	ligne = "{0};{1};{2};{3}\n"
	print(len(mat))
	for m in mat:
		nb = mat[m]
		mot1 = m[0]
		mot2 = m[1]
		taille = m[2]
		#print(mot1,mot2,nb)
		f.write(ligne.format(mot1,mot2,nb,taille))
				
	f.close()