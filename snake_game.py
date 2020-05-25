"""
File: snake_game.py
----------------
The Goal of the game is to keep the snake alive without hitting the borders or crashing into itself.
My version of the snake game is with obstacles and a background picture
"""

import pygame
import random
import math
from simpleimage import SimpleImage

# Importing Image module from PIL package

from PIL import Image

N_ROWS = 6
N_COLS = 6
PATCH_SIZE = 111
WIDTH = N_COLS * PATCH_SIZE
HEIGHT = N_ROWS * PATCH_SIZE

PATCH_NAME = 'images/simba-sq1.jpg'
SCREEN_WIDTH = 600      # Width of screen in pixels
SCREEN_HEIGHT = 600     # Height of screen in pixels

SNAKE_SIZE = 25


# pass parameters for new coordinates
def draw_snake(screen, x, y):
    radius = 8
    color = 40, 113, 68

    # tried doing a rounded snake lol decided to work with this
    inside_rec = pygame.draw.rect(screen, color, [x, y, SNAKE_SIZE, SNAKE_SIZE])
    pygame.draw.rect(screen, color, inside_rec)

    # draw eyes
    radius = 4  # size
    circle_middle = (x + 20, y + 5)
    circle_middle2 = (x + 5, y + 5)
    pygame.draw.circle(screen, (254, 220, 0), circle_middle, radius)
    pygame.draw.circle(screen, (254, 220, 0), circle_middle2, radius)


def draw_snake_food(screen, x, y):
    snake_food_img = pygame.image.load('images/frog.png')
    screen.blit(snake_food_img, (x, y))


# using the distance formula to calculate how close both objects are
# D = Square root(x2 - x1)^2 + (y2 -y1)^2
def ate_food(snake_x, snake_y, snake_food_x, snake_food_y):
    distance = math.sqrt(math.pow(snake_x - snake_food_x, 2) +
                         (math.pow(snake_y - snake_food_y, 2)))
    if distance < 27:
        return True
    else:
        return False


def draw_new_body(screen, snake_list):
    color = 40, 113, 68
    for x in snake_list:
        pygame.draw.rect(screen, color, [x[0], x[1], SNAKE_SIZE, SNAKE_SIZE])

# def our_snake(screen, snake_block, snake_list):
#     for x in snake_list:
#         color = 40, 113, 68
#         pygame.draw.rect(screen, color, [x[0], x[1], snake_block, snake_block])


def place_patch(row, col, patch, final_image):
    for y in range(patch.height):
        for x in range(patch.width):
            pixel = patch.get_pixel(x, y)
            final_image.set_pixel(x, y, pixel)
            final_image.set_pixel(x + PATCH_SIZE * col, y + PATCH_SIZE * row, pixel)
    return final_image


def make_recolored_patch(red_scale, green_scale, blue_scale):
    """
    Implement this function to make a patch for the Warhol Filter. It
    loads the patch image and recolors it.
    :param red_scale: A number to multiply each pixels' red component by
    :param green_scale: A number to multiply each pixels' green component by
    :param blue_scale: A number to multiply each pixels' blue component by
    :return: the newly generated patch
    """
    patch = SimpleImage(PATCH_NAME)
    for pixel in patch:
        pixel.red *= red_scale
        pixel.green *= green_scale
        pixel.blue *= blue_scale
    # TODO: your code here.
    return patch


def show_score(screen, score, x, y):
    # font for text font name and size (www.dafint.com) for more fonts
    font = pygame.font.Font('freesansbold.ttf', 32)
    score = font.render("Score : " + str(score), True, (255, 255, 255))
    screen.blit(score, (x, y))


