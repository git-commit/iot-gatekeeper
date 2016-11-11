import requests
from gatekeeper import config


class FaceRecognition:

    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': '%s' % config.azure_subs_id,
    }
    image_folder = '../auth_pictures/'

    def decode_face(self, image_name):
        params = {
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false'
        }
        body = open(self.image_folder + image_name, 'rb').read()
        response = requests.post("%s/face/v1.0/detect" % config.azure_api_url, params=params, headers=self.headers, data=body)
        print(response.text)
        response.raise_for_status()
        return response.json()[0]['faceId']

    def verify_face(self, ):
        params = None
        try:
            conn = http.client.HTTPSConnection(config.azure_api_url)
            conn.request("POST", "/face/v1.0/verify?%s" % params, "{body}", self.headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

FaceRecognition().decode_face('trump.jpg')