import base64
import requests
from PIL import Image
from io import BytesIO
from app.constants.crawler import CRAWLER_AUTH_ENDPOINT_GT, CRAWLER_AUTH_HEADER_GT, CRAWLER_IMAGE_ENDPOINT_GT, CRAWLER_IMAGE_HEADER_GT
import matplotlib.pyplot as plt
from flask import Response

def get_image_url(camera_id):
    response = requests.get(url=CRAWLER_AUTH_ENDPOINT_GT, headers=CRAWLER_AUTH_HEADER_GT)
    cookies = response.cookies

    image_endpoint = CRAWLER_IMAGE_ENDPOINT_GT + camera_id +'?h=244&w=326'
    print(image_endpoint)
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
        
        image.save(img_byte_array, format="JPEG")
        
        img_byte_array.seek(0)
        img_byte_array_png = base64.b64encode(img_byte_array.getvalue())
        
        data_url = "data:image/jpeg;base64," + img_byte_array_png.decode('utf-8')
        # print(data_url)
        return data_url
        # image_bytes = BytesIO(image_response.content)
        # return Response(image_bytes, mimetype='image/jpeg')
    else:
        return "IMAGE NOT AVAILABLE"