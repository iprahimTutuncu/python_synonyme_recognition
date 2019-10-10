import sys
import numpy as np
import synonym as syn
import entrainement as ent
import re
from ConnexionCxOracle import *
import cluster as clst
import ecrireFichier as ecf

def verifNombre(String):
	var = re.sub("[0-9]",'',String)
	if var == '':
		return True
	else:
		return False

def entrainement(fenetre, chemin, encodage,):
	fenetre = int(fenetre)

	
	connection = Connexion()
	text = ent.splitTextCorrectement(ent.readText(chemin, encodage))
	dictionnaire = ent.motsUniques(text)
	dictionnaire = ent.insertMotInDatabase(dictionnaire, connection)
	
	ent.genConcurenceMatDB2(text,fenetre,connection)
	
	connection.close()
	return dictionnaire

def recherche(fenetre):
	motTrompeur = ['tu' , 'autre', 'nôtres', 'auquel', 'aucunes', 'de', 't', 'tels',
	'même', 'tiennes', 'unes', 'ça', 'desquelles', 'la', 'tel', 'ceux',
	'tienne', 'celle', 'en', 'aucun', 'telle',  'tien',  'les', 'aucune',
	'où', 'certaines', 'cela', 'dont', 'certaine', 'soi', 'd', 'aucuns', 'te',
	'une', 'celui', 'un', 'se', 'auxquels', 'toi', 'siens', 'leur', 'y', 'ceci', 'mienne',
	'toutes', 'à', 'lequel', 'elle', 'qu',  'miennes', 'on', 'là', 'toute',
	'nôtre', 'ils',  'lesquelles', 'desquels', 'mien', 'me',
	'que', 'elles', 'est', 'lui', 'tous', 'tiens', 'celles', 'ci', 'qui', 'sienne', 'autres',
	'duquel', 'nuls', 'nul', 'nulles', 'il', 'quoi', 'telles', 'eux', 'leurs', 'm',
	'vôtres', 'vôtre', 'sien', 'siennes', 'uns', 'miens', 'moi', 'auxquelles', 'tout',
	'ce', 'le', 'laquelle', 'vous', 'mêmes', 'nous', 'lesquels', 'nulle', 'l', 'certains',
	'et', 'des', 's', 'dans', 'au', 'ne', 'du', 'son', 'pas','sa', 'n', 'sur',
	'plus', 'pour', 'par', 'avec', 'comme', 'ses', 'c', 'mais', 'cette', 'sans', 'si', 'sous',
	'ces', 'aux', 'a', 'je', 'quand', 'j', 'votre', 'mon', 'ma', 'cet', 'ou', 'mes', 'puis',
	'donc', 'près', 'quelque']

	connection = Connexion()
	
	methode = {0:syn.produitVectoriel,
				1:syn.manhatten,
				2:syn.least_squares,}
		
	rep = [""]

	dictionnaire = dict(connection.getMots())
	if len(dictionnaire) == 0:
		return 10
		
	dictMotTrompeur = {}
	for mot in motTrompeur:
		if mot in dictionnaire:
			dictMotTrompeur[dictionnaire[mot]] = 1
	
	concurrances = connection.getConcurranceMat(fenetre)
	if len(concurrances) == 0:
		return 11
	
	#remplir matrice
	matrice = np.zeros((len(dictionnaire), len(dictionnaire)))
	
	for conc in concurrances:
		matrice[conc[1]][conc[2]] = conc[3]
		matrice[conc[2]][conc[1]] = conc[3]

	connection.close()
	
	while rep[0].upper() != "Q":
		rep = input("Tapez un mot, le nombre de synonymes et la méthode de calcul,\ni.e. produit scalaire: 0, least square: 1, cityblock: 2 (Q pour quitter): ")
		rep = [str(x) for x in rep.split(" ")]

		if rep[0].upper() != "Q":
			mot =""
			type=0
			nbSynonyme=0
			if len(rep) == 3:

				mot = rep[0].lower()
				
				if mot in dictionnaire:
					if verifNombre(rep[1]):
						nbSynonyme = int(rep[1])
						if verifNombre(rep[2]):
							type = int(rep[2])

							if type in methode.keys():
								syn.MeilleurMots(methode[type], mot, matrice, dictionnaire, nbSynonyme, dictMotTrompeur)
							else:
								return 5
						else:
							return 8

					else:
						return 8
				else:
					return 9

			else:
				return 7

