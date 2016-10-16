import os
from UpdateDisplay import update_display


def initialise():
    Message = "USB Check..."
    return Message
    update_display(PhotosPerCart)

    # Following is a check to see there is a USB mounted if not it loops with a USB message
    usbcheck = False
    rootdir = '/media/'

    while not usbcheck:
        dirs = os.listdir(rootdir)
        for file in dirs:
            folder = os.path.join(rootdir, file)
            if not file == 'SETTINGS' and os.path.isdir(folder):
                usbcheck = True
                imagedrive = os.path.join(rootdir, file)
                imagefolder = os.path.join(imagedrive, 'PhotoBooth')
                # If a photobooth folder on the usb doesn't exist create it
                if not os.path.isdir(imagefolder):
                    os.makedirs(imagefolder)

    return


def folder_check():
    # Procedure checks if a numerical folder exists, if it does pick the next number
    # each start gets a new folder i.e. /photobooth/1/ etc
    notfound = True
    folderno = 1
    while notfound:
        tmppath = os.path.join(imagefolder, `folderno`)
        if not os.path.isdir(tmppath):
            os.makedirs(tmppath)
            imagefolder = tmppath
            notfound = False
        else:
            folderno = folderno + 1

    imagecounter = 0

    return
