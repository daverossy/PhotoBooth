import datetime
import os
import time
import RPi.GPIO as gpio
import cups
import picamera
import pygame
import threading


class PhotoBooth(threading.Thread):
    gpio.setmode(gpio.BCM)  # Set GPIO to BCM Layout
    gpio.setup(22, gpio.IN)  # Setup start button
    gpio.setup(24, gpio.OUT)  # Setup start button
    pygame.init()
    count = 0
    folder_path = ''
    light_on = True
    camera = picamera.PiCamera()
    camera.preview_alpha = 120
    camera.vflip = False
    camera.hflip = True
    camera.rotation = 90
    camera.brightness = 45
    camera.resolution = (1280, 720)
    interrupt = False
    run = True

    @staticmethod
    def interface(mode):
        if mode == 'stop':
            pygame.quit()

    def messages(self, font, message):
        self.background.fill(pygame.Color("black"))  # Black background
        large_font = pygame.font.Font(None, 800)
        small_font = pygame.font.Font(None, 180)
        if font == 'large':
            text = large_font.render(message, 1, (255, 255, 255))
        elif font == 'small':
            text = small_font.render(message, 1, (255, 255, 255))
        else:
            text = small_font.render(message, 1, (255, 255, 255))
        text_pos = text.get_rect()
        text_pos.centerx = self.background.get_rect().centerx
        text_pos.centery = self.background.get_rect().centery
        self.background.blit(text, text_pos)

        self.screen.blit(self.background, (0, 0))
        pygame.draw.rect(self.screen, pygame.Color(255, 255, 255), (10, 10, 1780, 980), 2)  # Draw the red outer box
        pygame.display.flip()

    def storage(self, mode):
        if mode == 'initialise':
            root_dir = '/media/'
            dirs = os.listdir(root_dir)
            print(dirs)
        elif mode == 'folder_path':
            folder_path = 'something'
            self.folder_path = folder_path

    def camera(self, mode):
        if mode == 'start':
            self.camera.start_preview()
        elif mode == 'stop':
            self.camera.stop_preview()
        else:
            exit()

    def light(self):
        while self.light_on:
            gpio.output(24, gpio.HIGH)
            time.sleep(1)
            gpio.output(24, gpio.LOW)
            time.sleep(1)

    def button(self):
        while not gpio.input(22, gpio.IN):
            self.light_on = True
        self.light_on = False
        return True

    def counter(self):
        if self.count >= 5:
            self.count = 0
        self.count = self.count + 1

    def countdown(self):
        for countdown in range(5, 0, -1):
            self.messages('small', str(countdown))
            time.sleep(1)

    def photo_count(self):
        if self.counter == 1:
            self.messages('small', 'First Photo!')
        elif self.counter == 2:
            self.messages('small', 'Second Photo!')
        elif self.counter == 3:
            self.messages('small', 'Last Photo!')
        else:
            self.messages('small', 'Unknown photo number.')

    @staticmethod
    def filename():
        ts = time.time()
        filename = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
        return filename

    def take_photo(self):
        filename = self.filename()
        folder = self.folder_path
        self.camera.capture(os.path.join(folder, filename))

    @staticmethod
    def image_processing():
        print('collage')

    def print_photo(self):
        conn = cups.Connection()
        printers = conn.getPrinters()
        printer_name = printers.keys()[0]
        self.messages('small', 'Printing...')
        print_queue_length = len(conn.getJobs())
        if print_queue_length > 1:
            self.messages('small', 'Print error.')
            conn.enablePrinter(printer_name)
        elif print_queue_length == 1:
            self.messages('small', 'Print Queue Full!')
            conn.enablePrinter(printer_name)
        conn.printFile(printer_name, '/tmp/temp_print.jpg', "PhotoBooth", {})
        time.sleep(20)

    def check_interrupt(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self.interrupt = False
            elif event.key == pygame.K_ESCAPE:
                self.interrupt = False
            else:
                self.interrupt = True

    def main(self):
        self.storage(mode='initialise')
        while self.run:
            self.screen = pygame.display.set_mode((1800, 1000), pygame.FULLSCREEN)  # Full screen 1800x1000
            self.background = pygame.Surface(self.screen.get_size())  # Create the background object
            self.background = self.background.convert()  # Convert it to a background
            self.light_thread = threading.Thread(target=self.light())
            self.light_thread.daemon = True
            self.light_thread.start()
            self.camera_thread = threading.Thread(target=self.camera(mode='start'))
            self.camera_thread.daemon = True
            self.camera_thread.start()
            self.check_interrupt()
            if not self.interrupt:
                self.run = False
                self.interface(mode='stop')
            elif self.interrupt:
                self.run = True
                self.messages('small', 'Press button to start!')
                if self.button():
                    while self.count < 5:
                        self.counter()
                        self.photo_count()
                        self.countdown()
                        self.take_photo()
                        if self.count > 5:
                            self.messages('small', 'All Done!')


session = PhotoBooth()
session.main()
