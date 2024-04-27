import os
import pygame
from os import listdir
from os.path import isfile, join
from assets.map_one import MAP_ONE
from assets.map_two import MAP_TWO
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import simpledialog
from tkinter import ttk




def get_username():
    root = tk.Tk()
    root.withdraw()  
    dialog = tk.Toplevel(root)
    dialog.title("Username")
    dialog.geometry("400x200")  
    image_pil = Image.open("C:/Users/likit/Downloads/Python-Platformer-main (1)/Python-Platformer-main/assets/Background/frontpage3.jpg")
    # Convert the PIL image to a Tkinter-compatible format
    background_image = ImageTk.PhotoImage(image_pil)
    # Add a label to display the background image
    background_label = tk.Label(dialog, image=background_image)
    background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Expand the label to cover the entire dialog
    # Ensure the background image stays visible
    background_label.image = background_image
    # Add widgets to the dialog box
    label = ttk.Label(dialog, text="Enter your username:", font=("Arial", 14), background="white")  # Increase font size and set background color
    label.pack(pady=20)  # Increase padding
    entry = ttk.Entry(dialog, font=("Arial", 12), width=30)  # Increase font size and width
    entry.pack(pady=10)  # Increase padding
    username = None  # Initialize username to None
    def submit():
        nonlocal username  # Declare username as non-local
        username = entry.get()
        dialog.destroy()
        root.destroy()
    def handle_enter(event):
        submit()
    submit_button = ttk.Button(dialog, text="Submit", command=submit)
    submit_button.pack(pady=10)
    dialog.bind('<Return>', handle_enter)  # Bind Enter key to submit function
    # Center the dialog box on the screen
    dialog.update_idletasks()
    width = dialog.winfo_width()
    height = dialog.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    dialog.geometry(f"{width}x{height}+{x}+{y}")

    # Run the dialog box
    dialog.grab_set()
    root.wait_window(dialog)

    return username



pygame.init()

pygame.display.set_caption("Platformer")

WIDTH, HEIGHT = 1000, 720
FPS = 60
PLAYER_VEL = 3
score = 0
start_time = 0
map_end = 3560

# declare objects list
objects = []

# Load font
timer_font = pygame.font.Font("assets/fonts/retro_font.ttf", 30)
score_font = pygame.font.Font("assets/fonts/retro_font.ttf", 30)

# Add these global variables at the top of your code
timer_start=pygame.time.get_ticks()
run = True
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Initialize pygame mixer
pygame.mixer.init()

# Load music file


# Function to display timer and score
def display_info(window):
    global score, timer_start
    # Calculate elapsed time
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - timer_start) // 1000

    # Render timer text with retro style
    timer_text = timer_font.render("Time: " + str(elapsed_time) + "s", True, (255, 255, 255))  
    window.blit(timer_text, (WIDTH - 250, 20))  # Adjusted position

    # Render score text with retro style
    score_text = score_font.render("Score: " + str(score), True, (255, 0, 255))  # Magenta color
    window.blit(score_text, (WIDTH - 250, 70))  # Adjusted position


def flip(sprites):
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]


