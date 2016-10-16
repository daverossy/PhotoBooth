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

# Initialise pygame
pygame.mixer.pre_init(44100, -16, 1, 1024 * 3)  # PreInit Music, plays faster
pygame.init()  # Initialise pygame
screen = pygame.display.set_mode((800, 480), pygame.FULLSCREEN)  # Full screen 640x480
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
ExternalStorage.initialise()

# Set message to initialise
Message = "Initialise"

# Update display to reflect message
update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

# Procedure checks if a numerical folder exists, if it does pick the next number
# each start gets a new folder i.e. /photobooth/1/ etc
ExternalStorage.folder_check(imagefolder)

# Set message to empty
Message = ""

# Update display to reflect message
update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

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

# input_value is the shutter release
if input_value == False:
    subimagecounter = 0

imagecounter = 0

# Increment the image number
imagecounter + 1

# Initialise number of shots variable
shotscountdown = 4

# Define empty dictionary for image variable data
im = {}

# Keep running until number of shots left is 0
while shotscountdown > 0:
    # Initialise countdown variable to 5
    countdown = 5

    # Keep running until countdown for photo is 0
    while countdown > 0:
        # Display the countdown number
        Numeral = str(countdown)
        update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)
        # Subtract 1 from countdown each increment
        countdown - 1
        # Flash the light at half second intervals
        timepulse = 0.5
        # Wait 1 second between beeps
        time.sleep(1)

        Numeral = ""

        if shotscountdown == 5:
            Message = "First Photo!"
        elif shotscountdown == 4:
            Message = "Second Photo!"
        elif shotscountdown == 3:
            Message = "Third Photo!"
        elif shotscountdown == 2:
            Message = "Forth Photo!"
        elif shotscountdown == 1:
            Message = "Last Photo!"
        else:
            exit()

        # Update display
        update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

        # increment the subimage
        subimagecounter = subimagecounter + 1

        # create the filename
        filename = 'image'
        filename += `imagecounter`
        filename += '_'
        filename += `subimagecounter`
        filename += '.jpg'

        # Capture image
        Camera.capture(imagefolder, filename)

        # Add an image element to the dictionary
        im[shotscountdown] = PIL.Image.open(os.path.join(imagefolder, filename)).transpose(Image.FLIP_LEFT_RIGHT)

        # Set message to get ready
        Message = "Get Ready"

        # Update display to reflect new message
        update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

        # Set timepulse to 999
        timepulse = 999

        # Wait for 3 seconds
        time.sleep(3)

        # Set message to empty
        Message = ""

        # Minus 1 off the amount of shots left
        shotscountdown - 1

# Call image processing function and pass in dictionary containing all images
ImageProcessing(im, background_template_location, imagefolder, imagecounter)

# Call print function to print photos
Print(TotalImageCount)

# Clear message variable
Message = ""

# Update display
update_display(TotalImageCount, Numeral, Message, PhotosPerCart, screen, background, pygame)

# Set timepulse to 999
timepulse = 999

# Reset the shutter switch
while input_value == False:
    input_value = gpio.input(22)

# Stop preview
Camera.stop_preview()

# Launch main thread
Thread(target=main, args=('Main', 1)).start()

# Launch pulse thread
Thread(target=pulse, args=('Pulse', 1)).start()

# Sleep for 5 seconds
time.sleep(5)
