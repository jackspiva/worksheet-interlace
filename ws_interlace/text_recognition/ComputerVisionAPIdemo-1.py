########### Python 3.2 #############
import sys, http.client, urllib.request, urllib.parse, urllib.error, base64, requests, time, json


def main(args):
	if len(args) == 2:
		url = args[1]
	else:
		url = "http://www.polyvore.com/cgi/img-thing?.out=jpg&size=l&tid=39165497"

	textList = getHandwrittenTextFromRemoteURL(url)
	print(textList)



def parseRecognizedTextJSON(recognizedTextJSON):
	# Dependent on Microsoft Cognitive Service API specs

	### ORDER NOT PRESERVED FOR NOW
	## When preserving order, sort top to bottom and as tiebreaker use left to right

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
	body = {'url':remote_url}

	# Microsoft Cognitive Services API
	serviceUrl = 'https://westus.api.cognitive.microsoft.com/vision/v1.0/RecognizeText'

	# For printed text, set "handwriting" to false.
	params = {'handwriting' : 'true'}


	try:
		response = requests.request('post', serviceUrl, json=body, data=None, headers=requestHeaders, params=params)
		print(response.status_code)

		# This is the URI where you can get the text recognition operation result.
		operationLocation = response.headers['Operation-Location']

		# Note: The response may not be immediately available. Handwriting recognition is an
		# async operation that can take a variable amount of time depending on the length
		# of the text you want to recognize. You may need to wait or retry this GET operation.

		time.sleep(10)
		response = requests.request('get', operationLocation, json=None, data=None, headers=requestHeaders, params=None)
		return parseRecognizedTextJSON(response.json())
	except Exception as e:
		print(e)
		return []


if __name__ == '__main__':
	main(sys.argv)