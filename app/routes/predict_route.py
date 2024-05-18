from flask import Blueprint, abort, request, make_response, jsonify, send_file
from app.controllers.velocity_controller import predict_velocity, predict_velocity_from_image
from app.controllers.density_controller import predict_density
from app.controllers.condition_controller import predict_condition
import base64
from PIL import Image
from io import BytesIO

predict_blueprint = Blueprint('velocity', __name__, url_prefix='/api')

# Get the prediction for all aspects
@predict_blueprint.route('/predict', methods=['GET'])
def predict_all_aspects():
    try:
        camera_id = request.args.get('camera_id')
        
        if not camera_id:
            abort(404, description="Missing camera_id parameter.")
            
        velocity = predict_velocity(camera_id)
        condition = predict_condition(camera_id)
        density = predict_density(camera_id)
        
        data = {
            'velocity': velocity,
            'condition': condition,
            'density': density
        }
        
        response = make_response(jsonify(data), 200)
        
        return response
    except Exception as e:
        abort(404, description=str(e))

@predict_blueprint.route('/predict-image', methods=['POST'])
def predict_image():
    try:
        # get the image from the request body 
        # base64 string
        image = request.json['image']

        # remove data:image/jpeg;base64, if it exists
        if 'base64,' in image:
            image = image.split('base64,')[1]

        # get prediction from the image
        image_bytes = BytesIO(base64.b64decode(image))
        image_to_predict = Image.open(image_bytes).convert("RGB")

        velocity = predict_velocity_from_image(image_to_predict)
        data = {
            'velocity': velocity,
        }

        response = make_response(jsonify(data), 200)
        return response

    except Exception as e:
        print(e)
        abort(404, description=str(e))

# Get the prediction for a specific aspect
@predict_blueprint.route('/predict/<aspect>', methods=['GET'])
def predict_specific_aspect(aspect):
    try:
        camera_id = request.args.get('camera_id')
        if not camera_id:
            abort(404, description="Missing camera_id parameter.")
            
        data = {}
        match aspect:
            case 'velocity':
                velocity = predict_velocity(camera_id)
                
                data = {
                    'velocity': velocity,
                }
                
            case 'condition':
                # TODO
                pass
            
            case 'density':
                # TODO
                pass
            
            case _:
                abort(404, description="Invalid aspect parameter.")
                
        response = make_response(jsonify(data), 200)
        return response
    
    except Exception as e:
        abort(404, description=str(e))