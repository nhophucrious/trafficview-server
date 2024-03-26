import base64
import requests
from PIL import Image
from io import BytesIO
from app.constants.crawler import CRAWLER_AUTH_ENDPOINT_GT, CRAWLER_AUTH_HEADER_GT, CRAWLER_IMAGE_ENDPOINT_GT, CRAWLER_IMAGE_HEADER_GT
import matplotlib.pyplot as plt
from app.model.condition_model import Model as ConditionModel
from app.model.density_model import Model as DensityModel
from app.model.velocity_model import Model as VelocityModel
    

def get_image_and_predictions(camera_id):
    response = requests.get(url=CRAWLER_AUTH_ENDPOINT_GT, headers=CRAWLER_AUTH_HEADER_GT)
    cookies = response.cookies

    image_endpoint = CRAWLER_IMAGE_ENDPOINT_GT + camera_id
    image_response = requests.get(
        url=image_endpoint,
        headers=CRAWLER_IMAGE_HEADER_GT,
        cookies=cookies
    )

    # Check if the response is an image
    if image_response.status_code == 200 and 'image' in image_response.headers['Content-Type']:
        image_bytes = BytesIO(image_response.content)
        image = Image.open(image_bytes).convert("RGB")

        img_byte_array = BytesIO()
        
        # add prediction here
        image_for_models = image.copy()

        velocity_model = VelocityModel()
        velocity = velocity_model.predict_from_bytes(image_for_models)

        condition_model = ConditionModel()
        condition = condition_model.predict_from_bytes(image_for_models)

        density_model = DensityModel()
        density = density_model.predict_from_bytes(image_for_models)

        image.save(img_byte_array, format="JPEG")
        
        img_byte_array.seek(0)
        img_byte_array_png = base64.b64encode(img_byte_array.getvalue())
        
        data_url = "data:image/jpeg;base64," + img_byte_array_png.decode('utf-8')
        # print(data_url)
        return {
            "image": data_url,
            "velocity": str(velocity),
            "condition": str(condition),
            "density": str(density)
        }
    else:
        return "IMAGE NOT AVAILABLE"

def predict_velocity_condition_density(camera):
    pass