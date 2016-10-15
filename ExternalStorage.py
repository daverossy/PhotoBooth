def ExternalStorage():
    Message = "USB Check..."
    return Message
    UpdateDisplay(PhotosPerCart)

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
