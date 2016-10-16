import cups
import UpdateDisplay


def Print(TotalImageCount):
    # Connect to cups and select printer 0
    conn = cups.Connection()
    printers = conn.getPrinters()
    printer_name = printers.keys()[0]

    # Increment the large image counter
    TotalImageCount = TotalImageCount + 1
    return TotalImageCount
    # Update message
    Message = "Print..."
    return Message
    UpdateDisplay()
    # Print the file
    printqueuelength = len(conn.getJobs())
    # If multiple prints in the queue error
    if printqueuelength > 1:
        Message = "PRINT ERROR"
        return Message
        conn.enablePrinter(printer_name)
        UpdateDisplay()
    elif printqueuelength == 1:
        SmallMessage = "Print Queue Full!"
        return SmallMessage
        conn.enablePrinter(printer_name)
        UpdateDisplay()

    conn.printFile(printer_name, '/tmp/tempprint.jpg', "PhotoBooth", {})
    time.sleep(20)


def Reprint():
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
