from rest_framework import status, views
from rest_framework.response import Response
import cv2
import numpy as np
import base64
import subprocess
import shutil
import time

class AIGenerateViews(views.APIView):
    def post(self, request):
        # must get encoded_data. not decoded data. may..be..?
        encoded_image = request.data.get('file')
        ts = str(time.time())
        encoded_image.save(f'static/input/{ts}.png')
        # make subprocess in docker container have to option that "--cap-add=SYS_PRACTICE"
        # it processes video in static/output/{ts}/video.gif
        # if subprocess makes error in docker -> then just run image_to_animation function

        p = subprocess.run(["python3.8", "../animated_drawing/AnimatedDrawings-main/examples/image_to_animation.py",
                            f'static/input/{ts}.png', f'static/output/{ts}'])
        # remove used file.

        return Response(status=status.HTTP_200_OK)
