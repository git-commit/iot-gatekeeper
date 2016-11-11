import http.client
import json
import urllib.error
import urllib.parse
import urllib.request

from gatekeeper import config


class FaceRecognition:

    headers = {
        # Request headers
        'Content-Type': 'application/json',
        'Ocp-Apim-Subscription-Key': '%s' % config.azure_subs_id,
    }

    def decode_face(self):
        params = urllib.parse.urlencode({
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false'
        })
        body = ' {"url": "%s"}' % config.test_trump_image_url
        conn = http.client.HTTPSConnection(config.azure_api_url)
        conn.request("POST", "/face/v1.0/detect?%s" % params, body, self.headers)
        response = conn.getresponse()
        data_str = response.read().decode('utf-8')
        print(data_str)
        data = json.loads(data_str)
        conn.close()
        return data[0]['faceId']

    def verify_face(self):
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

FaceRecognition().decode_face()