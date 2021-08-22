from flask import request, jsonify
from router.route import app
from utils import image_to_text


@app.route('/convert-image-to-text', methods=("POST",))
def img2text():
    if "image" in request.files:
        img = request.files['image']
        response = image_to_text.ImageToText(path=img).convert()
        return jsonify({"text": response}), 200
    return jsonify({"text": "Something went wrong.."}), 400
