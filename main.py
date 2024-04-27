import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import random
import tkinter as tk
from tkinter import messagebox
import time
import webbrowser
import subprocess

pygame.init()

#
#SirPigariStudios
#

def read_settings_from_file(filename):
    settings = {}
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            if line:
                parts = line.split('=')
                if len(parts) == 2:
                    key, value = parts
                    settings[key.strip()] = value.strip()
                else:
                    print(f"Ignoring invalid line in settings file: {line}")
    return settings


def secretkey(filename):
    key_dict = {}
    with open(filename, 'r') as file:
        for line in file:
            if 'SECRET_KEY6' in line:
                line = line.strip()
                if line:
                    key_value = line.split('=')
                    if len(key_value) == 2:
                        key_dict[key_value[0].strip()] = key_value[1].strip()

    return key_dict



settings = read_settings_from_file('settings.txt')
key = secretkey('secretkey.txt')

SECRET_KEY = str(key.get('SECRET_KEY6'))
WIDTH = int(settings.get('WIDTH', 800))
HEIGHT = int(settings.get('HEIGHT', 600))
RESOLUTION = tuple(map(int, settings.get('RESOLUTION', '0,0').split(',')))
BUTTON_WIDTH1 = int(settings.get('BUTTON_WIDTH1', 100))
BUTTON_HEIGHT1 = int(settings.get('BUTTON_HEIGHT1', 50))
BUTTON_MARGIN = int(settings.get('BUTTON_MARGIN', 20))
BLACK = tuple(map(int, settings.get('BLACK', '0,0,0').split(',')))
WHITE = tuple(map(int, settings.get('WHITE', '255,255,255').split(',')))
RED = tuple(map(int, settings.get('RED', '255,0,0').split(',')))
GRAY = tuple(map(int, settings.get('GRAY', '63,63,63').split(',')))
PADDLE_WIDTH = int(settings.get('PADDLE_WIDTH', 10))
PADDLE_HEIGHT = int(settings.get('PADDLE_HEIGHT', 100))
BALL_SIZE = int(settings.get('BALL_SIZE', 20))
PADDLE_SPEED = int(settings.get('PADDLE_SPEED', 5))
BALL_SPEED_X = int(settings.get('BALL_SPEED_X', 4))
BALL_SPEED_Y = int(settings.get('BALL_SPEED_Y', 4))
DEVELOPER_MODE = str(settings.get('DEVELOPER_MODE'))
BOT_MISTAKE_PROBABILITY = float(settings.get('BOT_MISTAKE_PROBABILITY', 0.25))
FPS = int(settings.get('FPS', 60))
SLIDER_WIDTH = int(settings.get('SLIDER_WIDTH', 400))
SLIDER_HEIGHT = int(settings.get('SLIDER_HEIGHT', 20))
SLIDER_COLOR = tuple(map(int, settings.get('SLIDER_COLOR', '100,100,100').split(',')))
SLIDER_BUTTON_COLOR = tuple(map(int, settings.get('SLIDER_BUTTON_COLOR', '150,150,150').split(',')))
SLIDER_BUTTON_RADIUS = int(settings.get('SLIDER_BUTTON_RADIUS', 10))
SLIDER_MIN_VALUE = int(settings.get('SLIDER_MIN_VALUE', 10))
SLIDER_MAX_VALUE = int(settings.get('SLIDER_MAX_VALUE', 120))
DEFAULT_FPS = int(settings.get('DEFAULT_FPS', 60))
PLAYER_A = str(settings.get('PLAYER_A'))
PLAYER_B = str(settings.get('PLAYER_B'))
PLAYER_A_SCORE = int(settings.get('PLAYER_A_SCORE', 0))
PLAYER_B_SCORE = int(settings.get('PLAYER_B_SCORE', 0))
SOUNDS = int(settings.get('SOUNDS', 0))
HIGH_SCORE = int(settings.get('HIGH_SCORE', 0))

