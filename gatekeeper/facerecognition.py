import logging
import requests
import os
import config
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
        face_id = self.decode_face_from_file(image_name)
        decoded_auth_faces[image_name] = (face_id, datetime.now())
        return face_id

    def decode_face_from_file(self, image_name):
        return self.decode_page_from_image(open(self.image_folder + image_name, 'rb').read())

    def decode_page_from_image(self, image):
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': '%s' % config.azure_subs_id,
        }
        params = {
            # Request parameters
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false'
        }
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

    def verify_face_id(self, face_id):
        for image_name in os.listdir(self.image_folder):
            if self.are_same(face_id, self.get_face_id(image_name)):
                return image_name
        return None

    def is_valid(self, last_decode):
        return datetime.now() - timedelta(days=1) < last_decode

    def add_auth_person(self, image, name):
        image.download(self.image_folder + '%s.jpg' % name)

    def verify_face(self, image):
        face_id = self.decode_page_from_image(image)
        return self.verify_face_id(face_id)
