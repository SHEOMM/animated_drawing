import subprocess

from flask import *
import time

from examples.image_to_animation import image_to_animation

app = Flask(__name__)


@app.route('/', method=['POST'])
def index():
    param = request.get_json()
    encoded_image = param['file']
    ts = str(time.time())
    encoded_image.save(f'static/input/{ts}.png')
    # make subprocess in docker container have to option that "--cap-add=SYS_PRACTICE"
    # it processes video in static/output/{ts}/video.gif
    # if subprocess makes error in docker -> then just run image_to_animation function
    p = subprocess.run(["python3.8", "../animated_drawing/AnimatedDrawings-main/examples/image_to_animation.py",
                        f'static/input/{ts}.png', f'static/output/{ts}'])

    image_to_animation(f'static/input/{ts}.png', f'static/output/{ts}')