if SECRET_KEY == 'Zw^K$J&7#%:a2(fhE<kuyRtsF_8d>brGP;~{C.N35me+vg,AB4':
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong v2.0")

    paddle_sound = pygame.mixer.Sound("pong paddle.wav")
    wall_sound = pygame.mixer.Sound("pong wall.wav")
    score_sound = pygame.mixer.Sound("pong score.wav")
    main_sound = pygame.mixer.Sound("main_sounds.wav")

    paddle_sound.set_volume(0.5)
    wall_sound.set_volume(0.5)
    score_sound.set_volume(0.2)
    main_sound.set_volume(0.1)

    main_sound_playing = False

    sound_enabled_img = pygame.image.load("musicOff.png").convert_alpha()
    sound_disabled_img = pygame.image.load("musicOn.png").convert_alpha()

    yt = "www.youtube.com/@SirPigari"
    pong = "https://www.ponggame.org/"

    reset_yes = False
    select_menu_text = 'Do you want to reset your highscore?'


    class Paddle:
        def __init__(self, x, y):
            self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)

        def draw(self):
            pygame.draw.rect(screen, WHITE, self.rect)

        def move(self, direction):
            if direction == "up" and self.rect.top > 0:
                self.rect.y -= PADDLE_SPEED
            elif direction == "down" and self.rect.bottom < HEIGHT:
                self.rect.y += PADDLE_SPEED


    class Ball:
        def __init__(self):
            self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
            self.direction_x = random.choice([-1, 1])
            self.direction_y = random.choice([-1, 1])

        def draw(self):
            pygame.draw.rect(screen, WHITE, self.rect)

        def move(self):
            self.rect.x += BALL_SPEED_X * self.direction_x
            self.rect.y += BALL_SPEED_Y * self.direction_y

        def bounce(self):
            if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(opponent_paddle.rect):
                self.direction_x *= -1
                if SOUNDS == 1:
                    paddle_sound.play()

            if self.rect.y <= 0 or self.rect.y >= HEIGHT - BALL_SIZE:
                self.direction_y *= -1
                if SOUNDS == 1:
                    wall_sound.play()

            if self.rect.x <= 0:
                return "player_b_score"
            elif self.rect.x >= WIDTH:
                return "player_a_score"


    player_paddle = Paddle(WIDTH - 20, HEIGHT // 2 - PADDLE_HEIGHT // 2)
    opponent_paddle = Paddle(10, HEIGHT // 2 - PADDLE_HEIGHT // 2)

    ball = Ball()

    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 56)
    small_font = pygame.font.Font(None, 16)


    def draw_text(text, color, x, y):
        text_surface = font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_big_text(text, color, x, y):
        text_surface = big_font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_small_text(text, color, x, y):
        text_surface = small_font.render(text, True, color)
        screen.blit(text_surface, (x, y))

    def draw_slider(x, y, selected_value):
        pygame.draw.rect(screen, SLIDER_COLOR, (x, y, SLIDER_WIDTH, SLIDER_HEIGHT))
        button_x = (selected_value - SLIDER_MIN_VALUE) / (SLIDER_MAX_VALUE - SLIDER_MIN_VALUE) * SLIDER_WIDTH
        pygame.draw.circle(screen, SLIDER_BUTTON_COLOR, (int(x + button_x), int(y + SLIDER_HEIGHT / 2)),
                           SLIDER_BUTTON_RADIUS)


    def select_menu():
        global reset_yes
        global select_menu_text

        screen1 = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Select Menu")

        label_text = select_menu_text
        yes_text = "Yes"
        no_text = "No"

        label_surface = font.render(label_text, True, WHITE)
        yes_surface = font.render(yes_text, True, WHITE)
        no_surface = font.render(no_text, True, WHITE)

        yes_rect = pygame.Rect((WIDTH - BUTTON_WIDTH1) // 2 - BUTTON_WIDTH1 - BUTTON_MARGIN, HEIGHT // 2,
                               BUTTON_WIDTH1, BUTTON_HEIGHT1)
        no_rect = pygame.Rect((WIDTH - BUTTON_WIDTH1) // 2 + BUTTON_MARGIN, HEIGHT // 2, BUTTON_WIDTH1,
                              BUTTON_HEIGHT1)

        screen1.blit(label_surface, ((WIDTH - label_surface.get_width()) // 2, HEIGHT // 4))
        pygame.draw.rect(screen1, BLACK, yes_rect)
        pygame.draw.rect(screen1, BLACK, no_rect)
        screen1.blit(yes_surface,
                     ((WIDTH - yes_surface.get_width()) // 2 - BUTTON_WIDTH1 - BUTTON_MARGIN, HEIGHT // 2 + 10))
        screen1.blit(no_surface, ((WIDTH - no_surface.get_width()) // 2 + BUTTON_MARGIN, HEIGHT // 2 + 10))

        true = True
        while true:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_pos = pygame.mouse.get_pos()
                        if yes_rect.collidepoint(mouse_pos):
                            reset_yes = True
                            return
                        elif no_rect.collidepoint(mouse_pos):
                            reset_yes = False
                            return

            pygame.display.flip()


    def open_text_file(filename1):
        try:
            subprocess.Popen(['xdg-open', filename1])
        except OSError:
            try:
                subprocess.Popen(['open', filename1])
            except OSError:
                subprocess.Popen(['start', '', filename1], shell=True)


    def singleplayer_game():
        global HIGH_SCORE
        pygame.display.set_caption("Pong v2.0 (singleplayer)")
        bot_score = PLAYER_A_SCORE
        player_score = PLAYER_B_SCORE
        player_paddle.rect.centery = HEIGHT // 2
        opponent_paddle.rect.centery = HEIGHT // 2
        ball = Ball()
        paused = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused
                    elif DEVELOPER_MODE == 'True':
                        if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                            player_score += 1
                        elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                            player_score -= 1
                        elif event.key == pygame.K_KP0:
                            bot_score -= 1
                        elif event.key == pygame.K_KP1:
                            bot_score += 1

            if paused:
                draw_big_text("Paused", WHITE, WIDTH // 2 - 60, HEIGHT // 2 - 50)
                quit_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 50, 100, 50)
                pygame.draw.rect(screen, BLACK, quit_button)
                draw_text("Quit", WHITE, WIDTH // 2 - 25, HEIGHT // 2 + 65)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_menu()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if quit_button.collidepoint(mouse_pos):
                            main_menu()
                        else:
                            paused = False
                continue

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                player_paddle.move("up")
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                player_paddle.move("down")

            if ball.rect.y < opponent_paddle.rect.y and random.random() > BOT_MISTAKE_PROBABILITY:
                opponent_paddle.move("up")
            elif ball.rect.y > opponent_paddle.rect.y and random.random() > BOT_MISTAKE_PROBABILITY:
                opponent_paddle.move("down")

            ball.move()

            result = ball.bounce()
            if result == "player_b_score":
                if SOUNDS == 1:
                    score_sound.play()
                player_score += 1
                ball = Ball()
            elif result == "player_a_score":
                if SOUNDS == 1:
                    score_sound.play()
                bot_score += 1
                ball = Ball()

            if player_score > HIGH_SCORE:
                HIGH_SCORE = player_score
                with open('settings.txt', 'r+') as file:
                    lines = file.readlines()
                    file.seek(0)
                    for line in lines:
                        if 'HIGH_SCORE' in line:
                            file.write(f'HIGH_SCORE={HIGH_SCORE}\n')
                        else:
                            file.write(line)
                    file.truncate()

            screen.fill(BLACK)

            player_paddle.draw()
            opponent_paddle.draw()
            ball.draw()

            draw_text("Bot: " + str(bot_score), WHITE, 10, 10)
            draw_text("Player: " + str(player_score), WHITE, WIDTH - 150, 10)
            draw_text("Your high Score: " + str(HIGH_SCORE), WHITE, 10, 50)

            pygame.display.flip()

            pygame.time.Clock().tick(FPS)


    def multiplayer_game():
        pygame.display.set_caption("Pong v2.0 (multiplayer)")
        player_a_score = PLAYER_A_SCORE
        player_b_score = PLAYER_B_SCORE
        player_paddle.rect.centery = HEIGHT // 2
        opponent_paddle.rect.centery = HEIGHT // 2
        ball = Ball()
        paused = False
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        paused = not paused

            if paused:
                draw_big_text("Paused", WHITE, WIDTH // 2 - 60, HEIGHT // 2 - 50)
                quit_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 + 80, 100, 50)
                pygame.draw.rect(screen, BLACK, quit_button)
                draw_text("Quit", WHITE, WIDTH // 2 - 25, HEIGHT // 2 + 80)
                pygame.display.flip()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        main_menu()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        mouse_pos = event.pos
                        if quit_button.collidepoint(mouse_pos):
                            main_menu()
                        else:
                            paused = False
                continue

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player_paddle.move("up")
            if keys[pygame.K_DOWN]:
                player_paddle.move("down")
            if keys[pygame.K_w]:
                opponent_paddle.move("up")
            if keys[pygame.K_s]:
                opponent_paddle.move("down")

            ball.move()

            result = ball.bounce()
            if result == "player_b_score":
                if SOUNDS == 1:
                    score_sound.play()
                player_b_score += 1
                ball = Ball()
            elif result == "player_a_score":
                if SOUNDS == 1:
                    score_sound.play()
                player_a_score += 1
                ball = Ball()


            screen.fill(BLACK)

            player_paddle.draw()
            opponent_paddle.draw()
            ball.draw()

            draw_text(PLAYER_A + ': ' + str(player_a_score), WHITE, 10, 10)
            draw_text(PLAYER_B + ': ' + str(player_b_score), WHITE, WIDTH - 150, 10)

            pygame.display.flip()

            pygame.time.Clock().tick(FPS)


    def main_menu():
        global FPS
        pygame.display.set_caption("Pong v2.0")
        while True:
            screen.fill(BLACK)
            draw_big_text("Pong", WHITE, WIDTH // 2 - 40, HEIGHT // 2 - 100)
            singleplayer_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
            multiplayer_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
            settings_button = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
            pygame.draw.rect(screen, BLACK, singleplayer_button)
            pygame.draw.rect(screen, BLACK, multiplayer_button)
            pygame.draw.rect(screen, BLACK, settings_button)
            draw_text("Singleplayer", WHITE, WIDTH // 2 - 75, HEIGHT // 2 - 25)
            draw_text("Multiplayer", WHITE, WIDTH // 2 - 65, HEIGHT // 2 + 75)
            draw_text("Settings", WHITE, WIDTH // 2 - 40, HEIGHT // 2 + 175)
            quit_button = pygame.Rect(WIDTH // 2 - 5, HEIGHT // 2 + 235, 30, 15)
            yt_button = pygame.Rect(WIDTH // 2 + 280, HEIGHT // 2 + 275, 120, 20)
            pong_button = pygame.Rect(WIDTH // 2 - 395, HEIGHT // 2 + 275, 52, 20)
            pygame.draw.rect(screen, BLACK, quit_button)
            draw_small_text("Quit", RED, WIDTH // 2 - 5, HEIGHT // 2 + 235)
            pygame.draw.rect(screen, BLACK, yt_button)
            pygame.draw.rect(screen, BLACK, pong_button)
            draw_small_text("Pong v2.0", GRAY, WIDTH // 2 - 395, HEIGHT // 2 + 280)
            draw_small_text("© SirPigari Studio", GRAY, WIDTH // 2 + 280, HEIGHT // 2 + 280)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = event.pos
                    if singleplayer_button.collidepoint(mouse_pos):
                        singleplayer_game()
                    elif multiplayer_button.collidepoint(mouse_pos):
                        multiplayer_game()
                    elif settings_button.collidepoint(mouse_pos):
                        FPS = settings_menu(FPS)
                    elif yt_button.collidepoint(mouse_pos):
                        print('SirPigari Studio')
                        webbrowser.open(yt)
                    elif pong_button.collidepoint(mouse_pos):
                        print('Pong')
                        webbrowser.open(pong)
                    elif quit_button.collidepoint(mouse_pos):
                        pygame.display.set_caption("Pong v2.0 (quiting)")
                        print('Game quit in:')
                        print('3')
                        time.sleep(1)
                        print('2')
                        time.sleep(1)
                        print('1')
                        time.sleep(1)
                        pygame.quit()


    def settings_menu(current_fps):
        global select_menu_text
        global reset_yes
        global main_sound
        global sound_enabled_img
        global sound_disabled_img
        global SOUNDS
        global DEFAULT_FPS
        global HIGH_SCORE
        global main_sound_playing
        global filename1
        pygame.display.set_caption("Pong v2.0 (settings)")
        filename1 = 'settings.txt'
        running = True
        selected_value = current_fps
        slider_dragging = False
        while running:
            screen.fill(BLACK)
            draw_big_text("Settings", WHITE, WIDTH // 2 - 65, HEIGHT // 2 - 100)
            draw_text("FPS:", WHITE, WIDTH//4, HEIGHT//2)
            draw_text(str(selected_value), WHITE, 3 * WIDTH//4, HEIGHT//2)
            draw_slider(WIDTH//4, HEIGHT//2 + 50, selected_value)
            back_button = pygame.Rect(WIDTH//2 - 50, HEIGHT - 100, 100, 50)
            reset_button = pygame.Rect(90, HEIGHT - 550, 50, 25)
            reset_settings_button = pygame.Rect(200, 380, 150, 15)
            open_settings_button = pygame.Rect(200, 395, 150, 15)
            pygame.draw.rect(screen, BLACK, back_button)
            draw_text("Back", WHITE, WIDTH//2 - 25, HEIGHT - 85)
            draw_text("Your highscore: " + str(HIGH_SCORE), WHITE, 10, 10)
            pygame.draw.rect(screen, BLACK, reset_button)
            draw_small_text("RESET ", WHITE, 90, 50)
            pygame.draw.rect(screen, BLACK, reset_settings_button)
            button_width = 50
            button_height = 50
            sound_enabled_img = pygame.transform.scale(sound_enabled_img, (button_width, button_height))
            sound_disabled_img = pygame.transform.scale(sound_disabled_img, (button_width, button_height))
            pygame.draw.rect(screen, BLACK, open_settings_button)
            draw_small_text("Reset settings to default ", WHITE, 200, 380)
            draw_small_text("Open settings file ", WHITE, 200, 395)
            enable_sound_button = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 110, sound_enabled_img.get_width(), sound_enabled_img.get_height())
            if SOUNDS == 2:
                if not main_sound_playing:
                    main_sound.play()
                    main_sound_playing = True
            elif SOUNDS == 0:
                if main_sound_playing:
                    main_sound.stop()
                    main_sound_playing = False
            elif SOUNDS == 2 and not main_sound_playing:
                main_sound.play()
                main_sound_playing = True

            if SOUNDS == 1:
                screen.blit(sound_enabled_img, enable_sound_button)
            else:
                screen.blit(sound_disabled_img, enable_sound_button)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        mouse_x, mouse_y = event.pos
                        if WIDTH//4 <= mouse_x <= WIDTH//4 + SLIDER_WIDTH and HEIGHT//2 + 50 <= mouse_y <= HEIGHT//2 + 50 + SLIDER_HEIGHT:
                            slider_dragging = True
                        elif back_button.collidepoint((mouse_x, mouse_y)):
                            running = False
                            pygame.display.set_caption("Pong v2.0")
                        elif open_settings_button.collidepoint((mouse_x, mouse_y)):
                            select_menu_text = 'Do you want to open settings file?'
                            select_menu()
                            if reset_yes == True:
                                pygame.display.set_caption("Pong v2.0")
                                open_text_file(filename1)
                            else:
                                pygame.display.set_caption("Pong v2.0")
                                print('Access denied')
                        elif reset_button.collidepoint((mouse_x, mouse_y)):
                            select_menu_text = 'Do you want to reset your highscore?'
                            select_menu()
                            if reset_yes == True:
                                pygame.display.set_caption("Pong v2.0")
                                with open('settings.txt', 'r+') as file:
                                    lines = file.readlines()
                                    file.seek(0)
                                    for line in lines:
                                        if 'HIGH_SCORE=' in line:
                                            file.write('HIGH_SCORE=0\n')
                                        else:
                                            file.write(line)
                                    file.truncate()
                                HIGH_SCORE = 0
                                draw_text("Your high Score: " + str(HIGH_SCORE), WHITE, 10, 10)
                                pygame.display.flip()
                                reset_yes = False
                            else:
                                pygame.display.set_caption("Pong v2.0")
                                reset_yes = False
                                print('Access denied')
                        elif enable_sound_button.collidepoint((mouse_x, mouse_y)):
                            if SOUNDS == 1:
                                with open('settings.txt', 'r+') as file:
                                    lines = file.readlines()
                                    file.seek(0)
                                    for line in lines:
                                        if 'SOUNDS=' in line:
                                            file.write('SOUNDS=0\n')
                                        else:
                                            file.write(line)
                                    file.truncate()
                                    SOUNDS = 0
                                pygame.display.flip()
                            else:
                                with open('settings.txt', 'r+') as file:
                                    lines = file.readlines()
                                    file.seek(0)
                                    for line in lines:
                                        if 'SOUNDS=' in line:
                                            file.write('SOUNDS=1\n')
                                        else:
                                            file.write(line)
                                    file.truncate()
                                    SOUNDS = 1
                                pygame.display.flip()
                        elif reset_settings_button.collidepoint((mouse_x, mouse_y)):
                            select_menu_text = 'Do you want to reset settings? (dangerous)'
                            select_menu()
                            if reset_yes:
                                pygame.display.set_caption("Pong v2.0")
                                with open('settings.txt', 'r+') as file:
                                    lines = file.readlines()
                                    file.seek(0)
                                    for line in lines:
                                        if 'WIDTH=' in line:
                                            file.write('WIDTH=800\n')
                                        if 'HEIGHT=' in line:
                                            file.write('HEIGHT=600\n')
                                        if 'BUTTON_WIDTH1=' in line:
                                            file.write('BUTTON_WIDTH1=100\n')
                                        if 'BUTTON_HEIGHT1=' in line:
                                            file.write('BUTTON_HEIGHT1=50\n')
                                        if 'BUTTON_MARGIN=' in line:
                                            file.write('BUTTON_MARGIN=20\n')
                                        if 'BLACK=' in line:
                                            file.write('BLACK=0,0,0\n')
                                        if 'WHITE=' in line:
                                            file.write('WHITE=255,255,255\n')
                                        if 'RED=' in line:
                                            file.write('RED=255,0,0\n')
                                        if 'GRAY=' in line:
                                            file.write('GRAY=63,63,63\n')
                                        if 'PADDLE_WIDTH=' in line:
                                            file.write('PADDLE_WIDTH=10\n')
                                        if 'PADDLE_HEIGHT=' in line:
                                            file.write('PADDLE_HEIGHT=100\n')
                                        if 'BALL_SIZE=' in line:
                                            file.write('BALL_SIZE=20\n')
                                        if 'PADDLE_SPEED=' in line:
                                            file.write('PADDLE_SPEED=5\n')
                                        if 'BALL_SPEED_X=' in line:
                                            file.write('BALL_SPEED_X=4\n')
                                        if 'BALL_SPEED_Y=' in line:
                                            file.write('BALL_SPEED_Y=4\n')
                                        if 'BOT_MISTAKE_PROBABILITY=' in line:
                                            file.write('BOT_MISTAKE_PROBABILITY=0.25\n')
                                        if 'FPS=' in line:
                                            file.write('FPS=60\n')
                                        if 'SLIDER_WIDTH=' in line:
                                            file.write('SLIDER_WIDTH=400\n')
                                        if 'SLIDER_HEIGHT=' in line:
                                            file.write('SLIDER_HEIGHT=20\n')
                                        if 'SLIDER_COLOR=' in line:
                                            file.write('SLIDER_COLOR=100,100,100\n')
                                        if 'SLIDER_BUTTON_COLOR=' in line:
                                            file.write('SLIDER_BUTTON_COLOR=150,150,150\n')
                                        if 'SLIDER_BUTTON_RADIUS=' in line:
                                            file.write('SLIDER_BUTTON_RADIUS=10\n')
                                        if 'SLIDER_MIN_VALUE=' in line:
                                            file.write('SLIDER_MIN_VALUE=10\n')
                                        if 'SLIDER_MAX_VALUE=' in line:
                                            file.write('SLIDER_MAX_VALUE=120\n')
                                        if 'DEFAULT_FPS=' in line:
                                            file.write('DEFAULT_FPS=60\n')
                                        if 'PLAYER_A=' in line:
                                            file.write('PLAYER_A=Player A\n')
                                        if 'PLAYER_B=' in line:
                                            file.write('PLAYER_B=Player B\n')
                                        if 'PLAYER_A_SCORE=' in line:
                                            file.write('PLAYER_A_SCORE=0\n')
                                        if 'PLAYER_B_SCORE=0' in line:
                                            file.write('\n')
                                        if 'HIGH_SCORE=' in line:
                                            continue
                                        reset_yes = False
                                    else:
                                        pygame.display.set_caption("Pong v2.0")
                                        reset_yes = False
                                        file.write(line)
                                        file.truncate()
                            else:
                                pygame.display.set_caption("Pong v2.0")
                                print('Access denied')
                                print('')
                                print('If you want to reset your settings go to your folder of this game and copy file settings_save.txt and paste it for settings_save - copy.txt and then copy that copy file and go to game folder and pase it here (delete old settings before doing this) and rename it to settings.txt (also reset high score)')
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:
                        slider_dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if slider_dragging:
                        mouse_x, _ = event.pos
                        selected_value = int((mouse_x - WIDTH//4) / SLIDER_WIDTH * (SLIDER_MAX_VALUE - SLIDER_MIN_VALUE) + SLIDER_MIN_VALUE)
                        selected_value = max(SLIDER_MIN_VALUE, min(selected_value, SLIDER_MAX_VALUE))
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        running = False
                else:
                    command = str(input(' '))
                    if command == '/yt':
                        webbrowser.open(yt)
                    else:
                        print('Unknown command')


        return selected_value


    main_menu()



else:
    window = tk.Tk()
    window.title("Error")
    window.geometry("210x25")
    label = tk.Label(window, text="Dont steal games you fucking bastard!")
    label.pack()
    messagebox.showerror("Error", "Invalid key")
    window.mainloop()
    window.destroy()