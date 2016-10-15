import os
import time
import PIL.Image
import cups
import picamera
import RPi.GPIO as gpio
import pygame
from PIL import Image
from pygame.locals import *
from threading import Thread

# Imports from broken out functions
from UpdateDisplay import UpdateDisplay
from Pulse import pulse
from Print import Print

# initialise global variables
closeme = True  # Loop Control Variable
timepulse = 999  # Pulse Rate of LED
LEDon = False  # LED Flashing Control
gpio.setmode(gpio.BCM)  # Set GPIO to BCM Layout
Numeral = ""  # Numeral is the number display
Message = ""  # Message is a fullscreen message
SmallMessage = ""  # SmallMessage is a lower banner message
TotalImageCount = 1  # Counter for Display and to monitor paper usage
PhotosPerCart = 16  # Selphy takes 16 sheets per tray
background_template_location = "/home/pi/Desktop/template.jpg"

# initialise pygame
pygame.mixer.pre_init(44100, -16, 1, 1024 * 3)  # PreInit Music, plays faster
pygame.init()  # Initialise pygame
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)  # Full screen 640x480
background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert()  # Convert it to a background


# Main Thread
def main(threadName, *args):
    # Setup Variables
    gpio.setup(24, gpio.IN)  # Button on Pin 24 Reprints last image
    gpio.setup(22, gpio.IN)  # Button on Pin 22 is the shutter
    global closeme
    global timepulse
    global TotalImageCount
    global Numeral
    global SmallMessage
    global Message

    Message = "Loading..."
    UpdateDisplay(PhotosPerCart)
    time.sleep(5)  # 5 Second delay to allow USB to mount

    # Initialise the camera object
    camera = picamera.PiCamera()

    # Transparency allows pigame to shine through
    camera.preview_alpha = 120
    camera.vflip = False
    camera.hflip = True
    camera.rotation = 90
    camera.brightness = 45
    camera.exposure_compensation = 6
    camera.contrast = 8
    camera.resolution = (1280, 720)

    # Start the preview
    camera.start_preview()

    Message = "USB Check..."
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

    Message = "Initialise"

    UpdateDisplay(PhotosPerCart)

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

    Message = ""
    UpdateDisplay(PhotosPerCart)

    # Main Loop
    while closeme:
        try:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    closeme = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        closeme = False
        except KeyboardInterrupt:
            closeme = False

        # input_value is the shuttergp
        gpio.setup(22, gpio.IN)
        input_value = gpio.input(22)
        # input_value2 is photo reprint
        gpio.setup(24, gpio.IN)
        input_value2 = gpio.input(24)

    UpdateDisplay(PhotosPerCart)

    # Reprint Button has been pressed
    if input_value2 == False:
        # If the temp image exists send it to the printer
        if os.path.isfile('/home/pi/Desktop/tempprint.jpg'):
            # Open a connection to cups
            conn = cups.Connection()
            # get a list of printers
            printers = conn.getPrinters()
            # select printer 0
            printer_name = printers.keys()[0]
            Message = "Re-Print..."
            UpdateDisplay(PhotosPerCart)
            # print the buffer file
            printqueuelength = len(conn.getJobs())
            if printqueuelength > 1:
                Message = "PRINT ERROR"
                conn.enablePrinter(printer_name)
                UpdateDisplay(PhotosPerCart)
            elif printqueuelength == 1:
                SmallMessage = "Print Queue Full!"
                UpdateDisplay(PhotosPerCart)
                conn.enablePrinter(printer_name)
            conn.printFile(printer_name, '/home/pi/Desktop/tempprint.jpg', "PhotoBooth", {})
            time.sleep(20)
            Message = ""
            UpdateDisplay(PhotosPerCart)

    # input_value is the shutter release
    if input_value == False:
        subimagecounter = 0
    # Increment the image number
    imagecounter = imagecounter + 1

    # Initialise number of shots variable
    shotscountdown = 4
    #
    im = {}

    while shotscountdown > 0:
        # Initialise countdown variable to 5
        countdown = 5

        while countdown > 0:
            # Display the countdown number
            Numeral = countdown
            UpdateDisplay(PhotosPerCart)
            # Subtract 1 from countdown each increment
            countdown - 1
            # Flash the light at half second intervals
            timepulse = 0.5
            # Wait 1 second between beeps
            time.sleep(1)

        Numeral = ""
        Message = "Smile!"
        # Update display
        UpdateDisplay(PhotosPerCart)
        # increment the subimage
        subimagecounter = subimagecounter + 1
        # create the filename
        filename = 'image'
        filename += `imagecounter`
        filename += '_'
        filename += `subimagecounter`
        filename += '.jpg'
        # capture the image
        camera.capture(os.path.join(imagefolder, filename))
        # create an image object
        im[shotscountdown] = PIL.Image.open(os.path.join(imagefolder, filename)).transpose(Image.FLIP_LEFT_RIGHT)
        Message = "Get Ready"
        UpdateDisplay(PhotosPerCart)
        timepulse = 999
        time.sleep(3)

        Message = ""
        shotscountdown + 1


    # Load the background template
    bgimage = PIL.Image.open(background_template_location)
    # thumbnail the 4 images
    im[4].thumbnail((560, 400))
    im[3].thumbnail((560, 400))
    im[2].thumbnail((560, 400))
    im[1].thumbnail((560, 400))
    # paste the thumbnails to the background images
    bgimage.paste(im[4], (15, 20))
    bgimage.paste(im[3], (15, 410))
    bgimage.paste(im[2], (15, 820))
    bgimage.paste(im[1], (15, 1230))
    # two columns of 4
    bgimage.paste(im[4], (620, 20))
    bgimage.paste(im[3], (620, 410))
    bgimage.paste(im[2], (620, 820))
    bgimage.paste(im[1], (620, 1230))

    # Create the final filename
    final__image__name = os.path.join(imagefolder, "Final_" + `imagecounter` + ".jpg")
    # Save it to the usb drive
    bgimage.save(os.path.join(imagefolder, "Final_" + `imagecounter` + ".jpg"))
    # Save a temp file, its faster to print from the pi than usb
    bgimage.save('/tmp/tempprint.jpg')

    # Call print function to print photos
    Print(TotalImageCount, printer_name)
    # Clear message variable
    Message = ""
    # Update display
    UpdateDisplay(PhotosPerCart)
    # Set timepulse to 999
    timepulse = 999

    # Reset the shutter switch
    while input_value == False:
        input_value = gpio.input(22)
    # Stop preview
    camera.stop_preview()

    # Launch main thread
    Thread(target=main, args=('Main', 1)).start()
    # Launch pulse thread
    Thread(target=pulse, args=('Pulse', 1)).start()
    # Sleep for 5 seconds
    time.sleep(5)
