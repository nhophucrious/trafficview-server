from flask import Blueprint, abort, request, make_response, jsonify
from app.controllers.composite_controller import get_image_and_predictions

image_with_predictions_blueprint = Blueprint('image_with_predictions', __name__, url_prefix='/api')

@image_with_predictions_blueprint.route('/get-image-with-predictions/<camera_id>', methods=['GET'])
def get_image_with_predictions(camera_id):
    # predict right with the camera image in BASE64
    try:
        # camera_id = request.args.get('camera_id')

        # if not camera_id:
        #     print("shit")
        #     abort(404, description="Missing camera_id parameter.")

        data = get_image_and_predictions(camera_id)

        response = make_response(jsonify(data), 200)

        return response

    except Exception as e:
        print(e)
        abort(404, description=str(e))