import json, requests
import privateconfig, logging

#Note: The way to get api key:
#Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
#Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0
tts_url_api="https://speech.platform.bing.com"

class TextToSpeech:

    accesstoken = None

    def __init__(self):
        params = ""
        headers = {"Ocp-Apim-Subscription-Key": privateconfig.bing_speech_token}

        accessTokenUri = "https://api.cognitive.microsoft.com/sts/v1.0/issueToken"

        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

        # Connect to server to get the Access Token
        logging.debug ("Connect to server to get the Access Token")

        response = requests.post(accessTokenUri, params=params, headers=headers)
        logging.debug (response.text)

        data = response.text

        response.raise_for_status()

        TextToSpeech.accesstoken = data
        logging.debug ("Access Token: " + TextToSpeech.accesstoken)

    def transformToAudio(self, text):
        body = "<speak version='1.0' xml:lang='en-us'> \
            <voice xml:lang='en-us' xml:gender='Male' name='Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)'>\
            %s</voice></speak>" % text

        headers = {"Content-type": "application/ssml+xml",
			           "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
			           "Authorization": "Bearer " + TextToSpeech.accesstoken,
			           "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
	                   "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
	                   "User-Agent": "TTSForPython"}

        #Connect to server to synthesize the wave
        logging.debug ("\nConnect to server to synthesize the wave")

        response = requests.post ("%s/synthesize" % tts_url_api, headers=headers, data=body)

        response.raise_for_status()

        data = response.content

        logging.debug ("The synthesized wave length: %d" %(len(data)))

        file = open('temp.wav', 'wb')
        file.write(data)
        return 'temp.wav'
