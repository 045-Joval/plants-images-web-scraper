from flask import Flask, request
import image_scraper
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/api/getimages", methods=["POST"])
def get_images():
    data = request.get_json()
    query = data['query']
    license_type = data['license_type']
    number_of_images = data['number_of_images']
    image_width = data['image_width']
    image_height = data['image_height']
    return_data = image_scraper.image_download(query, license_type, number_of_images, (image_width, image_height))
    return return_data, 200


if __name__ == "__main__":
    app.run(debug=True)