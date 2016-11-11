import logging
import requests
import os
from gatekeeper import config
from datetime import datetime, timedelta

# After decoding authenticated face we store it to this dictionary for 24 hours, to reduce the number of decoding requests
decoded_auth_faces = {}

class FaceRecognition:

    image_folder = '../auth_pictures/'

    def get_face_id(self, image_name):
        if image_name in decoded_auth_faces:
            face_id, last_decode = decoded_auth_faces[image_name]
            if self.is_valid(last_decode):
                return face_id
        face_id = self.decode_face(image_name)
        decoded_auth_faces[image_name] = (face_id, datetime.now())
        return face_id

    def decode_face(self, image_name):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '%s' % config.azure_subs_id,
        }
        params = {
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false'
        }
        body = open(self.image_folder + image_name, 'rb').read()
        response = requests.post("%s/face/v1.0/detect" % config.azure_api_url, params=params, headers=headers, data=body)
        logging.debug(response.text)
        response.raise_for_status()
        return response.json()[0]['faceId']

    def are_same(self, face_id1, face_id2):
        headers = {
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '%s' % config.azure_subs_id,
        }
        body = {
            "faceId1": face_id1,
            "faceId2": face_id2
        }
        response = requests.post("%s/face/v1.0/verify" % config.azure_api_url, headers=headers, json=body)
        logging.debug(response.text)
        response.raise_for_status()
        return response.json()['isIdentical']

    def verify_face(self, face_id):
        for image_name in os.listdir(self.image_folder):
            if self.are_same(face_id, self.get_face_id(image_name)):
                return True
        return False

    def is_valid(self, last_decode):
        return datetime.now() - timedelta(days=1) < last_decode


FaceRecognition().are_same("bb8d90b7-ffec-4ab1-92e0-636c18e8619b", "c1838c6f-2e46-487b-8be3-76e878bebd0c")
