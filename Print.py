import cups
import UpdateDisplay


def initial_print(total_image_count):
    # Connect to cups and select printer 0
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = printers.keys()[0]

    # Increment the large image counter
    total_image_count = total_image_count + 1
    return total_image_count
    # Update message
    message = "Print..."
    return message
    UpdateDisplay.update_display()
    # Print the file
    printqueuelength = len(conn.getJobs())
    # If multiple prints in the queue error
    if printqueuelength > 1:
        message = "PRINT ERROR"
        return message
        conn.enablePrinter(printer_name)
        UpdateDisplay.update_display()
    elif printqueuelength == 1:
        small_message = "Print Queue Full!"
        return small_message
        conn.enablePrinter(printer_name)
        UpdateDisplay.update_display()

    conn.printFile(printer_name, '/tmp/tempprint.jpg', "PhotoBooth", {})
    time.sleep(20)


def reprint():
    # Open a connection to cups
    conn = cups.Connection()
    # get a list of printers
    printers = conn.getPrinters()
    # select printer 0
    printer_name = printers.keys()[0]
    message = "Re-Print..."
    UpdateDisplay.update_display()
    # print the buffer file
    printqueuelength = len(conn.getJobs())
    if printqueuelength > 1:
        message = "PRINT ERROR"
        conn.enablePrinter(printer_name)
        UpdateDisplay.update_display()
    elif printqueuelength == 1:
        small_message = "Print Queue Full!"
        UpdateDisplay.update_display()
        conn.enablePrinter(printer_name)
    conn.printFile(printer_name, '/home/pi/Desktop/tempprint.jpg', "PhotoBooth", {})

    return
