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
        encoded_image.save(ts + '.png')
        # make subprocess in docker container have to option that "--cap-add=SYS_PRACTICE"
        # it processes video in static/{ts}/video.gif
        p = subprocess.run(["python3.8", "image_to_animation.py", "{ts}.png", 'static/{ts}'])


        return Response(status=status.HTTP_200_OK)
