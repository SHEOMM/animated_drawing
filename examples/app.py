import base64
import os
import boto3
import time

from examples.image_to_animation import image_to_animation
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
from PIL import Image
from io import BytesIO
from flask import *

app = Flask(__name__)


@app.route('/', methods=['POST'])
def index():
    param = request.get_json()

    ts = str(time.time())
    remove_list = []
    response_dict = {}
    image = Image.open(BytesIO(base64.b64decode(param['file'])))
    image.save(f'static/input/{ts}.png', "PNG")

    # make subprocess in docker container have to option that "--cap-add=SYS_PRACTICE"
    # it processes video in static/output/{ts}/video.gif
    # if subprocess makes error in docker -> then just run image_to_animation function
    # p = subprocess.run(["python3.8", "../animated_drawing/AnimatedDrawings-main/examples/image_to_animation.py",
    #                     f'static/input/{ts}.png', f'static/output/{ts}'])

    remove_list.append(f'static/input/{ts}.png')
    s3_client = S3_CLIENT

    motion_list = ["dab", "jumping", "wave_hello", "jesse_dance"]

    for motion in motion_list:
        remove_list.append(upload_to_s3(s3_client, motion, ts))

    for remove in remove_list:
        os.remove(remove)

    image_url = "https://little-studio.s3.amazonaws.com"

    for motion in motion_list:
        response_dict[motion] = f"{image_url}/drawings/{motion}/{ts}"

    for remove in remove_list:
        os.remove(remove)

    return make_response(jsonify(response_dict), 200)


def upload_to_s3(s3_client, motion: str, ts: str):
    image_to_animation(f'static/input/{ts}.png', f'static/output/{ts}/{motion}', f'config/motion/{motion}.yaml'
                       , 'config/retarget/fair1_ppf.yaml')
    s3_url = f"drawings/{motion}/{ts}"
    ai_generated_image = f'static/output/{ts}/{motion}/movie.gif'
    gif = open(ai_generated_image, mode='r')
    s3_client.upload_fileobj(gif.read(), 'little-studio', s3_url)
    return ai_generated_image


S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
