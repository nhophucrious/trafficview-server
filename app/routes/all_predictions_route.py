from flask import Blueprint, abort, request, make_response, jsonify
from app.controllers.all_predictions_controller import get_only_predictions

all_predictions_blueprint = Blueprint('all_predictions', __name__, url_prefix='/api')

@all_predictions_blueprint.route('/get-only-predictions/<camera_id>', methods=['GET'])
def get_only_predictions_route(camera_id):
    # predict right with the camera image, but do not return the image
    try:
        data = get_only_predictions(camera_id)

        response = make_response(jsonify(data), 200)

        return response

    except Exception as e:
        print(e)
        abort(404, description=str(e))