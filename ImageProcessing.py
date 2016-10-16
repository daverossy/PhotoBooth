import PIL
import os


def image_processing(im, background_template_location, imagefolder, imagecounter):
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

    return
