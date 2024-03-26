from .predict_route import predict_blueprint
from .image_route import image_blueprint
from .image_with_predictions_route import image_with_predictions_blueprint

def register_route(app):
    app.register_blueprint(predict_blueprint)
    app.register_blueprint(image_blueprint)
    app.register_blueprint(image_with_predictions_blueprint)