def main():

    # Background Image
    image = SimpleImage(PATCH_NAME)
    # image.show()
    final_image = SimpleImage.blank(WIDTH, HEIGHT)
    # TODO: your code here.
    # This is an example which should generate a pinkish patch
    for row in range(N_ROWS):
        for col in range(N_COLS):
            # The uniform() method returns a random floating number between the two specified numbers (both included).
            patch = make_recolored_patch(random.uniform(0, 0.5), random.uniform(0, 0.5), random.uniform(0, 0.5))
            place_patch(row, col, patch, final_image)
    # final_image.show()

    final_image.pil_image.save("images/newkarel.png")

    background_img = pygame.image.load('images/newkarel.png')

    # initialise pygame to access methods and functions
    # needed to run pygame
    pygame.init()

    # Create the window of the game
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Set Title, Icon and Background
    pygame.display.set_caption("Snake Game by Bridget")
    icon = pygame.image.load('images/snake.jpg')
    pygame.display.set_icon(icon)

    # Snake
    snake_x = 300
    snake_y = 480
    change_snake_x = 0
    change_snake_y = 0

    snake_food_x = random.randint(0, 536)
    snake_food_y = random.randint(50, 150)

    # score board
    score = 0

    game_running = True

    direction = "up"

    text_x = 10
    text_y = 10

    snake_list = []
    length_of_snake = 0

    clock = pygame.time.Clock()

    while game_running:
        # fill the background (R,G,B)
        screen.fill((10, 46, 54))

        # below the screen.fill so the image is infront.
        # loading of image in while loop slow downs the process
        screen.blit(background_img, (0, 0))

        # gets and checks all events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False

            # if keystroke is pressed check whether its right or left
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    change_snake_x = -5
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    change_snake_x = 5
                    direction = "right"
                elif event.key == pygame.K_UP:
                    change_snake_y = -5
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                    change_snake_y = 5

            # stop moving if player releases key
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or \
                        event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    change_snake_x = 0
                    change_snake_y = 0

        # Update Movement of Snake
        snake_x += change_snake_x
        snake_y += change_snake_y

        previous_x = snake_x
        previous_y = snake_y
        # ToDo Fix the extra issue with the wall

        # sets wall boundaries for all coners
        if snake_x <= 0 + 4:
            # left wall
            change_snake_x = 0 + 4

        elif snake_x >= SCREEN_WIDTH - SNAKE_SIZE - 10:
            # right wall
            change_snake_x = SCREEN_WIDTH - SNAKE_SIZE - 10
        elif snake_y <= 0 + 4:
            # top wall
            change_snake_y = 0 + 4
        elif snake_y >= SCREEN_HEIGHT - SNAKE_SIZE - 10:
            # bottom wall
            change_snake_y = SCREEN_HEIGHT - SNAKE_SIZE - 10

        # check to see the distance between the food and snake
        if ate_food(snake_x, snake_y, snake_food_x, snake_food_y):
            score += 1

            length_of_snake += 1

            for i in range(length_of_snake):
                if i == 0:
                    previous_x = snake_x - (SNAKE_SIZE * i)
                    previous_y = snake_y
                if direction == "left":
                    previous_x = snake_x + (SNAKE_SIZE * i)
                    previous_y = snake_y
                elif direction == "right":
                    previous_x = snake_x - (SNAKE_SIZE * i)
                    previous_y = snake_y
                elif direction == "up":
                    previous_x = snake_x
                    previous_y = snake_y + (SNAKE_SIZE * i)
                elif direction == "down":
                    previous_x = snake_x
                    previous_y = snake_y - (SNAKE_SIZE * i)

                # add to body part
                snake_body = []
                snake_body.append(previous_x)
                snake_body.append(previous_y)
                snake_list.append(snake_body)

            # To keep randomly change food position
            snake_food_x = random.randint(0, 536)
            snake_food_y = random.randint(50, 450)

        # add snake to background
        print(snake_list)
        draw_new_body(screen, snake_list)

        draw_snake(screen, snake_x, snake_y)
        print(snake_x, snake_y)

        # add snake food to background
        draw_snake_food(screen, snake_food_x, snake_food_y)

        # add  Score Board
        show_score(screen, score, text_x, text_y)

        # update game
        pygame.display.update()

        clock.tick(60)


if __name__ == '__main__':
    main()