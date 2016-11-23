import os
import time
import PIL.Image
import RPi.GPIO as gpio
import pygame
from PIL import Image
from pygame.locals import *
from threading import Thread

# Imports from broken out functions
from UpdateDisplay import update_display
from Pulse import pulse
import Print
import ExternalStorage
import ImageProcessing
import Camera

# Initialise global variables
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
imagefolder = ""
imagedriver = ""
usbcheck = True
subimagecounter = 0

# Initialise pygame
pygame.init()  # Initialise pygame
screen = pygame.display.set_mode((1800, 1000), pygame.FULLSCREEN)  # Full screen 640x480
background = pygame.Surface(screen.get_size())  # Create the background object
background = background.convert()  # Convert it to a background


# Main Thread
def main(threadName, *args):
    # Setup GPIO pins
    gpio.setup(24, gpio.IN)  # Button on Pin 24 Reprints last image
    gpio.setup(22, gpio.IN)  # Button on Pin 22 is the shutter

    # Setup global variables
    global closeme
    global timepulse
    global TotalImageCount
    global Numeral
    global SmallMessage
    global Message

    subimagecounter = 0

    # Update message to loading
    Message = "Loading..."

    # Update display to reflect message
    update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

    # 5 Second delay to allow USB to mount
    time.sleep(5)

    # Call camera initialisation function
    Camera.initialise_camera()

    # Start camera preview
    Camera.start_preview()

    # Initialise the external storage
    Message, usbcheck, rootdir, imagedrive, imagefolder = ExternalStorage.initialise()

    # Set message to initialise
    Message = "Initialise"

    # Update display to reflect message
    update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

    # Procedure checks if a numerical folder exists, if it does pick the next number
    # each start gets a new folder i.e. /photobooth/1/ etc
    imagefolder = ExternalStorage.folder_check(imagefolder)

    # Set message to empty
    Message = ""

    # Update display to reflect message
    update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

    closeme = True

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

        # Update display to reflect changes
        update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

        # Reprint Button has been pressed
        if input_value2 == False:
            # If the temp image exists send it to the printer
            if os.path.isfile('/home/pi/Desktop/tempprint.jpg'):
                # Call reprint function
                Print.reprint()
                # Wait 20 seconds
                time.sleep(20)
                # Set message to empty
                Message = ""
                # Update display to reflect changes
                update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

        # Clear message variable
        Message = "Press button to start!"

        # Update display
        update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

        # Set timepulse to 999
        timepulse = 999

        # Set start button to false
        input_value = False

        # Reset the shutter switch
        while input_value == False:
            input_value = gpio.input(22)

        # input_value is the shutter release
        if input_value == False:
            subimagecounter = 0

        imagecounter = 0

        # Increment the image number
        imagecounter + 1

        # Define empty dictionary for image variable data
        im = {}

        # Keep running until number of shots taken is 5
        for shotscountdown in range(1, 6):
            if shotscountdown == 1:
                Message = "First Photo!"
            elif shotscountdown == 2:
                Message = "Second Photo!"
            elif shotscountdown == 3:
                Message = "Third Photo!"
            elif shotscountdown == 4:
                Message = "Fourth Photo!"
            elif shotscountdown == 5:
                Message = "Last Photo!"
            else:
                exit()

            # Update display
            update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

            # Wait for 1 second
            time.sleep(1)

            # Set message to be empty
            Message = ""

            # Keep running until countdown for photo is 0
            for countdown in range(5, 0, -1):
                # Display the countdown number
                Numeral = str(countdown)
                update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)
                # Flash the light at half second intervals
                timepulse = 0.5
                # Wait 1 second between beeps
                time.sleep(1)
                Numeral = ""

            # increment the subimage
            subimagecounter = subimagecounter + 1

            # create the filename
            filename = 'image'
            filename += `imagecounter`
            filename += '_'
            filename += `subimagecounter`
            filename += '.jpg'

            # Set message to get ready
            Message = "Get Ready!"

            # Update display to reflect new message
            update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

            # Wait for 2 seconds
            time.sleep(1)

            # Capture image
            Camera.capture(imagefolder, filename)

            # Add an image element to the dictionary
            im[shotscountdown] = PIL.Image.open(os.path.join(imagefolder, filename)).transpose(Image.FLIP_LEFT_RIGHT)

            # Set timepulse to 999
            timepulse = 999

            # Set message to empty
            Message = ""

        # Call image processing function and pass in dictionary containing all images
        ImageProcessing.image_processing(im, background_template_location, imagefolder, imagecounter)

        # Call print function to print photos
        # Print function not required for this project so commented out
        # Print(TotalImageCount)

        # Set message variable
        Message = "All Done!"

        # Update display
        update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

        time.sleep(2)

        # Set message variable
        Message = "Check the Hub for Photos!"

        # Update display
        update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

        time.sleep(5)

    # Stop preview
    Camera.stop_preview()

    pygame.quit()

# Launch main thread
Thread(target=main, args=('Main', 1)).start()

# Launch pulse thread
# Thread(target=pulse, args=('Pulse', 1)).start()

# Sleep for 5 seconds
time.sleep(5)
