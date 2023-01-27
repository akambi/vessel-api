from flask import Flask, jsonify
from flask_restful import Api
from api.resources.vessel_position_list import VesselPositionList
from api.models import db

def init_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("api.config.Config")
    app.config["BUNDLE_ERRORS"] = True

    db.init_app(app)  # initialise the database for the app
    with app.app_context():
        from api.models import VesselPosition # Create the table "vessels" if it does not exist
        db.drop_all()
        db.create_all()
        VesselPosition.load_data(app.config)
    
        api = Api(app)
        api.add_resource(VesselPositionList, '/vessels/positions')

        return app