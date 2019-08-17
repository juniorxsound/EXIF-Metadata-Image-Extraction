from flask import Flask, request, redirect, url_for, send_file
from dotenv import load_dotenv
from subprocess import PIPE, run, TimeoutExpired, CalledProcessError
from os import getenv, getcwd, listdir, path
from PIL import Image
from io import BytesIO
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
@app.route('/exif/json', methods=['GET'])
def raw_exif_as_json():
    if 'file' not in request.files:
        return 'Oops, no image file provided in the request body', 400

    try:
        result = run(
            ['exiftool', '-', '-j'],
            input=request.files['file'].read(),
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    return send_file(BytesIO(result.stdout), mimetype='application/json')

'''
Return the EXIF metadata as JSON
'''
@app.route('/exif/json', methods=['GET'])
def raw_exif_as_json():
    if 'file' not in request.files:
        return 'Oops, no image file provided in the request body', 400

    try:
        result = run(
            ['exiftool', '-', '-X'],
            input=request.files['file'].read(),
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    return send_file(BytesIO(result.stdout), mimetype='text/xml')

'''
Returns a JPEG image with the depth map from iPhone portrait images
'''
@app.route('/exif/depth/iphone', methods=['GET'])
def depthmap_from_iphone():
    if 'file' not in request.files:
        return 'Oops, no image file provided in the request body', 400

    try:
        result = run(
            ['exiftool', '-', '-b', '-MPImage2'],
            input=request.files['file'].read(),
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    return send_file(BytesIO(result.stdout), mimetype='image/jpeg')

'''
Returns a JPEG image with the depth map from Pixel portrait images
'''
@app.route('/exif/depth/pixel', methods=['GET'])
def depthmap_from_pixel():
    if 'file' not in request.files:
        return 'Oops, no image file provided in the request body', 400

    try:
        result = run(
            ['exiftool', '-', '-b', '-Data'],
            input=request.files['file'].read(),
            check=True,
            stdout=PIPE,
            timeout=10,
        )
    except TimeoutExpired:
        return 'Sorry, the server timed out', 408
    except CalledProcessError:
        return 'Sorry, the server had a weird issue out', 500

    return send_file(BytesIO(result.stdout), mimetype='image/jpeg')


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=getenv('PORT'))
