from email.message import Message
from flask import request
from flask_restful import Resource
import os, io
from google.cloud import vision
from google.protobuf.json_format import MessageToDict




class GoogleVisionResource(Resource):
    def post(self):
        """
        Identifies objects in image and returns a filtered list of objects.
        Filters duplicates and objects with <.5 confidence scores

        Ex:
        Takes in JSON body:
        {
            "uri": "https://cloud.google.com/vision/docs/images/bicycle_example.png"
        }

        Returns 
        {
            "obj": [
            {
                "name": "Bicycle wheel",
                "score": 0.9423431158065796
            },
            {
                "name": "Bicycle",
                "score": 0.897310733795166
            },
            {
                "name": "Picture frame",
                "score": 0.7171173691749573
            }
            ]
        }
        """
        json_data = request.get_json(force=True)
        print(json_data)
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = r'src/services/google_vision/google_vision_token.json'

        client = vision.ImageAnnotatorClient()

        image = vision.Image()
        image.source.image_uri = json_data["uri"]
        print(image)

        objects = client.object_localization(image=image).localized_object_annotations
        print(objects)
        obj_array = []
        obj_set = set()
        for obj in objects:
            if obj.name not in obj_set and float(obj.score)>.20:
                obj_array.append({"name": obj.name, "score": obj.score})
                obj_set.add(obj.name)
        

        return {"objects": obj_array}


