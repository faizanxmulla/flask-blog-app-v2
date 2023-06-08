from flask import send_file
from flask_restful import Resource
from flask_jwt_extended import jwt_required

from flask import current_app as app
from app.tasks import *

# -------------- 

class ExportAPI(Resource):
    @jwt_required()
    def get(self): 
        with app.app_context():
            task = export_csv.delay()

            result = task.wait()
            print(result)

            csv_path = result['csv_path']
            response = send_file(csv_path, as_attachment=True)

            return response
