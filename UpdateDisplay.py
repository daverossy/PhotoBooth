# UpdateDisplay - Thread to update the display, neat generic procedure
def UpdateDisplay():
    # init global variables from main thread
    global Numeral
    global Message
    global SmallMessage
    global TotalImageCount
    global screen
    global background
    global pygame

    SmallText = "Rossy's Photobooth"  # Default Small Message Text

    if (TotalImageCount >= (PhotosPerCart - 2)):  # Low Paper Warning at 2 images less
        SmallText = "Paper Running Low!..."
    if (TotalImageCount >= PhotosPerCart):  # Paper out warning when over Photos per cart
        SmallMessage = "Paper Out!..."
        TotalImageCount = 0

    background.fill(pygame.Color("black"))  # Black background
    smallfont = pygame.font.Font(None, 50)  # Small font for banner message
    SmallText = smallfont.render(SmallText, 1, (255, 0, 0))
    background.blit(SmallText, (10, 445))  # Write the small text
    SmallText = smallfont.render(`TotalImageCount` + "/" + `PhotosPerCart`, 1, (255, 0, 0))
    background.blit(SmallText, (710, 445))  # Write the image counter

    if (Message != ""):  # If the big message exits write it
        font = pygame.font.Font(None, 180)
        text = font.render(Message, 1, (255, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)
    elif (Numeral != ""):  # Else if the number exists display it
        font = pygame.font.Font(None, 800)
        text = font.render(Numeral, 1, (255, 0, 0))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, pygame.Color("red"), (10, 10, 770, 430), 2)  # Draw the red outer box
    pygame.display.flip()

    return
