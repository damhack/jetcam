from .camera import Camera
import atexit
import cv2
import numpy as np
import threading
import traitlets


class MJPEGCamera(Camera):
    
    capture_location = traitlets.String(default_value="127.0.0.1:8080/stream")
    capture_fps = traitlets.Integer(default_value=30)
    capture_width = traitlets.Integer(default_value=640)
    capture_height = traitlets.Integer(default_value=480)
    
    
    def __init__(self, *args, **kwargs):
        super(MJPEGCamera, self).__init__(*args, **kwargs)
        try:
            self.cap = cv2.VideoCapture(self._gst_str(), cv2.CAP_GSTREAMER)

            re, image = self.cap.read()

            if not re:
                raise RuntimeError('Could not read image from camera.')
        except:
            raise RuntimeError(
                'Could not initialize camera.  Please see error trace.')

        atexit.register(self.cap.release)
                
    def _gst_str(self):
        return 'souphttpsrc location=%s do-timestamp=true is_live=true ! multipartdemux ! jpegdec ! videorate ! videoscale ! video/x-raw, width=(int)%d, height=(int)%d, framerate=(fraction)%d/1 ! videoconvert ! video/x-raw, format=BGR ! appsink' % (
                "http://" + self.capture_location, self.capture_width, self.capture_height, self.capture_fps)

    
    def _read(self):
        re, image = self.cap.read()
        if re:
            return image
        else:
            raise RuntimeError('Could not read image from camera')
