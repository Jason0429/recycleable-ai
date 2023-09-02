from flask import Flask
from flask_restful import Api
from .services.google_vision.gvs_resource import GoogleVisionResource
from .services.recycle_instruction.recycle_instruction_resource import RecycleInstructionResource



def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    api = Api(app)

    api.add_resource(GoogleVisionResource, "/api/gvs")
    api.add_resource(RecycleInstructionResource, "/api/recycle-instruction")

    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY = "dev"
        )
    else:
        app.config.from_mapping(test_config)


    return app