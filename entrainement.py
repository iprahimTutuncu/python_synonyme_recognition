import re
import numpy as np
from ConnexionCxOracle import *
#import time

def readText(path, enc = "utf-8"):
	s = ""
	print("reading file XD")
	f = open(path, 'r', encoding = enc)
	s += f.read()
	f.close()
	#print(s)
	return s

def splitTextCorrectement(text):
	phrases = re.findall('([A-Z][^\.!?w]*)', text[:])
	for n in range(len(phrases)):
		phrases[n] = re.sub("[^\w]", " ", phrases[n]).split()

	mots = []
	for phrase in phrases:
		mots += phrase

	mots = [x.lower() for x in mots]

	return mots

def motsUniques(text):
	d = {}
	index = 0
	for mot in text:
		if mot not in d:
			d[mot] = index
			index+=1
	return d

def insertMotInDatabase(dictmotsuniques, connection):

	####Inserer les mots d'un dictionnaire trouvés dans la bd dans la bd
	print("Adding words to Database")
	d = {}
	index = 0
	if not connection.findIfTablesExist():
		print("Table Don't exist")
		connection.buildScript('Create Table.sql')
	
	#Recherche des ID existants
	connection.curseur.execute('Select chaine, id From mot Order By id')
	fullresult = connection.curseur.fetchall()
	
	if fullresult:
		d = dict(fullresult)

		index = fullresult[-1][1] + 1

	
	for mot, ind in dictmotsuniques.items():
		if mot not in d.keys():
			connection.curseur.execute('Insert into mot (id, chaine) values (:id, :chain)', {'chain':mot, 'id':index})
			d[mot] = index
			index+=1
		else:
			pass
	connection.curseur.execute('Commit')
	print("Words added - Changes Commited")

	return d
				
def genConcurenceMatDB2(text,taille, connection):
	print("GENERE MATRICE2")
	d = 0
	m = taille//2
	f = taille
	di = {}
	matrice = {}
	
	connection.curseur.execute("select chaine,id from mot")
	curtuple = connection.curseur.fetchall()
	if curtuple:
		di = dict(curtuple)
	
	while f <= len(text):

		i = d
		motAnalyse = text[m]
		
		if motAnalyse not in di:
			di[motAnalyse] = connection.getIndex(motAnalyse)
		indexMot = di[motAnalyse]
		
		while i < f:
			if i != m:
				motConc = text[i]
				if motAnalyse != motConc:

					if motConc not in di:
						di[motConc] = connection.getIndex(motConc)
					indexConc = di[motConc]
					
					mot1,mot2 = 0,0
					if indexMot > indexConc:
						mot1,mot2 = indexConc,indexMot
					else:
						mot1,mot2 = indexMot,indexConc
						
					if (mot1,mot2) not in matrice:
						matrice[(mot1,mot2)] = 1
					else:
						matrice[(mot1,mot2)] += 1
						
			i+=1
		d+=1
		m+=1
		f+=1
						
	keys = list(matrice.keys())

	curtuple = None
	vecteurs = {}
	update = []
	nouveau = []
	connection.curseur.execute("select idmot1,idmot2,nbconcurrences,id from concurrence where fenetre = :fenetre",{"fenetre":taille})
	curtuple = connection.curseur.fetchall()
	if curtuple:
		for cur in curtuple:
			vecteurs[(cur[0],cur[1])] = (cur[2],cur[3])
	print("Insert dans BD")		
	for m in matrice:
		if m in vecteurs:
			update.append((matrice[m]+vecteurs[m][0],vecteurs[m][1]))
		else:
			nouveau.append((m[0],m[1],matrice[m],taille))

	if len(nouveau) > 0:
		print("INSERT")		
		connection.curseur.executemany("insert into concurrence(idmot1,idmot2,nbconcurrences,fenetre) values(:1,:2,:3,:4)",nouveau)
		connection.curseur.execute("commit")
	if len(update) > 0:
		print("UPDATE")
		connection.curseur.executemany("update concurrence set nbconcurrences = :1 where id = :2",update)
		connection.curseur.execute("commit")	


def genConcurrenceMatCSV(text,taille,matrice,dictionnaire):
	d = 0
	m = taille//2
	f = taille
	
	while f <= len(text):

		i = d
		motAnalyse = text[m]

		indexMot = dictionnaire[motAnalyse]
		
		while i < f:
			if i != m:
				motConc = text[i]
				if motAnalyse != motConc:
				
					indexConc = dictionnaire[motConc]
					
					mot1,mot2 = 0,0
					if indexMot > indexConc:
						mot1,mot2 = indexConc,indexMot
					else:
						mot1,mot2 = indexMot,indexConc
						
					if (mot1,mot2,taille) not in matrice:
						matrice[(mot1,mot2,taille)] = 1
					else:
						matrice[(mot1,mot2,taille)] += 1
						
			i+=1
		d+=1
		m+=1
		f+=1
		
	return matrice
