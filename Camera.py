import picamera


def InitialiseCamera():
    # Initialise the camera object
    global camera = picamera.PiCamera()

    # Transparency allows pigame to shine through
    camera.preview_alpha = 120
    camera.vflip = False
    camera.hflip = True
    camera.rotation = 90
    camera.brightness = 45
    camera.exposure_compensation = 6
    camera.contrast = 8
    camera.resolution = (1280, 720)
    return


def StartPreview():
    # Stop Preview
    camera.start_preview()
    return


def StopPreview():
    # Stop preview
    camera.stop_preview()
    return


def Capture(imagefolder, filename):
    camera.capture(os.path.join(imagefolder, filename))
    return
