import numpy as np

def produitVectoriel(text_input, matrice, dictionnaire):
    row = dictionnaire[text_input]

    result = np.dot(matrice[row], matrice)
    return result

def least_squares(text_input, matrice, dictionnaire):
    row = dictionnaire[text_input]

    result = []
    x = matrice[row] - matrice
    x = np.square(x)

    for m in range(len(matrice)):
        result.append(np.sum(x[m]))

    return result

def manhatten(text_input, matrice, dictionnaire):
    row = dictionnaire[text_input]

    result = []
    x = matrice[row] - matrice
    x = np.absolute(x)

    for m in range(len(matrice)):
        result.append(np.sum(x[m]))

    return result

def MeilleurMots(foncCalcul, text_input, matrice, dictionnaire, qtMots = 20, motfiltre = {}):
    scoreNum = foncCalcul(text_input, matrice, dictionnaire)
    scoreInfo = []

    #filtre mots
    for mot, index in dictionnaire.items():
        if index not in motfiltre and index != dictionnaire[text_input]:
            scoreInfo.append((scoreNum[index], mot))


    #resultat trier
    renverser = False
    if foncCalcul == produitVectoriel:
        renverser = True
    sortedScore = sorted(scoreInfo, reverse=renverser)

    for score, mot in sortedScore[:qtMots]:
        print( '(' + mot + ', ' + str(score) + ')')
