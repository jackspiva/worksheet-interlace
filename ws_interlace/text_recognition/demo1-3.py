import os, sys


def main(args):
	wordList = ["Jon", "Crls", "Sarah", "Tem"]
	dictionaryList  = ["Charles", "Greg", "Sarah", "Tim", "John", "Chris"]

	print(wordList)
	print(dictionaryList)

	refinedWordList = getRefinedWordList_Many2Many(wordList, dictionaryList)

	print(refinedWordList)

###
#
#	PUBLIC API CALLS
#
###


def getRefinedWord_Many2One(word, dictionaryList):
	"""
		Get the most similar word in a dictionaryList
			for a single word
	"""
	return getRefinedWordList_Many2Many([word], dictionaryList)

def getRefinedWordList_Many2Many(wordList, dictionaryList):
	"""
		Get the most similar words in a dictionaryList
			for each word in a word list
		Ensure that mapping is 1-to-1
	"""

	matrix = generateDistanceMatrix(wordList, dictionaryList, levenshteinDistance)
	matrix = wordDifferenceCountToIndex(matrix)

	refinedWordList = getClosetDictionaryWordList(matrix, wordList, dictionaryList)
	return refinedWordList


###
#
#	INTERNAL METHODS
#
###

def getClosetDictionaryWordList(sortedMatrix, wordList, dictionaryList):
	"""
		Lazy way of applying best choices to wordList
			No backtracking involved.
			Research "Assignment Problem" and corresponding algorithm
	"""
	s = set(dictionaryList)
	refinedWordList = wordList

	for rowI, row in enumerate(sortedMatrix):
		for preferredIndex in row:
			dWord = dictionaryList[preferredIndex]
			if dWord in s:
				refinedWordList[rowI] = dWord
				s.discard(dWord)
				break
			else:
				continue

	return refinedWordList
	
def wordDifferenceCountToIndex(matrix):
	"""
		Sort the 2d matrix of word difference counts
			Sort by the value of the tuple (index,value)
			Return the indeces (in their new order)

		Returns the ordered indices that each word prefers
			Used by stable 
	"""
	for rowI, row in enumerate(matrix):
		matrix[rowI] = [int(tup[0]) for tup in sorted(enumerate(row), key=lambda x: x[1])]
	
	return matrix


def print2DMatrix(matrix):
	"""
		Print the 2D matrix in a better format
	"""
	s = [[str(e) for e in row] for row in matrix]
	lens = [max(map(len, col)) for col in zip(*s)]
	fmt = '\t'.join('{{:{}}}'.format(x) for x in lens)
	table = [fmt.format(*row) for row in s]
	print('\n'.join(table))


def generateDistanceMatrix(wordList, dictionaryList, distanceFunction):
	"""
		Row: words in wordList
		Column: words in dictionaryList
	"""

	w, h = len(dictionaryList), len(wordList);
	distanceMatrix = [[0 for x in range(w)] for y in range(h)] 

	for wordI, word in enumerate(wordList):
		for dictWordI, dictWord in enumerate(dictionaryList):
			dist = distanceFunction(word, dictWord)
			distanceMatrix[wordI][dictWordI] = dist

	return distanceMatrix


def levenshteinDistance(s, t):
    
    ## base cases
    if s == t: return 0
    lenT = len(t)
    lenS = len(s)
    if lenS == 0: return lenT
    if lenT == 0: return lenS

    ##create two work vectors of integer distances
    v0 = [None] * (lenT + 1)
    v1 = [None] * (lenT + 1)

    ## initialize v0 (the previous row of distances)
    ## this row is A[0][i]: edit distance for an empty s
    ## the distance is just the number of characters to delete from t
    for i in range(lenT + 1):
    	v0[i] = i

    for i in range(lenS):
        ## calculate v1 (current row distances) from the previous row v0

        ## first element of v1 is A[i+1][0]
        ## edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1;

        ## use formula to fill in the rest of the row
        for j in range(lenT):
        	### Added bonus (-1) for strings that have correct letters
        	### Maintained penalty (1) for differences
            cost = -1 if (s[i] == t[j]) else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        ## copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(lenT + 1):
            v0[j] = v1[j]

    return v1[lenT]



if __name__ == '__main__':
    main(sys.argv)
