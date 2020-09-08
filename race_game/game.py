import pygame
import time
import random
from constants import d, s, sp, display_width, display_height, black, white, gray, title, red, green, buttons, car_image


def circle(circle_x, circle_y, color, size=20):
    pygame.draw.circle(game_display, color, [circle_x, circle_y], size)

def quitgame():
    pygame.quit()
    quit()

def statistics(count, caught, special):
    font = pygame.font.SysFont(None, 25)
    text = font.render(f"Dodged: {count}, Score: {caught}, Special: {special}", True, black)
    game_display.blit(text,(0,0))

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(game_display, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(game_display, ic,(x,y,w,h))


    smallText = pygame.font.Font("freesansbold.ttf",20)
    textSurf, textRect = text_objects(msg, smallText)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    game_display.blit(textSurf, textRect)

def objects(objectsx, objectsy, objectsw, objectsh, color):
    pygame.draw.rect(game_display, color, [objectsx, objectsy, objectsw, objectsh])

def car(x, y):
    game_display.blit(car_image,(x, y))

def text_objects(text, font):
    text_surface = font.render(text, True, title)
    return text_surface, text_surface.get_rect()

def message_display(text, size=115):
    large_text = pygame.font.Font('freesansbold.ttf',size)
    text_surf, text_rect = text_objects(text, large_text)
    text_rect.center = ((display_width/2),(display_height/2))
    game_display.blit(text_surf, text_rect)
    pygame.display.update()
    time.sleep(2)
    game_loop()

def crash():
    message_display('GAME OVER')


pygame.init()

game_display = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Ride or Die')


clock = pygame.time.Clock()


def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        game_display.fill(gray)
        largeText = pygame.font.Font('freesansbold.ttf', 115)
        TextSurf, TextRect = text_objects("Ride or Die ", largeText)
        TextRect.center = ((display_width / 2), (display_height - 725))
        game_display.blit(TextSurf, TextRect)

        largeText2 = pygame.font.Font('freesansbold.ttf', 55)
        TextSurf2, TextRect2 = text_objects(f"Best Scores: ", largeText2)
        TextRect2.center = ((display_width / 2 - 400), (display_height - 550))
        game_display.blit(TextSurf2, TextRect2)

        largeText3 = pygame.font.Font('freesansbold.ttf', 35)
        TextSurf3, TextRect3 = text_objects(f'Dodged: {d["score"]}, Scored: {s["score"]} , Special:{sp["score"]}', largeText3)
        TextRect3.center = ((display_width / 2 - 250), (display_height - 430))
        game_display.blit(TextSurf3, TextRect3)

        button('Play', 950, 200, 200, 100, buttons, black, game_loop)
        button('Quit', 950, 350, 200, 100, buttons, black, quitgame)


        pygame.display.update()
        clock.tick(15)


def game_loop():
    x = 425
    y = 600
    game_over = False
    x_change = 0
    y_change = 0
    dodged = 0
    caught = 0
    special_count = 0
    car_speed = 4
    bonus = False
    special = False

    circle_x = 500
    circle_y = 350
    object_startx = random.randrange(0, 1000)
    object_starty = -800
    object_speed = 3
    object_width = 100
    object_height = 100

    while not game_over:

        for event in pygame.event.get():

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_intro()

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -car_speed
                elif event.key == pygame.K_RIGHT:
                    x_change = car_speed
                elif event.key == pygame.K_UP:
                    y_change = -car_speed
                elif event.key== pygame.K_DOWN:
                    y_change = car_speed


        x += x_change
        y += y_change

        if (x < 0 or x > display_width - 60) or (y < 0 or y > display_height - 60):
            crash()


        game_display.fill(gray)

        objects(object_startx, object_starty, object_width, object_height, black)
        if bonus:
            circle(circle_x, circle_y, green, size=20)
            special = True
        else:
            bonus = False
            circle(circle_x, circle_y, red)
        object_starty += object_speed
        car(x, y)
        statistics(dodged, caught, special_count)

        if x > display_width - 60 or x < 0:
            crash()

        if object_starty > display_height:
            object_starty = 0 - object_height
            object_startx = random.randrange(0, 1000)
            dodged += 1
            if dodged % 5 == 0 :
                object_speed += 1
                car_speed += 1
                object_width += (dodged * 1.5)
                object_height += (dodged * 1.5)

        if y > object_starty and y < object_starty + object_height or y  > object_starty and y  < object_starty + object_height:

            if x > object_startx and x < object_startx + object_width or x + 60 > object_startx and x + 60 < object_startx + object_width:
                crash()


        if circle_x - 40  <= x <= circle_x  and circle_y - 60 <= y <= circle_y:

            if special == True:
                special_count +=1
                special = False

            if caught  % 5 == 0 and caught != 0:
                caught += 2
                bonus = True
            else:
                caught += 1
                bonus = False
            circle_x = random.randrange(25, 850)
            circle_y = random.randrange(25, 600)

        if dodged > d['score']:
            d['score'] = dodged

        if caught > s['score']:
            s['score'] = caught

        if special_count > sp['score']:
            sp['score'] = special_count


        pygame.display.update()
        clock.tick(60)

game_intro()
game_loop()
pygame.quit()
quit()




