import pygame


# UpdateDisplay - Thread to update the display, neat generic procedure
def update_display(total_image_count, numeral, message, photos_per_cart, screen, background, pygame):
    small_text = "Rossy's Photobooth"  # Default Small Message Text

    if total_image_count >= (photos_per_cart - 2):  # Low Paper Warning at 2 images less
        small_text = "Paper Running Low!..."
    if total_image_count >= photos_per_cart:  # Paper out warning when over Photos per cart
        small_message = "Paper Out!..."
        total_image_count = 0

    background.fill(pygame.Color("black"))  # Black background
    smallfont = pygame.font.Font(None, 50)  # Small font for banner message
    small_text = smallfont.render(small_text, 1, (86, 40, 115))
    background.blit(small_text, (1200, 920))  # Write the small text
    small_text = smallfont.render(`total_image_count` + "/" + `photos_per_cart`, 1, (86, 40, 115))
    background.blit(small_text, (1710, 920))  # Write the image counter

    if message != "":  # If the big message exits write it
        font = pygame.font.Font(None, 180)
        text = font.render(message, 1, (86, 40, 115))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)
    elif numeral != "":  # Else if the number exists display it
        font = pygame.font.Font(None, 800)
        text = font.render(numeral, 1, (86, 40, 115))
        textpos = text.get_rect()
        textpos.centerx = background.get_rect().centerx
        textpos.centery = background.get_rect().centery
        background.blit(text, textpos)

    screen.blit(background, (0, 0))
    pygame.draw.rect(screen, pygame.Color(86, 40, 115), (10, 10, 1780, 980), 2)  # Draw the red outer box
    pygame.display.flip()

    return
