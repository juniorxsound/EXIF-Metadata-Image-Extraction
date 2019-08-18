from flask import Flask, request, redirect, url_for, send_file, jsonify, Response
from dotenv import load_dotenv
from subprocess import PIPE, run, TimeoutExpired, CalledProcessError
from os import getenv, getcwd, listdir, path
from PIL import Image
from io import BytesIO
import base64
load_dotenv()

app = Flask(__name__)

'''
EXIFTool Rest API
-----------------
1) Endpoints:
- '/exif/json' - returns the exif metadata as JSON object (useful for debugging images)
- '/exif/xml' - returns the exif metadata as XML object (useful for debugging images)
- '/exif/depth/iphone' - returns a JPEG image with the depth map encoded by iPhones in portrait mode
- '/exif/depth/pixel' - returns a JPEG image with the depth map encoded by Pixels in portrait mode

2) Usage:
This API is used directly by the Electron frontend included, but you can run just the server and make requests to it independetly (port is defined in the .env file)
Call `make api` from the root directory of the project

Example request
curl -X GET \
  http://127.0.0.1:2912/exif/json \
  -H 'content-type: multipart/form-data;' \
  -F file=@/Path/to/samples/pixel_portait_ORIGINAL.jpg
'''

@app.route('/')
def index():
    return 'This is just another REST API, so nothing to see here', 400

'''
Return the EXIF metadata as JSON
'''
@app.route('/exif/json', methods=['GET', 'POST'])
def raw_exif_as_json():
    if request.json is None:
        return 'Oops, no image file provided in the request body', 400

    decoded_base64_img = base64.b64decode(request.get_json()['image'])

    try:
        result = run(
            ['exiftool', '-', '-j'],
            input=decoded_base64_img,
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    return Response(result.stdout.decode('utf-8'), mimetype='application/json'), 200

'''
Return the EXIF metadata as JSON
'''
@app.route('/exif/xml', methods=['GET', 'POST'])
def raw_exif_as_xml():
    if request.json is None:
        return 'Oops, no image file provided in the request body', 400

    decoded_base64_img = base64.b64decode(request.get_json()['image'])

    try:
        result = run(
            ['exiftool', '-', '-X'],
            input=decoded_base64_img,
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    return Response(result.stdout.decode('utf-8'), 'text/xml'), 200

'''
Returns a JPEG image with the depth map from iPhone portrait images
'''
@app.route('/exif/depth/iphone', methods=['GET', 'POST'])
def depthmap_from_iphone():
    if request.json is None:
        return 'Oops, no image file provided in the request body', 400

    decoded_base64_img = base64.b64decode(request.get_json()['image'])

    try:
        result = run(
            ['exiftool', '-', '-b', '-MPImage2'],
            input=decoded_base64_img,
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    encoded_base64_img = base64.b64encode(result.stdout).decode('utf-8')

    return jsonify({ 'image': 'data:image/jpeg;base64,' + encoded_base64_img}), 200

'''
Returns a JPEG image with the depth map from Pixel portrait images
'''
@app.route('/exif/depth/pixel', methods=['GET', 'POST'])
def depthmap_from_pixel():
    if request.json is None:
        return 'Oops, no image file provided in the request body', 400

    decoded_base64_img = base64.b64decode(request.get_json()['image'])

    try:
        result = run(
            ['exiftool', '-', '-b', '-Data'],
            input=decoded_base64_img,
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    encoded_base64_img = base64.b64encode(result.stdout).decode('utf-8')

    return jsonify({ 'image': 'data:image/jpeg;base64,' + encoded_base64_img}), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=getenv('PORT'))
