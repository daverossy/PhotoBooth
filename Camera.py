import picamera
import os

global camera
# Initialise the camera object
camera = picamera.PiCamera()


def initialise_camera():
    # Transparency allows pigame to shine through
    camera.preview_alpha = 120
    camera.vflip = False
    camera.hflip = True
    camera.rotation = 90
    # camera.brightness = 45
    # camera.exposure_compensation = 6
    # camera.contrast = 8
    camera.resolution = (1280, 720)
    camera.exposure_mode = 'antishake'
    # camera.image_effect = ''
    camera.led = False
    camera.video_stabilization = True
    return


def start_preview():
    # Stop Preview
    camera.start_preview()
    return


def stop_preview():
    # Stop preview
    camera.stop_preview()
    return


def capture(imagefolder, filename):
    camera.capture(os.path.join(imagefolder, filename))
    return
