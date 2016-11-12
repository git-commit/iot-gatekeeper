import json, requests
import privateconfig, logging
import base64

#Note: The way to get api key:
#Free: https://www.microsoft.com/cognitive-services/en-us/subscriptions?productId=/products/Bing.Speech.Preview
#Paid: https://portal.azure.com/#create/Microsoft.CognitiveServices/apitype/Bing.Speech/pricingtier/S0
tts_url_api="https://speech.platform.bing.com"

class SpeechRecognition:

    accesstoken = None

    n = 0

    def __init__(self):
        self.renew_authentication()


    def renew_authentication(self):
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

        SpeechRecognition.accesstoken = data
        logging.debug ("Access Token: " + SpeechRecognition.accesstoken)

    def transformToAudio(self, text):
        if SpeechRecognition.n > 2 :
            return None

        body = "<speak version='1.0' xml:lang='en-us'> \
            <voice xml:lang='en-us' xml:gender='Male' name='Microsoft Server Speech Text to Speech Voice (en-US, BenjaminRUS)'>\
            %s</voice></speak>" % text

        headers = {"Content-type": "application/ssml+xml",
			           "X-Microsoft-OutputFormat": "riff-16khz-16bit-mono-pcm",
			           "Authorization": "Bearer " + SpeechRecognition.accesstoken,
			           "X-Search-AppId": "07D3234E49CE426DAA29772419F436CA",
	                   "X-Search-ClientID": "1ECFAE91408841A480F00935DC390960",
	                   "User-Agent": "TTSForPython"}

        #Connect to server to synthesize the wave
        logging.debug ("\nConnect to server to synthesize the wave")

        response = requests.post ("%s/synthesize" % tts_url_api, headers=headers, data=body)

        try:
            response.raise_for_status()
        except:
            logging.debug (response.text)
            self.renew_authentication()
            SpeechRecognition.n = SpeechRecognition.n + 1
            return self.transformToAudio(text)

        SpeechRecognition.n = 0

        data = response.content

        logging.debug ("The synthesized wave length: %d" %(len(data)))

        file = open('temp.wav', 'wb')
        file.write(data)
        return 'temp.wav'

    # Wave format audio
    def transformToText(self, audio_path):
        if SpeechRecognition.n > 2 :
            return None

        headers = {"Content-Type": "audio/wav; samplerate=16000",
			           "Authorization": "Bearer " + base64.b64encode(SpeechRecognition.accesstoken),
                       "Host": "speech.platform.bing.com"}

        params = {
            "scenarios": "smd",
            "appid": "D4D52672-91D7-4C74-8AD8-42B1D98141A5",
            "locale": "en-US",
            "device.os": "Linux",
            "version": "3.0",
            "format":"json",
            "requestid": "1d4b6030-9099-11e0-91e4-0800200c9a66&instanceid=1d4b6030-9099-11e0-91e4-0800200c9a66"
        }

        body = open(audio_path).read()

        #Connect to server to synthesize the wave
        logging.debug ("\nConnect to server to get text from wave")

        response = requests.post ("%s/query" % tts_url_api, headers=headers, params=params, data=body)

        try:
            response.raise_for_status()
        except:
            logging.debug (response.text)
            self.renew_authentication()
            SpeechRecognition.n = SpeechRecognition.n + 1
            return self.transformToText(audio_path)

        SpeechRecognition.n = 0

        logging.debug (response.json()[0]['results'])
