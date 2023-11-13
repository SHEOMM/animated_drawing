import subprocess

import boto3
from flask import *
import time

from examples.image_to_animation import image_to_animation
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY

app = Flask(__name__)


@app.route('', methods=['POST'])
def index():
    param = request.get_json()
    encoded_image = param['file']
    ts = str(time.time())

    # make subprocess in docker container have to option that "--cap-add=SYS_PRACTICE"
    # it processes video in static/output/{ts}/video.gif
    # if subprocess makes error in docker -> then just run image_to_animation function
    # p = subprocess.run(["python3.8", "../animated_drawing/AnimatedDrawings-main/examples/image_to_animation.py",
    #                     f'static/input/{ts}.png', f'static/output/{ts}'])

    encoded_image.save(f'static/input/{ts}.png')
    s3_client = S3_CLIENT
    # dab
    image_to_animation(f'static/input/{ts}.png', f'static/output/{ts}/dab', 'config/motion/dab.yaml'
                       , 'config/retarget/fair1_ppf.yaml')
    dab_url = f"drawings/dab/{ts}"

    dab = open(f'static/output/{ts}/dab/movie.gif', mode='r')
    s3_client.upload_fileobj(dab.read(), 'little-studio', dab_url)

    # jumping
    image_to_animation(f'static/input/{ts}.png', f'static/output/{ts}/jumping', 'config/motion/jumping.yaml'
                       , 'config/retarget/fair1_ppf.yaml')
    jump_url = f"drawings/jump/{ts}"

    jump = open(f'static/output/{ts}/jumping/movie.gif', mode='r')
    s3_client.upload_fileobj(jump.read(), 'little-studio', jump_url)

    # wave_hello
    image_to_animation(f'static/input/{ts}.png', f'static/output/{ts}/wave_hello', 'config/motion/wave_hello.yaml'
                       , 'config/retarget/fair1_ppf.yaml')
    wave_hello_url = f"drawings/wave_hello/{ts}"

    wave_hello = open(f'static/output/{ts}/wave_hello/movie.gif', mode='r')
    s3_client.upload_fileobj(wave_hello.read(), 'little-studio', wave_hello_url)
    # jesse_dance
    image_to_animation(f'static/input/{ts}.png', f'static/output/{ts}/jesse_dance', 'config/motion/jesse_dance.yaml'
                       , 'config/retarget/fair1_ppf.yaml')

    jesse_dance_url = f"drawings/jesse_dance/{ts}"

    jesse_dance = open(f'static/output/{ts}/jesse_dance/movie.gif', mode='r')
    s3_client.upload_fileobj(jesse_dance.read(), 'little-studio', jesse_dance_url)
    image_url = "https://little-studio.s3.amazonaws.com/"
    data = {'dab': image_url + dab_url, 'jump': image_url + jump_url, 'wave_hello': image_url + wave_hello_url,
            'jesse_dance': image_url+jesse_dance_url}

    return make_response(jsonify(data), 200)



S3_CLIENT = boto3.client(
    's3',
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)
