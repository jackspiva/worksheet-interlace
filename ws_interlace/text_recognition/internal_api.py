########### Python 3.2 #############
import sys
import http.client
import urllib.request
import urllib.parse
import urllib.error
import base64
import requests
import time
import json
import timeit


def refinedProcessWordList(url, wordList):
    textList = getHandwrittenTextFromRemoteURL(url)
    return getRefinedWordList_Many2Many(textList, wordList)


def processWordList(url):
    textList = getHandwrittenTextFromRemoteURL(url)
    # return getRefinedWordList_Many2Many(textList, wordList)
    return textList


def parseRecognizedTextJSON(recognizedTextJSON):
    # Dependent on Microsoft Cognitive Service API specs

    # ORDER NOT PRESERVED FOR NOW
    # When preserving order, sort top to bottom and as tiebreaker use left to
    # right

    recognizedText = []
    lineObjectList = recognizedTextJSON['recognitionResult']['lines']

    for lineObject in lineObjectList:
        for w in lineObject['words']:
            recognizedText.append(w['text'])

    return recognizedText


def getHandwrittenTextFromRemoteURL(remote_url):
    requestHeaders = {
        # Request headers - replace this example key with your valid subscription key.
        # Another valid content type is "application/octet-stream".
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '8802be67d66f4f32889d0c404c4f56ac',
    }

# URL of a JPEG image containing text.
    body = {'url': remote_url}

    # Microsoft Cognitive Services API
    serviceUrl = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'

    # For printed text, set "handwriting" to false.
    params = {'handwriting': 'true'}

    try:
        start_time = timeit.default_timer()

        response = requests.request(
            'post', serviceUrl, json=body, data=None, headers=requestHeaders, params=params)
        print(response.status_code)

        # This is the URI where you can get the text recognition operation
        # result.
        operationLocation = response.headers['Operation-Location']

        # Note: The response may not be immediately available. Handwriting recognition is an
        # async operation that can take a variable amount of time depending on the length
        # of the text you want to recognize. You may need to wait or retry this
        # GET operation.

        time.sleep(10)
        response = requests.request(
            'get', operationLocation, json=None, data=None, headers=requestHeaders, params=None)
        elapsed = timeit.default_timer() - start_time
        print(elapsed)

        return parseRecognizedTextJSON(response.json())
    except Exception as e:
        print(e)
        return []


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

    matrix = generateDistanceMatrix(
        wordList, dictionaryList, levenshteinDistance)
    matrix = wordDifferenceCountToIndex(matrix)

    refinedWordList = getClosetDictionaryWordList(
        matrix, wordList, dictionaryList)
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
        matrix[rowI] = [int(tup[0]) for tup in sorted(
            enumerate(row), key=lambda x: x[1])]

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

    w, h = len(dictionaryList), len(wordList)
    distanceMatrix = [[0 for x in range(w)] for y in range(h)]

    for wordI, word in enumerate(wordList):
        for dictWordI, dictWord in enumerate(dictionaryList):
            dist = distanceFunction(word, dictWord)
            distanceMatrix[wordI][dictWordI] = dist

    return distanceMatrix


def levenshteinDistance(s, t):

    # base cases
    if s == t:
        return 0
    lenT = len(t)
    lenS = len(s)
    if lenS == 0:
        return lenT
    if lenT == 0:
        return lenS

    # create two work vectors of integer distances
    v0 = [None] * (lenT + 1)
    v1 = [None] * (lenT + 1)

    # initialize v0 (the previous row of distances)
    # this row is A[0][i]: edit distance for an empty s
    # the distance is just the number of characters to delete from t
    for i in range(lenT + 1):
        v0[i] = i

    for i in range(lenS):
        # calculate v1 (current row distances) from the previous row v0

        # first element of v1 is A[i+1][0]
        # edit distance is delete (i+1) chars from s to match empty t
        v1[0] = i + 1

        # use formula to fill in the rest of the row
        for j in range(lenT):
            # Added bonus (-1) for strings that have correct letters
            # Maintained penalty (1) for differences
            cost = -1 if (s[i] == t[j]) else 1
            v1[j + 1] = min(v1[j] + 1, v0[j + 1] + 1, v0[j] + cost)

        # copy v1 (current row) to v0 (previous row) for next iteration
        for j in range(lenT + 1):
            v0[j] = v1[j]

    return v1[lenT]
