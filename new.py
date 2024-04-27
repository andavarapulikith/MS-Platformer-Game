import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 400
screen_height = 200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Username Prompt")

# Set up colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Set up fonts
font = pygame.font.Font(None, 32)

def draw_text(surface, text, color, x, y):
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))

def main():
    running = True
    username = ""

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    running = False
                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += event.unicode

        # Clear the screen
        screen.fill(WHITE)

        # Draw the prompt
        draw_text(screen, "Enter your username:", BLACK, 50, 50)
        draw_text(screen, username, BLACK, 50, 100)

        # Update the display
        pygame.display.flip()

    pygame.quit()
    return username

if __name__ == "__main__":
    username = main()
    print("Username entered:", username)
