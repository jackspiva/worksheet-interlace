import os
import sys
from sklearn.externals import joblib
from sklearn.svm import LinearSVC

from ws_interlace.number_recognition.parsers import ImageParser
from ws_interlace.number_recognition.datasets import NISTDataset, UCILetterDataset, Chars74KDataset
from ws_interlace.number_recognition.classifiers import LinearSVM, LinearSVM_HOG


def test():
    print("test")


def parseNumberImage(imageName):
    print("parseNumberImage()")
    linearClassifierDigitsFile = "svm_digits_cls.pkl"
    hogLinearClassifierDigitsFile = "hog_svm_digits_cls.pkl"
    inputImagePath = "/Users/johnspiva/Google Drive/Programming/worksheet-project/media/" + \
        str(imageName)
    print("**********", inputImagePath)
    outputImagePath = os.path.join(
        "ws_interlace/number_recognition/images/labeled/", str(imageName))
    trainedDigitsFile = hogLinearClassifierDigitsFile
    locNumberList = parse(trainedDigitsFile, inputImagePath, outputImagePath)

    """ Sort tuples by 1st elem, return joined list of just 2nd elem"""
    locNumberList.sort(key=lambda tup: tup[0])
    numberList = [int(i[1]) for i in locNumberList]
    return int(''.join(map(str, numberList)))

def parseCustomNumberImage(pathToImg):
	print("parseCustomNumberImage()")
	print(pathToImg)
	outputImagePath = os.path.join("ws_interlace/number_recognition/images/labeled/", "demoOutput.png")
	trainedDigitsFile = "hog_svm_digits_cls.pkl"
	locNumberList = parse(trainedDigitsFile, pathToImg, outputImagePath)
	
	""" Sort tuples by 1st elem, return joined list of just 2nd elem"""
	locNumberList.sort(key=lambda tup: tup[0])
	numberList = [int(i[1]) for i in locNumberList]
	return int(''.join(map(str,numberList)))

def trainDigits():
    print("Loading NIST Dataset")
    nistDataset = NISTDataset()
    hogLinearClassifierDigitsFile = "hog_svm_digits_cls.pkl"
    hogLinearClassifier = LinearSVM_HOG(
        nistDataset, hogLinearClassifierDigitsFile)
    print("training number linear classifier with preprocessing ")
    hogLinearClassifier.trainAndSave()


def parse(classifierFilePath, inputImagePath, outputImagePath):
    parser = ImageParser()
    parser.load(classifierFilePath, inputImagePath)
    return parser.parse(outputImagePath)