def load_sprite_sheets(dir1, dir2, width, height, direction=False):
    path = join("assets", dir1, dir2)
    images = [f for f in listdir(path) if isfile(join(path, f))]

    all_sprites = {}

    for image in images:
        sprite_sheet = pygame.image.load(join(path, image)).convert_alpha()

        sprites = []
        for i in range(sprite_sheet.get_width() // width):
            surface = pygame.Surface((width, height), pygame.SRCALPHA, 32)
            rect = pygame.Rect(i * width, 0, width, height)
            surface.blit(sprite_sheet, (0, 0), rect)
            sprites.append(pygame.transform.scale2x(surface))

        if direction:
            all_sprites[image.replace(".png", "") + "_right"] = sprites
            all_sprites[image.replace(".png", "") + "_left"] = flip(sprites)
        else:
            all_sprites[image.replace(".png", "")] = sprites

    return all_sprites


def get_block(size,type="ground"):
    path = join("assets", "Terrain", "Terrain.png")
    image = pygame.image.load(path).convert_alpha()
    surface = pygame.Surface((size, size), pygame.SRCALPHA, 32)
    if type == "ground":
        rect = pygame.Rect(96, 0, size, size)
    elif type == "brick":
        rect = pygame.Rect(272, 64, size, size)
    elif type == "gold":
        rect = pygame.Rect(288, 144, 30, 30)
        
    surface.blit(image, (0, 0), rect)
    if type == "gold":
        surface = pygame.transform.scale(surface, (48, 48))
    return surface


class Player(pygame.sprite.Sprite):
    COLOR = (255, 0, 0)
    GRAVITY = 1
    SPRITES = load_sprite_sheets("MainCharacters", "PinkMan", 32, 32, True)
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.x_vel = 0
        self.y_vel = 0
        self.mask = None
        self.direction = "left"
        self.animation_count = 0
        self.fall_count = 0
        self.jump_count = 0
        self.hit = False
        self.hit_count = 0

    def jump(self):
        self.y_vel = -self.GRAVITY * 7
        self.animation_count = 0
        self.jump_count += 1
        if self.jump_count == 1:
            self.fall_count = 0

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def make_hit(self):
        self.hit = True

    def move_left(self, vel):
        self.x_vel = -vel
        if self.direction != "left":
            self.direction = "left"
            self.animation_count = 0

    def move_right(self, vel):
        self.x_vel = vel
        if self.direction != "right":
            self.direction = "right"
            self.animation_count = 0

    def loop(self, fps):
        self.y_vel += min(1, (self.fall_count / fps) * self.GRAVITY)
        self.move(self.x_vel, self.y_vel)

        if self.hit:
            self.hit_count += 1
        if self.hit_count > fps * 2:
            self.hit = False
            self.hit_count = 0

        self.fall_count += 1
        self.update_sprite()

    def landed(self):
        self.fall_count = 0
        self.y_vel = 0
        self.jump_count = 0

    def hit_head(self):
        self.count = 0
        self.y_vel *= -1

    def update_sprite(self):
        sprite_sheet = "idle"
        if self.hit:
            sprite_sheet = "hit"
        elif self.y_vel < 0:
            if self.jump_count == 1:
                sprite_sheet = "jump"
            elif self.jump_count == 2:
                sprite_sheet = "double_jump"
        elif self.y_vel > self.GRAVITY * 2:
            sprite_sheet = "fall"
        elif self.x_vel != 0:
            sprite_sheet = "run"

        sprite_sheet_name = sprite_sheet + "_" + self.direction
        sprites = self.SPRITES[sprite_sheet_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.sprite = sprites[sprite_index]
        self.animation_count += 1
        self.update()

    def update(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def draw(self, win, offset_x):
        win.blit(self.sprite, (self.rect.x - offset_x, self.rect.y))


class Object(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, name=None):
        super().__init__()
        self.rect = pygame.Rect(x, y, width, height)
        self.image = pygame.Surface((width, height), pygame.SRCALPHA)
        self.width = width
        self.height = height
        self.name = name

    def draw(self, win, offset_x):
        win.blit(self.image, (self.rect.x - offset_x, self.rect.y))


class Block(Object):
    def __init__(self, x, y, size, type="ground"):
        super().__init__(x, y, size, size)
        if type == "ground":
            block = get_block(size)
        elif type == "brick":
            block = get_block(size,type)
        elif type == "gold block":
            block = get_block(size,"gold")
            block = pygame.transform.scale(block, (76,76))
        
        # self.image.blit(block, (0, 0))
        self.image = block
        self.mask = pygame.mask.from_surface(self.image)


class Fire(Object):
    ANIMATION_DELAY = 3

    def __init__(self, x, y, width, height):
        super().__init__(x, y-16, width, height, "fire")
        self.fire = load_sprite_sheets("Traps", "Fire", 16, 32)
        self.image = self.fire["off"][0]
        self.mask = pygame.mask.from_surface(self.image)
        self.animation_count = 0
        self.animation_name = "off"

    def on(self):
        self.animation_name = "on"

    def off(self):
        self.animation_name = "off"

    def loop(self):
        sprites = self.fire[self.animation_name]
        sprite_index = (self.animation_count //
                        self.ANIMATION_DELAY) % len(sprites)
        self.image = sprites[sprite_index]
        self.animation_count += 1

        self.rect = self.image.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.image)

        if self.animation_count // self.ANIMATION_DELAY > len(sprites):
            self.animation_count = 0


class Fruit(Object):
    def __init__(self, x, y, width, height, type="Cherries"):
        super().__init__(x-16, y-16, width, height, type)
        self.fruits = load_sprite_sheets("Items", "Fruits", 32, 32)
        self.image = self.fruits[type][0]
        # resize the image to 32x32
        self.mask = pygame.mask.from_surface(self.image)
        self.taken = False

    def take(self):
        global score  # Access the global score variable
        if not self.taken:
            score += 1  # Increment the score
            self.taken = True
            coin_pick_sound_file = os.path.join("assets", "music", "collect-point.mp3")
            coin_pick_sound = pygame.mixer.Sound(coin_pick_sound_file)
            coin_pick_sound.play()
            global objects
            objects.remove(self)  # Remove the fruit from the objects list


class Trophy(Object):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        image_path = join("assets", "Items", "Checkpoints","End","End (Idle).png")
        self.image = pygame.image.load(image_path).convert_alpha()
        # resize the image to 80x96
        self.image = pygame.transform.scale(self.image, (width, height))
        self.mask = pygame.mask.from_surface(self.image)


def get_background(name):
    image = pygame.image.load(join("assets", "Background", name))
    _, _, width, height = image.get_rect()
    tiles = []

    for i in range(WIDTH // width + 1):
        for j in range(HEIGHT // height + 1):
            pos = (i * width, j * height)
            tiles.append(pos)

    return tiles, image


def draw(window, background, bg_image, player, objects, offset_x):
    for tile in background:
        window.blit(bg_image, tile)

    for obj in objects:
        obj.draw(window, offset_x)

    player.draw(window, offset_x)

    # Display timer and score
    display_info(window)

    pygame.display.update()


def handle_vertical_collision(player, objects, dy):
    collided_objects = []
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            if dy > 0:
                player.rect.bottom = obj.rect.top
                player.landed()
            elif dy < 0:
                player.rect.top = obj.rect.bottom
                player.hit_head()

            collided_objects.append(obj)

    return collided_objects


def collide(player, objects, dx):
    player.move(dx, 0)
    player.update()
    collided_object = None
    for obj in objects:
        if pygame.sprite.collide_mask(player, obj):
            collided_object = obj
            break

    player.move(-dx, 0)
    player.update()
    return collided_object


def draw_text(text, font_path, color, surface, x, y, font_size=None):
    if font_size:
        font = pygame.font.Font(font_path, font_size)
    else:
        font = pygame.font.Font(font_path, 30)  # Default font size
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)


def main_page():
    background_image = pygame.image.load("./assets/Background/frontpage3.jpg").convert()
    background_rect = background_image.get_rect()
    
    # Scale the background image to fit the window size
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    music_file = os.path.join("assets", "music", "bgm.mp3")
    pygame.mixer.music.load(music_file)
# Play music (-1 for infinite loop)
    pygame.mixer.music.play(-1)

    while True:
        # Blit the scaled background image onto the window surface
        #print("i am in main loop")
        window.blit(background_image, background_rect)
        
        # Draw heading
        draw_text("Platformer Game", "assets/fonts/atop_font.ttf", (255,0,0), window, 20, 80, font_size=60)
        # Load images for buttons
        one_button_image = pygame.image.load("./assets/Other/map1.png").convert_alpha()
        two_button_image = pygame.image.load("./assets/Other/map2.png").convert_alpha()
        leaderboard_button_image = pygame.image.load("./assets/Menu/Buttons/Leaderboard.png").convert_alpha()
        # Resize buttons to 200x200
        one_button_image = pygame.transform.scale(one_button_image, (200, 200))
        two_button_image = pygame.transform.scale(two_button_image, (200, 200))
        leaderboard_button_image = pygame.transform.scale(leaderboard_button_image, (100,100))
        # Blit buttons onto the window surface
        window.blit(one_button_image, (int(WIDTH*1.7//5 - 100), int(HEIGHT//2-50 - 100)))
        window.blit(two_button_image, (int(WIDTH * 3//5 - 100), int(HEIGHT//2-50 - 100)))
        window.blit(leaderboard_button_image, (int(WIDTH * 4//5 ), int(HEIGHT//2-50 + 150)))
        # Add text below buttons
        draw_text("Map 1", "assets/fonts/atop_font.ttf", (255,102,102), window, WIDTH//5 +100, HEIGHT//2 + 50)
        draw_text("Map 2", "assets/fonts/atop_font.ttf", (255,102,102), window, WIDTH * 4//5 -250, HEIGHT//2 + 50)
        draw_text("Leaderboard", "assets/fonts/atop_font.ttf", (0,255,0), window, WIDTH * 4//5 -15, HEIGHT//2 + 200,font_size=20)
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                # Get rectangles for buttons
                one_button_rect = pygame.Rect(int(WIDTH*1.7//5 - 100), int(HEIGHT//2-50 - 100), 200, 200)
                two_button_rect = pygame.Rect(int(WIDTH * 3//5 - 100), int(HEIGHT//2-50 - 100), 200, 200)
                leaderboard_button_rect = pygame.Rect(int(WIDTH * 4//5), int(HEIGHT//2-50 + 150), 200, 200)

                # Check if a button is clicked
                if one_button_rect.collidepoint(mouse_pos):
                    return "one"
                elif two_button_rect.collidepoint(mouse_pos):
                    return "two"
                elif leaderboard_button_rect.collidepoint(mouse_pos):
                    
                    # Replace "leaderboard" with the page you want to navigate to
                    return "leaderboard"

        pygame.display.update()


selected_level = main_page()

def handle_game_over(player, hit_fire=False):
    global run
    global name
    global selected_level
    if hit_fire or player.rect.y > HEIGHT:
        # Game over logic here
        out_music_file = os.path.join("assets", "music", "game_over.mp3")
        out_music = pygame.mixer.Sound(out_music_file)
        out_music.play()
               
        print("Game Over!")
        player.rect.x = 100
        player.rect.y = 50
        run=False
        
    
    elif  player.rect.x >= map_end:
        # Game complete
        end_time = pygame.time.get_ticks()
        
        player.rect.x = 100
        player.rect.y = 50
        print("You Won!!!\n  Time taken: ", (end_time - start_time) / 1000, " seconds\n Score: ", score)
        win_music_file = os.path.join("assets", "music", "game_win.mp3")

        win_game=pygame.mixer.Sound(win_music_file)
        win_game.play()
        global selected_level
        if selected_level == "one":
            with open("platform1_scores.txt", "a") as file:
                file.write(f"{name},{score},{(end_time - start_time) / 1000}\n")
        else:
            with open("platform2_scores.txt", "a") as file:
                file.write(f"{name},{score},{(end_time - start_time) / 1000}\n")
        run=False
        # You can also add code to reset the game or display a game over screen
        
    
    return False


def handle_move(player, objects):
    keys = pygame.key.get_pressed()

    player.x_vel = 0
    collide_left = collide(player, objects, -PLAYER_VEL * 2)
    collide_right = collide(player, objects, PLAYER_VEL * 2)

    if keys[pygame.K_LEFT] and not collide_left:
        player.move_left(PLAYER_VEL)
    if keys[pygame.K_RIGHT] and not collide_right:
        player.move_right(PLAYER_VEL)

    vertical_collide = handle_vertical_collision(player, objects, player.y_vel)
    to_check = [collide_left, collide_right, *vertical_collide]


    for obj in to_check:
        if obj and obj.name == "fire":
            # player.make_hit()
            handle_game_over(player, True)
            
        elif obj and obj.name in ["Cherries","Banana","Orange","Apple","Strawberry"]:
            obj.take()  # Call the take method for fruits

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)                       
font = pygame.font.Font(None, 36)




def draw_leaderboard(window):
    # Load background image
    background_image = pygame.image.load("./assets/Background/frontimage4.jpg")
    # Scale the background image to fit the window size
    background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
    # Draw the background image onto the window
    window.blit(background_image, (0, 0))

    platform1_scores = []
    with open("./platform1_scores.txt", "r") as file:
        leaderboard_data = file.readlines()
    print(leaderboard_data)
    leaderboard_data.sort(key=lambda x: (-int(x.strip().split(",")[1]), float(x.strip().split(",")[2].split()[0])))

    for line in leaderboard_data[:5]:
        player, score, time = line.strip().split(",")
        platform1_scores.append((player, int(score), float(time.split()[0])))
    platform2_scores = []
    with open("./platform2_scores.txt", "r") as file:
        leaderboard_data = file.readlines()
    leaderboard_data.sort(key=lambda x: (-int(x.strip().split(",")[1]), float(x.strip().split(",")[2].split()[0])))
    for line in leaderboard_data[:5]:
        player, score, time = line.strip().split(",")
        platform2_scores.append((player, int(score), float(time.split()[0])))

    # Sort the scores by score value
    platform1_scores.sort(key=lambda x: x[1], reverse=True)
    platform2_scores.sort(key=lambda x: x[1], reverse=True)

    # Display the leaderboard title
    draw_text("Leaderboard", "assets/fonts/atop_font.ttf", (255, 0, 0), window, WIDTH // 2 - 100, 20, font_size=40)

    # Display Platform 1 scores in a table format
    draw_text("Platform 1", "assets/fonts/atop_font.ttf", (255, 25,25), window, 20, 80, font_size=35)
    draw_text("Rank                             Player                                 Score                  Time", "assets/fonts/atop_font.ttf", (0,255,0), window, 50, 120, font_size=25)
    y_offset = 150
    for i, (player, score, time) in enumerate(platform1_scores[:5]):
        draw_text(f"{i+1}.", "assets/fonts/atop_font.ttf", (255, 255, 255), window, 80, y_offset, font_size=25)
        draw_text(player[:10] if len(player) > 10 else player, "assets/fonts/atop_font.ttf", (255, 255, 255), window, 290, y_offset, font_size=25)
        draw_text(str(score), "assets/fonts/atop_font.ttf", (255, 255, 255), window, 610, y_offset, font_size=25)
        draw_text(f"{time}s", "assets/fonts/atop_font.ttf", (255, 255, 255), window, 780, y_offset, font_size=25)
        y_offset += 40

    # Display Platform 2 scores in a table format
    draw_text("Platform 2", "assets/fonts/atop_font.ttf", (255,25,25), window, 20, y_offset + 20, font_size=35)
    draw_text("Rank                             Player                                 Score                  Time", "assets/fonts/atop_font.ttf", (0, 255, 0), window, 50, y_offset + 60, font_size=25)
    y_offset += 90
    for i, (player, score, time) in enumerate(platform2_scores[:5]):
        draw_text(f"{i+1}.", "assets/fonts/atop_font.ttf", (255, 255, 255), window, 80, y_offset, font_size=25)
        draw_text(player[:10] if len(player) > 10 else player, "assets/fonts/atop_font.ttf", (255, 255, 255), window, 290, y_offset, font_size=25)
        draw_text(str(score), "assets/fonts/atop_font.ttf", (255, 255, 255), window, 610, y_offset, font_size=25)
        draw_text(f"{time}s", "assets/fonts/atop_font.ttf", (255, 255, 255), window, 780, y_offset, font_size=25)
        y_offset += 40

    # Display a back button
    draw_text("Back", "assets/fonts/atop_font.ttf", (255, 255, 255), window, WIDTH - 100, HEIGHT - 50, font_size=25)

    pygame.display.update()



def leaderboard_page():
    global run
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if the back button is clicked
                if WIDTH - 100 <= mouse_pos[0] <= WIDTH and HEIGHT - 50 <= mouse_pos[1] <= HEIGHT:
                    return "main"  # Return to the main page

        window.fill((255, 255, 255))  # Clear the screen
        draw_leaderboard(window)  # Display the leaderboard
        pygame.display.update()




def main(window):
    clock = pygame.time.Clock()
    # record start time
    global start_time
    start_time = pygame.time.get_ticks()

    background, bg_image = get_background("Brown.png")

    block_size = 48
    map_choose=selected_level

    global map_end
    if map_choose == "one":
        map = MAP_ONE(block_size, WIDTH, HEIGHT, 16, 32)
        map_end = 3560
    elif map_choose=="two":
        map = MAP_TWO(block_size, WIDTH, HEIGHT, 32, 48)
        map_end = 4070
    else:
        leaderboard_page()

    player = Player(block_size, 100, 50, 50)


    global objects
    objects = [Block(x, y, block_size, type) for x, y, type in map.get_blocks()]

    # Add fires
    for x, y in map.get_fires():
        fire = Fire(x, y, 32, 48)
        fire.on()
        objects.append(fire)

    # Add fruits
    for x, y, type in map.get_fruits():
        fruit = Fruit(x, y, 16, 32, type)
        objects.append(fruit)

    # Add trophy
    trophy = Trophy(3608, 576, 80, 96)
    objects.append(trophy)

    offset_x = 0
    scroll_area_width = 200

    global run    
    while run:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player.jump_count < 2:
                    player.jump()

        player.loop(FPS)

        for obj in objects:
            if obj.name == "fire":
                obj.loop()
        
        handle_move(player, objects)
        draw(window, background, bg_image, player, objects, offset_x)

        if ((player.rect.right - offset_x >= WIDTH - scroll_area_width) and player.x_vel > 0) or (
                (player.rect.left - offset_x <= scroll_area_width) and player.x_vel < 0):
            offset_x += player.x_vel

        # Check for game over condition
        if handle_game_over(player):
            
            return "main"
    global score        
    run=True
    score=0
    #pygame.quit()
    #quit()

name=None

while True:
    selected_level = main_page()
    
    if selected_level == "leaderboard":
        selected_level = leaderboard_page()
    elif selected_level == "one" or selected_level == "two":
        while not name:  # Keep asking for username until it's provided
            name = get_username()
        if name:
            timer_start = pygame.time.get_ticks()
            returned_page = main(window)
            if returned_page == "main":
                
                continue
    else:
        break




