from flask import Flask, request
import image_scraper

app = Flask(__name__)


@app.route("/api/getimages", methods=["POST"])
def get_images():
    data = request.get_json()
    name = data['name']
    image_scraper.image_download(name)
    return "Success", 200


if __name__ == "__main__":
    app.run(debug=True)
