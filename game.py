"""
Create a grid with rows and colums
"""

import pygame

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

pygame.init()

# Set the width and height of the screen [width, height]
size = (512, 512)
screen = pygame.display.set_mode(size)

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

width = 20
height = 20
margin = 5
# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.fill(BLACK)

    # --- Drawing code should go here
    # for column (that is along the x axis) in range (0 = starting position,     100=number to go up to, width+margin =step by (increment by this number)
    # adding the 255 makes it fill the entire row, as 255 is the size of the screen (both ways)
    for column in range(0 + margin, 255, width + margin):
        pygame.draw.rect(screen, WHITE, [column, 0 + margin, width, height])
        for row in range(0 + margin, 255, width + margin):
            pygame.draw.rect(screen, WHITE, [0 + margin, row, width, height])
        # This simply draws a white rectangle to position (column)0,(row)0 and of size width(20), height(20) to the screen

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()