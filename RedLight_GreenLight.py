import pygame
from gpiozero import LED, Button, MotionSensor
from Vec2 import Vec2
from circle import Circle
from time import sleep
import random

screen = pygame.display.set_mode([800, 800])
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
objects = []

RED = LED(27) # Red bulb attached to GPIO pin 27
GREEN = LED(17) # Green bulb attached to GPIO pin 17
button = Button(2)

pir = MotionSensor(22)

'''
    Visual feedback for game beginning. LED's toggle every 0.75 seconds to represent a 3, 2, 1, go countdown
'''
def countdown():
    RED.on() # Get ready
    GREEN.on()
    sleep(3)

    for i in range(7, 0, -1):
        GREEN.toggle()
        RED.toggle()
        if i is 6:
            print("3")
        elif i is 4:
            print("2")
        elif i is 2:
            print("1")
        elif i is 0:
            print("GO")
        sleep(0.75)

'''
    Lights flicker back and forth as an idle when game is not running
'''
def idle_lights():
    GREEN.blink(1, 1)
    sleep(1)
    RED.blink(1, 1)


'''
    If player moves when light is red, move them back 50 pixels, or back to start if applicable
'''
def move_player(p):
    print("movement detected")
    if p.pos.y <= 550:
        p.pos.y += 50
    else:
        p.pos.y = 600

def main():
    # set up pygame and window
    pygame.init()
    bg_color = WHITE
    screen.fill(bg_color)

    # variables for determining if red/green light is on
    start_value = random.randrange(1, 10) # random determination if red or green starts
    if start_value % 2 == 0:
        green_on = True
        red_on = False
    else:
        green_on = False
        red_on = True

    change_light = True
    tot_seconds = 0 # start value

    # timer
    start_ticks = pygame.time.get_ticks()

    # player dot
    player = Circle(radius=20, color=(0, 50, 255), pos=Vec2(400, 600), mass=float('inf'))
    goal = Circle(radius = 20, color=(255, 0, 0), pos=Vec2(400, 100), mass=float('inf'))
    objects.append(player)
    objects.append(goal)

    # game loop
    running = True

    idle = True # set idle state to true initially

    # clock within pygame
    clock = pygame.time.Clock()
    fps = 60
    dt = 1/fps

    screen.fill(bg_color)
    for o in objects:
            o.update(dt)
            o.draw(screen)
    pygame.display.flip()

    idle_lights()
    pir.wait_for_motion()
    countdown()

    while running:
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        screen.fill(bg_color)

        if tot_seconds < seconds: # once we surpass the time limit for the light, set to true and swap lights
            change_light = True

        if change_light:
            num_seconds = random.randrange(3, 10) # random duration between 3 and 10 seconds for each light
            tot_seconds = seconds + num_seconds # number to reach before
            print("wait for: ", num_seconds)
            print("target time: ", tot_seconds)
            print("green: ", green_on)
            print("red: ", red_on)
            if green_on: # if green light is on, turn it off and turn red on
                GREEN.off()
                RED.on()
                green_on = False
                red_on = True
            else:
                GREEN.on()
                RED.off()
                red_on = False
                green_on = True
            change_light = False # don't go in this if statement while we're counting


        #if pir.motion_detected:
         #   print("motion")
        #else:
         #   print("no motion")

        for o in objects:
            o.update(dt)
            o.draw(screen)

        if button.is_pressed:
            player.pos.y -= 1

        if green_on and pir.motion_detected:
            player.pos.y -= 1

        if red_on and pir.motion_detected:
            move_player(player)


        distanceFromGoal = player.pos - goal.pos
        if distanceFromGoal.mag() < 39:
            print("You win!")
            running = False


        for e in pygame.event.get():
            # user clicks closed button
            if e.type == pygame.QUIT:
                running = False

        pygame.display.flip()
        clock.tick(fps) / 1000
    RED.off()
    GREEN.off()
    pygame.quit()

try:
    main()
except Exception:
    RED.off()
    GREEN.off()
    pygame.quit()
    raise