def main():
	fenetre = None
	encodage = None
	chemin = None
	index = -1

	optionEntrainement = ["-e", "-t", "-cc", "-enc"]
	optionRecherche	   = ["-s", "-t"]
	optionCluster	   = ["-t", "-nc", "-m", "-n"]
	#crash
	if "-e" in sys.argv and "-s" in sys.argv and "-nc" in sys.argv:
		return 1
	optionEntrainement = ["-t", "-cc", "-enc"]
	optionRecherche	   = ["-t"]
	optionCluster	   = ["-t", "-nc", "-n"]

	#option pour l'entrainement
	if "-e" in sys.argv:
		for option in optionEntrainement:
			if option not in sys.argv:
				return 2

		chemin   = sys.argv[sys.argv.index("-cc") 	+ 1]
		encodage = sys.argv[sys.argv.index("-enc") 	+ 1]
		fenetre  = sys.argv[sys.argv.index("-t")   	+ 1]

		if not verifNombre(fenetre):
			return 8
		entrainement(fenetre, chemin, encodage)

	#option pour la recherche
	elif "-s" in sys.argv:
		for option in optionRecherche:
			if option not in sys.argv:
				return 3

		fenetre  = sys.argv[sys.argv.index("-t")   	+ 1]
		if not verifNombre(fenetre):
			return 8
		return recherche(fenetre)
	elif "-nc" in sys.argv:
		for option in optionCluster:
			if option not in sys.argv:
				return 12
		if "-m" in sys.argv:
			#liste de mots
			listemots = sys.argv[sys.argv.index("-m") 	+ 1].split()
		else:
			listemots = "random"
		nbClusters = sys.argv[sys.argv.index("-nc") 	+ 1]
		nbMotsAffichage = sys.argv[sys.argv.index("-n") 	+ 1]
		fenetre  = sys.argv[sys.argv.index("-t")   	+ 1]
		print("CLUSTER")
		print("Fenetre", fenetre, "nbMotsAffichage", nbMotsAffichage, "nbClusters", nbClusters)
		print(listemots)
		ecf.initFichier(sys.argv)
		clst.cluster(int(nbClusters), int(fenetre), listemots, nbMotsAffichage)
		pass
		
	#crash
	else:
		
		return 4

if __name__ == "__main__":
	error = {1: "Erreur: -e et -s sont dans la liste, seul un des deux peuvent être présent",
			 2: "Erreur: commande manquante, invalide ou dupliqué dans l'entrainement",
			 3: "Erreur: commande manquante, invalide ou dupliqué dans la recherche",
			 4: "Erreur: -e et -s ne sont pasdans la liste, un des deux doit être présent",
			 5: "Erreur: méthode de calcul invalide",
			 6: "Erreur: nombre de synonyme entré invalide",
			 7: "Erreur: Nombre incorecte d'arguments",
			 8: "Erreur: Une chaine de caractères a été tappé au lien d'un nombre",
			 9: "Erreur: Mot innexistant dans le dictionnaire",
			 10: "Erreur: Dictionnaire vide. Faite un entrainement d'abord",
			 11: "Erreur: Matrice vide pour cette fenetre. Faite un entrainement d'abord",
			 12: "Erreur: commande manquante, invalide ou dupliqué dans la partition de données",}

	result = main()
	if result:
		print(error[result])
	sys.exit(result)
    
