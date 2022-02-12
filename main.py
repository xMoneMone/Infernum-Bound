import pygame as pg
import sys

WIDTH = 1000
HEIGHT = 700
BG_COLOUR = (50, 23, 43)
FPS = 20
SPEED = 6
MOF = 7
SLOWDOWN = 3

pg.init()
pg.font.init()

monitor = pg.display.Info()

# FLAGS
fullscreen = False
beginning = True
inventory_open = False
wait = False
dialogue_open = True
safe = True
pink = False
purple = False
blue = False
game = False
win = False

backfurniture_group = pg.sprite.Group()
frontfurniture_group = pg.sprite.Group()
all_furniture = pg.sprite.Group()
items_group = pg.sprite.Group()


class Furniture(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y, path, name):
        super().__init__()
        self.name = name
        self.image = pg.image.load(path).convert()
        self.rect = self.image.get_rect(topleft=(pos_x, pos_y))
        self.image.set_colorkey((5, 0, 255))
        self.desc = ""
        all_furniture.add(self)


class BackFurniture(Furniture):
    def __init__(self, pos_x, pos_y, path, name):
        super().__init__(pos_x, pos_y, path, name)
        backfurniture_group.add(self)


class FrontFurniture(Furniture):
    def __init__(self, pos_x, pos_y, path, name):
        super().__init__(pos_x, pos_y, path, name)
        self.rect = pg.Rect(pos_x, pos_y, self.image.get_width(), (self.image.get_height() // 3) * 2)
        frontfurniture_group.add(self)


class Character(pg.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.player = pg.image.load(r"graphics\character-sprite\down-1.png").convert_alpha()
        self.player.set_colorkey((5, 0, 255))
        self.rect = pg.Rect(pos_x, pos_y, self.player.get_width(), self.player.get_height() // 3)
        self.vertical_rect = pg.Rect(self.rect.x + self.rect.width // 2, self.rect.y - 6, 3, self.rect.height + 12)
        self.horizontal_rect = pg.Rect(self.rect.x - 6, self.rect.y + self.rect.height // 2, self.rect.width + 12, 3)
        self.future = pg.Rect(self.rect.x, self.rect.y, self.player.get_width(), self.player.get_height() // 3)
        self.frame = 1
        self.priority = []
        self.last_pressed = ""

        self.down = {1: pg.image.load(r"graphics\character-sprite\down-1.png").convert(),
                     2: pg.image.load(r"graphics\character-sprite\down-2.png").convert(),
                     3: pg.image.load(r"graphics\character-sprite\down-3.png").convert(),
                     4: pg.image.load(r"graphics\character-sprite\down-4.png").convert()}

        self.up = {1: pg.image.load(r"graphics\character-sprite\up-1.png").convert(),
                   2: pg.image.load(r"graphics\character-sprite\up-2.png").convert(),
                   3: pg.image.load(r"graphics\character-sprite\up-3.png").convert(),
                   4: pg.image.load(r"graphics\character-sprite\up-4.png").convert()}

        self.left = {1: pg.image.load(r"graphics\character-sprite\left-1.png").convert(),
                     2: pg.image.load(r"graphics\character-sprite\left-2.png").convert(),
                     3: pg.image.load(r"graphics\character-sprite\left-3.png").convert(),
                     4: pg.image.load(r"graphics\character-sprite\left-4.png").convert()}

        self.right = {1: pg.image.load(r"graphics\character-sprite\right-1.png").convert(),
                      2: pg.image.load(r"graphics\character-sprite\right-2.png").convert(),
                      3: pg.image.load(r"graphics\character-sprite\right-3.png").convert(),
                      4: pg.image.load(r"graphics\character-sprite\right-4.png").convert()}

        for frame in self.down:
            self.down[frame].set_colorkey((5, 0, 255))
        for frame in self.up:
            self.up[frame].set_colorkey((5, 0, 255))
        for frame in self.left:
            self.left[frame].set_colorkey((5, 0, 255))
        for frame in self.right:
            self.right[frame].set_colorkey((5, 0, 255))

    def interaction(self):

        for surface in all_furniture:
            if self.horizontal_rect.colliderect(surface) and self.last_pressed in ("left", "right"):
                return surface.name
            elif self.vertical_rect.colliderect(surface) and self.last_pressed in ("up", "down"):
                return surface.name

    def future_collision(self, x_mod, y_mod):
        self.future.x = self.rect.x + x_mod
        self.future.y = self.rect.y + y_mod

    def turn(self):
        if self.last_pressed == "up":
            self.player = self.up[1]
        elif self.last_pressed == "down":
            self.player = self.down[1]
        elif self.last_pressed == "right":
            self.player = self.right[1]
        elif self.last_pressed == "left":
            self.player = self.left[1]

    def animation(self):

        match self.priority[-1]:
            case "down":
                self.player = self.down[self.frame // SLOWDOWN + 1]
            case "up":
                self.player = self.up[self.frame // SLOWDOWN + 1]
            case "left":
                self.player = self.left[self.frame // SLOWDOWN + 1]
            case "right":
                self.player = self.right[self.frame // SLOWDOWN + 1]

        self.frame += 1
        if self.frame == 4 * SLOWDOWN:
            self.frame = 1

    def move(self):

        self.turn()
        pressed = pg.key.get_pressed()

        if pressed[pg.K_DOWN] or pressed[pg.K_s]:
            self.last_pressed = "down"
            if self.rect.bottom - room_rect.bottom + 33 < MOF:
                if "down" == self.priority[-1]:
                    self.future_collision(0, SPEED)
                    for surface in all_furniture:
                        if self.future.colliderect(surface):
                            if abs(self.future.bottom - surface.rect.top) < MOF:
                                break
                    else:
                        self.rect.y += SPEED
                        self.vertical_rect.y += SPEED
                        self.horizontal_rect.y += SPEED
                        self.animation()

        if pressed[pg.K_UP] or pressed[pg.K_w]:
            self.last_pressed = "up"
            if self.rect.top - room_rect.top - 150 > MOF:
                if "up" == self.priority[-1]:
                    self.future_collision(0, -SPEED)
                    for surface in all_furniture:
                        if self.future.colliderect(surface):
                            if abs(self.future.top - surface.rect.bottom) < MOF:
                                break
                    else:
                        self.rect.y -= SPEED
                        self.vertical_rect.y -= SPEED
                        self.horizontal_rect.y -= SPEED
                        self.animation()

        if pressed[pg.K_LEFT] or pressed[pg.K_a]:
            self.last_pressed = "left"
            if self.rect.left - room_rect.left - 9 > MOF:
                if "left" == self.priority[-1]:
                    self.future_collision(-SPEED, 0)
                    for surface in all_furniture:
                        if self.future.colliderect(surface):
                            if abs(self.future.left - surface.rect.right) < MOF:
                                break
                    else:
                        self.rect.x -= SPEED
                        self.vertical_rect.x -= SPEED
                        self.horizontal_rect.x -= SPEED
                        self.animation()

        if pressed[pg.K_RIGHT] or pressed[pg.K_d]:
            self.last_pressed = "right"
            if self.rect.right - room_rect.right + 22 < MOF:
                if "right" == self.priority[-1]:
                    self.future_collision(SPEED, 0)
                    for surface in all_furniture:
                        if self.future.colliderect(surface):
                            if abs(self.future.right - surface.rect.left) < MOF:
                                break
                    else:
                        self.rect.x += SPEED
                        self.vertical_rect.x += SPEED
                        self.horizontal_rect.x += SPEED
                        self.animation()


class Item(pg.sprite.Sprite):
    def __init__(self, path, name):
        super().__init__()
        self.name = name
        self.image = pg.image.load(path).convert()
        self.rect = self.image.get_rect()
        self.image.set_colorkey((10, 0, 255))
        self.desc = ""
        items_group.add(self)


class Star(pg.sprite.Sprite):
    def __init__(self, rect, name):
        super().__init__()
        self.name = name
        self.rect = rect


# GENERAL SETUP
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Infernum Bound")
icon = pg.image.load(r"graphics\icon.png").convert()
icon.set_colorkey((5, 0, 255))
pg.display.set_icon(icon)
clock = pg.time.Clock()
font = pg.font.Font(r"graphics\dialogue\Pixeltype.ttf", 40)
pg.mouse.set_visible(False)

# BACKGROUND
room = pg.image.load(r"graphics\furniture\room.png").convert()
room_rect = room.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
room.set_colorkey((5, 0, 255))

# FURNITURE LOADING
furniture = {}


def load_furniture():
    with open(r"graphics\furniture\coords.txt", "r") as f:
        for ln in f.readlines():
            x, y, path, name, flag = ln.strip().split(",")
            if flag == "b":
                furniture[name] = BackFurniture(room_rect.x + int(x), room_rect.y + int(y), path, name)
            else:
                furniture[name] = FrontFurniture(room_rect.x + int(x), room_rect.y + int(y), path, name)


load_furniture()

# SPECIAL RECTANGLES
furniture["cover"].rect = furniture["cover"].image.get_rect(topleft=(room_rect.x + 147 * 3, room_rect.y))
furniture["bunny"].rect = pg.Rect(room_rect.x + 89 * 3, room_rect.y + 36 * 3, furniture["bunny"].image.get_width(),
                                  furniture["bunny"].image.get_height() - 6)
furniture["drawer_lr"].rect = pg.Rect(room_rect.x + 28 * 3, room_rect.y + 44 * 3,
                                      furniture["drawer_lr"].image.get_width(),
                                      furniture["drawer_lr"].image.get_height() - 3)
furniture["painting"].rect.height += 12 * 3

# CHARACTER
soph = Character(room_rect.left + 27 * 3, room_rect.top + 82 * 3)

# DIALOGUE

speech_bubble = pg.image.load(r"graphics\dialogue\bubble.png").convert_alpha()
bubble_place = (0, 147)


def dialogue(text):
    screen.blit(speech_bubble, (room_rect.x + 0, room_rect.y + 140 * 3))
    text = text.split("%")
    y = 150
    for ln in text:
        screen.blit((font.render(ln, False, (255, 255, 255))),
                    (room_rect.x + 10 * 3, room_rect.y + y * 3))
        y += 10


# ITEM LOADING
items = {}


def load_items():
    with open(r"graphics\inventory\itemlist.txt", "r") as f:
        for ln in f:
            path, name = ln.strip().split(",")
            items[name] = Item(path, name)


load_items()

# INVENTORY
inventory_background = pg.image.load(r"graphics\inventory\inventory.png").convert()
inventory_background_rect = inventory_background.get_rect(center=(room_rect.x + room_rect.width // 2,
                                                                  room_rect.y + room_rect.height // 2))
inventory_background.set_colorkey((5, 0, 255))

inventory_pick = pg.image.load(r"graphics\inventory\inventory-selection.png").convert()
inventory_pick_rect = inventory_pick.get_rect(topleft=(1000, 1000))
inventory_pick.set_colorkey((5, 0, 255))

fade = pg.image.load(r"graphics\inventory\fade.png").convert_alpha()

slot_x = 1
slot_y = 1
next_vertical = 6 + inventory_pick.get_width()
next_horizontal = 9 + inventory_pick.get_height()

slots = ((27, 27), (102, 27), (177, 27), (252, 27), (327, 27),
         (27, 99), (102, 99), (177, 99), (252, 99), (327, 99),
         (27, 171), (102, 171), (177, 171), (252, 171), (327, 171))

inventory = []
removed = []

# inventory = [items["rubber_gloves"], items["ocular"], items["flashlight"], items["empty_glass"], items["golden_key"],
#              items["purple_gem"]]

has_items = ["drawer_lr", "desk_2", "drawer_br", "table_1", "crack"]


# adds all items // for testing
# for item_ye in items_group:
#     inventory.append(items[item_ye.name])


def inventory_inside():
    used_item = ""

    for thing in items_group:
        if inventory_pick_rect.colliderect(thing.rect):
            used_item = thing.name

    return used_item


# TEXT LOADING

def load_text(dic, path):
    with open(path, "r", encoding="utf8") as f:
        for ln in f:
            name, text = ln.strip().split(",")
            dic[name].desc = text


load_text(items, r"graphics\dialogue\items.txt")
load_text(furniture, r"graphics\dialogue\furniture.txt")

# POPUPS
popup_computer = pg.image.load(r"graphics\popups\computer.png").convert()
popup_computer.set_colorkey((5, 0, 255))

popup_telescope = pg.image.load(r"graphics\popups\telescope.png").convert()
popup_telescope.set_colorkey((5, 0, 255))

popup_wardrobe = pg.image.load(r"graphics\popups\wardrobe.png").convert()
popup_wardrobe.set_colorkey((5, 0, 255))

frame0 = pg.image.load(r"graphics\popups\telescope.png").convert()
frame0.set_colorkey((5, 0, 255))
frame1 = pg.image.load(r"graphics\popups\game1.png").convert()
frame1.set_colorkey((5, 0, 255))
frame2 = pg.image.load(r"graphics\popups\game2.png").convert()
frame2.set_colorkey((5, 0, 255))
frame3 = pg.image.load(r"graphics\popups\game3.png").convert()
frame3.set_colorkey((5, 0, 255))
frame4 = pg.image.load(r"graphics\popups\game4.png").convert()
frame4.set_colorkey((5, 0, 255))
frame5 = pg.image.load(r"graphics\popups\game5.png").convert()
frame5.set_colorkey((5, 0, 255))
frame6 = pg.image.load(r"graphics\popups\game6.png").convert()
frame6.set_colorkey((5, 0, 255))

star1 = Star((pg.Rect(inventory_background_rect.x + 39, inventory_background_rect.y + 56 * 3, 7 * 3, 9 * 3)), "star1")
star2 = Star((pg.Rect(inventory_background_rect.x + 29 * 3, inventory_background_rect.y + 14 * 3, 7 * 3, 10 * 3)),
             "star2")
star3 = Star((pg.Rect(inventory_background_rect.x + 39 * 3, inventory_background_rect.y + 34 * 3, 7 * 3, 9 * 3)),
             "star3")
star4 = Star((pg.Rect(inventory_background_rect.x + 59 * 3, inventory_background_rect.y + 40 * 3, 9 * 3, 13 * 3)),
             "star4")
star6 = Star((pg.Rect(inventory_background_rect.x + 82 * 3, inventory_background_rect.y + 17 * 3, 7 * 3, 10 * 3)),
             "star6")
star5 = Star((pg.Rect(inventory_background_rect.x + 100 * 3, inventory_background_rect.y + 45 * 3, 7 * 3, 10 * 3)),
             "star5")

answer = (star1, star2, star3, star4, star5, star6)
current = []


# FADE
def fade_out():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(0, 300):
        fade_sur.set_alpha(number)
        screen.fill(BG_COLOUR)
        screen.blit(room, room_rect)
        backfurniture_group.draw(screen)
        screen.blit(soph.player, (soph.rect.x, soph.rect.y - soph.rect.height * 2))
        for furnt in frontfurniture_group:
            if furnt is not furniture["cover"]:
                screen.blit(furnt.image, (furnt.rect.x, furnt.rect.y - furnt.rect.height // 2))
            else:
                screen.blit(furnt.image, furnt.rect)
        screen.blit(fade_sur, (0, 0))
        pg.display.update()
        pg.time.delay(3)


def fade_in():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(300, 0, -1):
        fade_sur.set_alpha(number)
        screen.fill(BG_COLOUR)
        screen.blit(room, room_rect)
        backfurniture_group.draw(screen)
        screen.blit(soph.player, (soph.rect.x, soph.rect.y - soph.rect.height * 2))
        for furnt in frontfurniture_group:
            if furnt is not furniture["cover"]:
                screen.blit(furnt.image, (furnt.rect.x, furnt.rect.y - furnt.rect.height // 2))
            else:
                screen.blit(furnt.image, furnt.rect)
        screen.blit(fade_sur, (0, 0))
        pg.display.update()
        pg.time.delay(3)


# CUTSCENES
current_cut_screen = 1
current_cut_screen_e = 1
b_cut_screen = True
e_cut_screen = True


def show_cut_screen():
    cut_screen_path = "graphics/story/b" + str(current_cut_screen) + ".png"
    surf = pg.image.load(cut_screen_path).convert()
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill((44, 9, 49))
    screen.blit(surf, rect)


def change_cut_screen():
    global current_cut_screen
    current_cut_screen += 1
    if current_cut_screen >= 6:
        global b_cut_screen
        b_cut_screen = False


def fade_in_cs():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(300, 0, -5):
        fade_sur.set_alpha(number)
        show_cut_screen()
        screen.blit(fade_sur, (0, 0))
        pg.display.update()


def fade_out_cs():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(0, 300, 5):
        fade_sur.set_alpha(number)
        show_cut_screen()
        screen.blit(fade_sur, (0, 0))
        pg.display.update()


def show_cut_screen_e():
    cut_screen_path = "graphics/story/e" + str(current_cut_screen_e) + ".png"
    surf = pg.image.load(cut_screen_path).convert()
    rect = surf.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.fill((44, 9, 49))
    screen.blit(surf, rect)


def change_cut_screen_e():
    global current_cut_screen_e
    current_cut_screen_e += 1
    if current_cut_screen_e >= 9:
        global e_cut_screen
        e_cut_screen = False


def fade_in_e():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(300, 0, -5):
        fade_sur.set_alpha(number)
        show_cut_screen_e()
        screen.blit(fade_sur, (0, 0))
        pg.display.update()


def fade_out_e():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(0, 300, 5):
        fade_sur.set_alpha(number)
        show_cut_screen_e()
        screen.blit(fade_sur, (0, 0))
        pg.display.update()


def bg_cs_fade_in():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(300, 0, -3):
        fade_sur.set_alpha(number)
        screen.fill((44, 9, 49))
        show_cut_screen()
        screen.blit(fade_sur, (0, 0))
        pg.display.update()
        pg.time.delay(3)


def end_cs_fade_in():
    fade_sur = pg.Surface((WIDTH, HEIGHT))
    fade_sur.fill((0, 0, 0))
    for number in range(300, 0, -3):
        fade_sur.set_alpha(number)
        screen.fill((44, 9, 49))
        show_cut_screen_e()
        screen.blit(fade_sur, (0, 0))
        pg.display.update()
        pg.time.delay(3)


# SOUND
interact = pg.mixer.Sound(r"sound\interaction.wav")
interact.set_volume(0.05)
game_loop = pg.mixer.Sound(r"sound\ingame_loop.ogg")
game_loop.set_volume(0.05)
cutscene_loop = pg.mixer.Sound(r"sound\cutsdcene_loop.ogg")
cutscene_loop.set_volume(0.1)

# TITLE
change_x = (monitor.current_w - 1000) // 2  # used for keeping character position constant
change_y = (monitor.current_h - 700) // 2  # when switching to fullscreen

title1 = pg.image.load(r"graphics\story\title1.png").convert()
title_rect = title1.get_rect(center=(WIDTH // 2, HEIGHT // 2))
title2 = pg.image.load(r"graphics\story\title2.png").convert()
title = True
fr = True

cutscene_loop.play(loops=-1)

while title:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            interact.play()
            if event.key == pg.K_SPACE:
                title = False
            if event.key == pg.K_F11:
                if not fullscreen:
                    WIDTH = monitor.current_w
                    HEIGHT = monitor.current_h
                    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
                    fullscreen = True
                    title_rect.x += change_x
                    title_rect.y += change_y
                elif fullscreen:
                    WIDTH = 1000
                    HEIGHT = 700
                    screen = pg.display.set_mode((WIDTH, HEIGHT))
                    fullscreen = False
                    title_rect.x -= change_x
                    title_rect.y -= change_y

    screen.fill(BG_COLOUR)
    if fr:
        screen.blit(title1, title_rect)
    else:
        screen.blit(title2, title_rect)
    fr = not fr
    pg.display.update()
    clock.tick(2)

# BEGINNING CUTSCENE
bg_cs_fade_in()

while b_cut_screen:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        show_cut_screen()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                fade_out_cs()
                change_cut_screen()
                if current_cut_screen >= 6:
                    break
                fade_in_cs()

    pg.display.update()
    clock.tick(2)

# GAME LOOP
if fullscreen:
    soph.rect.x += change_x
    soph.rect.y += change_y
    soph.horizontal_rect.x += change_x
    soph.horizontal_rect.y += change_y
    soph.vertical_rect.x += change_x
    soph.vertical_rect.y += change_y
    inventory_background_rect.x += change_x
    inventory_background_rect.y += change_y
    inventory_pick_rect.x += change_x
    inventory_pick_rect.y += change_y
    star1.rect.x += change_x
    star1.rect.y += change_y
    star2.rect.x += change_x
    star2.rect.y += change_y
    star3.rect.x += change_x
    star3.rect.y += change_y
    star4.rect.x += change_x
    star4.rect.y += change_y
    star5.rect.x += change_x
    star5.rect.y += change_y
    star6.rect.x += change_x
    star6.rect.y += change_y
    room_rect = room.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
    coords = []
    with open(r"graphics\furniture\coords.txt", "r") as file:
        for line in file.readlines():
            coords.append(line.strip().split(","))
        for num, furn in enumerate(furniture):
            furniture[furn].rect.x = room_rect.x + int(coords[num][0])
            furniture[furn].rect.y = room_rect.y + int(coords[num][1])
fade_in()
cutscene_loop.stop()
game_loop.play(loops=-1)
while True:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.MOUSEBUTTONUP:
            if game:
                cur = ""
                for star in answer:
                    if star.rect.collidepoint(pg.mouse.get_pos()):
                        current.append(star)
                        cur = star.name
                for star, click in zip(answer, current):
                    if star != click:
                        current = []
                        cur = ""
                if len(current) == 6:
                    game = False
                    win = True
                match cur:
                    case "":
                        popup_telescope = frame0
                    case star1.name:
                        popup_telescope = frame1
                    case star2.name:
                        popup_telescope = frame2
                    case star3.name:
                        popup_telescope = frame3
                    case star4.name:
                        popup_telescope = frame4
                    case star5.name:
                        popup_telescope = frame5
                    case star6.name:
                        popup_telescope = frame6
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                soph.priority.append("down")
                if inventory_open and slot_y != 3:
                    inventory_pick_rect.y += next_vertical
                    slot_y += 1
            elif event.key == pg.K_UP or event.key == pg.K_w:
                soph.priority.append("up")
                if inventory_open and slot_y != 1:
                    inventory_pick_rect.y -= next_vertical
                    slot_y -= 1
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                soph.priority.append("left")
                if inventory_open and slot_x != 1:
                    inventory_pick_rect.x -= next_horizontal
                    slot_x -= 1
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                soph.priority.append("right")
                if inventory_open and slot_x != 5:
                    inventory_pick_rect.x += next_horizontal
                    slot_x += 1
            if event.key == pg.K_F11:
                if not fullscreen:
                    WIDTH = monitor.current_w
                    HEIGHT = monitor.current_h
                    screen = pg.display.set_mode((WIDTH, HEIGHT), pg.FULLSCREEN)
                    soph.rect.x += change_x
                    soph.rect.y += change_y
                    soph.horizontal_rect.x += change_x
                    soph.horizontal_rect.y += change_y
                    soph.vertical_rect.x += change_x
                    soph.vertical_rect.y += change_y
                    inventory_background_rect.x += change_x
                    inventory_background_rect.y += change_y
                    inventory_pick_rect.x += change_x
                    inventory_pick_rect.y += change_y
                    star1.rect.x += change_x
                    star1.rect.y += change_y
                    star2.rect.x += change_x
                    star2.rect.y += change_y
                    star3.rect.x += change_x
                    star3.rect.y += change_y
                    star4.rect.x += change_x
                    star4.rect.y += change_y
                    star5.rect.x += change_x
                    star5.rect.y += change_y
                    star6.rect.x += change_x
                    star6.rect.y += change_y
                    fullscreen = True
                elif fullscreen:
                    WIDTH = 1000
                    HEIGHT = 700
                    screen = pg.display.set_mode((WIDTH, HEIGHT))
                    soph.rect.x -= change_x
                    soph.rect.y -= change_y
                    soph.horizontal_rect.x -= change_x
                    soph.horizontal_rect.y -= change_y
                    soph.vertical_rect.x -= change_x
                    soph.vertical_rect.y -= change_y
                    inventory_background_rect.x -= change_x
                    inventory_background_rect.y -= change_y
                    inventory_pick_rect.x -= change_x
                    inventory_pick_rect.y -= change_y
                    star1.rect.x -= change_x
                    star1.rect.y -= change_y
                    star2.rect.x -= change_x
                    star2.rect.y -= change_y
                    star3.rect.x -= change_x
                    star3.rect.y -= change_y
                    star4.rect.x -= change_x
                    star4.rect.y -= change_y
                    star5.rect.x -= change_x
                    star5.rect.y -= change_y
                    star6.rect.x -= change_x
                    star6.rect.y -= change_y
                    fullscreen = False
                room_rect = room.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 40))
                coords = []
                with open(r"graphics\furniture\coords.txt", "r") as file:
                    for line in file.readlines():
                        coords.append(line.strip().split(","))
                    for num, furn in enumerate(furniture):
                        furniture[furn].rect.x = room_rect.x + int(coords[num][0])
                        furniture[furn].rect.y = room_rect.y + int(coords[num][1])
            if event.key == pg.K_i or event.key == pg.K_ESCAPE:
                interact.play()
                inventory_open = not inventory_open
                dialogue_open = False
                inventory_pick_rect.x = inventory_background_rect.x + 6 * 3
                inventory_pick_rect.y = inventory_background_rect.y + 6 * 3
                slot_x = 1
                slot_y = 1
            if event.key == pg.K_SPACE:
                if not inventory_open and soph.interaction():
                    if not dialogue_open:
                        interact.play()
                        dialogue_open = True
                    elif dialogue_open:
                        dialogue_open = False
                elif inventory_open and soph.interaction():
                    interact.play()
                    dialogue_open = not dialogue_open
                    inventory_open = False
                elif inventory_open:
                    interact.play()
                    inventory_open = False
                elif beginning:
                    interact.play()
                    beginning = False
                    dialogue_open = False
                elif game:
                    interact.play()
                    game = False
                    dialogue_open = False
        if event.type == pg.KEYUP:
            if event.key == pg.K_DOWN or event.key == pg.K_s:
                soph.priority.remove("down")
            elif event.key == pg.K_UP or event.key == pg.K_w:
                soph.priority.remove("up")
            elif event.key == pg.K_LEFT or event.key == pg.K_a:
                soph.priority.remove("left")
            elif event.key == pg.K_RIGHT or event.key == pg.K_d:
                soph.priority.remove("right")

    screen.fill(BG_COLOUR)
    screen.blit(room, room_rect)
    backfurniture_group.draw(screen)

    if safe:
        if blue:
            screen.blit(furniture["blue_gem"].image, furniture["blue_gem"].rect)
        if pink:
            screen.blit(furniture["pink_gem"].image, furniture["pink_gem"].rect)
        if purple:
            screen.blit(furniture["purple_gem"].image, furniture["purple_gem"].rect)

    screen.blit(soph.player, (soph.rect.x, soph.rect.y - soph.rect.height * 2))

    # coloured hitboxes for testing purposes

    # pg.draw.rect(screen, "pink", (soph.rect.x, soph.rect.y, soph.rect.width, soph.rect.height))
    # pg.draw.rect(screen, "pink", (cover.rect.x, cover.rect.y, cover.rect.width, cover.rect.height))
    # pg.draw.rect(screen, "red", (soph.horizontal_rect.x, soph.horizontal_rect.y,
    #                              soph.horizontal_rect.width, soph.horizontal_rect.height))
    # pg.draw.rect(screen, "green", (soph.vertical_rect.x, soph.vertical_rect.y,
    #                                soph.vertical_rect.width, soph.vertical_rect.height))
    # pg.draw.rect(screen, "pink", (furniture["painting"].rect.x, furniture["painting"].rect.y,
    #                               furniture["painting"].rect.width, furniture["painting"].rect.height))

    if not inventory_open and not dialogue_open:
        soph.move()

    for furn in frontfurniture_group:
        if furn is not furniture["cover"]:
            screen.blit(furn.image, (furn.rect.x, furn.rect.y - furn.rect.height // 2))
        else:
            screen.blit(furn.image, furn.rect)

    if beginning:
        dialogue("Damn it! I need to get out of here and save Venus!")

    if inventory_open:
        screen.blit(fade, room_rect)
        screen.blit(inventory_background, inventory_background_rect)
        screen.blit(inventory_pick, inventory_pick_rect)

        for coord, item in zip(slots, inventory):
            item.rect.x = inventory_background_rect.x + coord[0]
            item.rect.y = inventory_background_rect.y + coord[1]
            screen.blit(item.image, item.rect)

        for item in items_group:
            if inventory_pick_rect.colliderect(item.rect):
                dialogue(items[item.name].desc)

    if pink and blue and purple and dialogue_open and soph.interaction() == "safe":
        if items["knife"] not in inventory:
            furniture["safe"].desc = "Obtained: a knife."
            inventory.append(items["knife"])

    if dialogue_open:
        if soph.interaction() in has_items:
            match soph.interaction():
                case "drawer_lr":
                    if items["ocular"] not in inventory:
                        furniture["drawer_lr"].desc = "Obtained: an eyepiece."
                        inventory.append(items["ocular"])
                        has_items.remove("drawer_lr")
                case "drawer_br":
                    if items["rubber_gloves"] not in inventory:
                        furniture["drawer_br"].desc = "Obtained: a pair of gloves."
                        inventory.append(items["rubber_gloves"])
                        has_items.remove("drawer_br")
                case "table_1":
                    if items["empty_glass"] not in inventory:
                        furniture["table_1"].desc = "Obtained: an empty glass."
                        inventory.append(items["empty_glass"])
                        all_furniture.remove(furniture["glass"])
                        backfurniture_group.remove(furniture["glass"])
                        has_items.remove("table_1")
                case "desk_2":
                    if items["flashlight"] not in inventory:
                        furniture["desk_2"].desc = "Obtained: a flashlight."
                        inventory.append(items["flashlight"])
                        has_items.remove("desk_2")
                case "crack":
                    if items["golden_key"] not in inventory:
                        furniture["crack"].desc = "Obtained: a golden key."
                        inventory.append(items["golden_key"])
                        has_items.remove("crack")

    if dialogue_open:
        if soph.interaction() == "hallway" or soph.interaction() == "hallway_2":
            dialogue_open = False
        elif not inventory_inside() and soph.interaction():
            match soph.interaction():
                case "desk_1":
                    screen.blit(fade, room_rect)
                    screen.blit(popup_computer, inventory_background_rect)
                case "telescope":
                    if furniture["telescope"].desc == "You can see the stars. [USE MOUSE]":
                        if not win and items["purple_gem"] not in inventory:
                            game = True
                            pg.mouse.set_visible(True)
                        if win:
                            furniture["telescope"].desc = "Obtained: purple gem"
                            inventory.append(items["purple_gem"])
                            win = False
                            pg.mouse.set_visible(False)
                        screen.blit(fade, room_rect)
                        screen.blit(popup_telescope, inventory_background_rect)
                case "wardrobe":
                    screen.blit(fade, room_rect)
                    screen.blit(popup_wardrobe, inventory_background_rect)
            dialogue(furniture[soph.interaction()].desc)
        if inventory_inside() and soph.interaction():
            match inventory_inside(), soph.interaction():
                case "flashlight", "bed":
                    furniture["bed"].desc = "Obtained: a screwdriver"
                    inventory.append(items["screwdriver"])
                    inventory.remove(items["flashlight"])
                    items_group.remove(items["flashlight"])
                case "golden_key", "cover":
                    frontfurniture_group.remove(furniture["cover"])
                    all_furniture.remove(furniture["cover"])
                    inventory.remove(items["golden_key"])
                    items_group.remove(items["golden_key"])
                    dialogue_open = False
                case "screwdriver", "painting":
                    all_furniture.remove(furniture["painting"])
                    backfurniture_group.remove(furniture["painting"])
                    furniture["safe"].rect.height += 12 * 3
                    safe = True
                    inventory.remove(items["screwdriver"])
                    items_group.remove(items["screwdriver"])
                case "pink_gem", "safe":
                    pink = True
                    inventory.remove(items["pink_gem"])
                    items_group.remove(items["pink_gem"])
                    furniture["safe"].desc = "There are gems on the door. Some are missing."
                case "blue_gem", "safe":
                    blue = True
                    inventory.remove(items["blue_gem"])
                    items_group.remove(items["blue_gem"])
                    furniture["safe"].desc = "There are gems on the door. Some are missing."
                case "purple_gem", "safe":
                    purple = True
                    inventory.remove(items["purple_gem"])
                    items_group.remove(items["purple_gem"])
                    furniture["safe"].desc = "There are gems on the door. Some are missing."
                case "rubber_gloves", "trash":
                    furniture["trash"].desc = "Obtained: a folded paper"
                    inventory.append(items["folded_paper"])
                    inventory.remove(items["rubber_gloves"])
                    items_group.remove(items["rubber_gloves"])
                case "folded_paper", "mirror":
                    furniture["mirror"].desc = "Obtained: a blue gem"
                    inventory.append(items["blue_gem"])
                    inventory.remove(items["folded_paper"])
                    items_group.remove(items["folded_paper"])
                case "full_glass", "big_flower":
                    furniture["big_flower"].desc = "Obtained: a pink gem"
                    furniture["big_flower"].image = pg.image.load(r"graphics\furniture\flower-blooming.png")
                    furniture["big_flower"].image.set_colorkey((5, 0, 255))
                    furniture["big_flower"].rect.y -= 9
                    inventory.append(items["pink_gem"])
                    inventory.remove(items["full_glass"])
                    items_group.remove(items["full_glass"])
                case "empty_glass", "sink":
                    furniture["sink"].desc = "Obtained: water"
                    inventory.append(items["full_glass"])
                    inventory.remove(items["empty_glass"])
                    items_group.remove(items["empty_glass"])
                case "ocular", "telescope":
                    furniture["telescope"].desc = "You can see the stars. [USE MOUSE]"
                    inventory.remove(items["ocular"])
                    items_group.remove(items["ocular"])
                case "knife", "bunny":
                    furniture["bunny"].desc = "Obtained: a silver key."
                    furniture["bunny"].image = pg.image.load(r"graphics\furniture\bunny-torn.png")
                    furniture["bunny"].image.set_colorkey((5, 0, 255))
                    inventory.append(items["silver_key"])
                    inventory.remove(items["knife"])
                    items_group.remove(items["knife"])
                case "silver_key", "door":
                    fade_out()
                    break
                case _:
                    dialogue_open = False

    # for star in answer:
    #     pg.draw.rect(screen, "pink", (star.x, star.y, star.width, star.height))

    if items["screwdriver"] in inventory and not dialogue_open:
        furniture["bed"].desc = "The bed is neatly made."
    if items["folded_paper"] in inventory and not dialogue_open:
        furniture["trash"].desc = "Just trash."
    if items["blue_gem"] in inventory and not dialogue_open:
        furniture["mirror"].desc = "A regular mirror."
    if items["full_glass"] in inventory and not dialogue_open:
        furniture["sink"].desc = "A sink. It’s only been used once."
    if items["pink_gem"] in inventory and not dialogue_open:
        furniture["big_flower"].desc = "A beautiful flower bloomed."
    if items["knife"] in inventory and not dialogue_open:
        furniture["safe"].desc = "It's unlocked."
    if items["ocular"] in inventory and not dialogue_open:
        furniture["drawer_lr"].desc = "It's an empty drawer."
    if items["golden_key"] in inventory and not dialogue_open:
        furniture["crack"].desc = "There’s a slight crack in the wall."
    if items["silver_key"] in inventory and not dialogue_open:
        furniture["bunny"].desc = "Poor bunny."
    if items["rubber_gloves"] in inventory and not dialogue_open:
        furniture["drawer_br"].desc = "It's an empty drawer."
    if items["empty_glass"] in inventory and not dialogue_open:
        furniture["table_1"].desc = "A table."
    if items["flashlight"] in inventory and not dialogue_open:
        furniture["desk_2"].desc = "It's an empty drawer."
    if items["purple_gem"] in inventory and not dialogue_open:
        furniture["telescope"].desc = "You can see the stars."

    if not dialogue_open and not inventory_open:
        inventory_pick_rect.x = 1000
        inventory_pick_rect.y = 1000
        game = False

    if not game:
        pg.mouse.set_visible(False)

    screen.blit(
        (font.render("[SPACE] interact / use item    [I] inventory     [F11] fullscreen", False, (73, 36, 64))),
        (room_rect.x - 3 * 3, room_rect.y - 20 * 3))

    pg.display.update()
    clock.tick(FPS)

# game_loop.stop() # i think it's better to keep the music here
# cutscene_loop.play()

# END CUTSCENE
end_cs_fade_in()
while e_cut_screen:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

        show_cut_screen_e()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                fade_out_e()
                change_cut_screen_e()
                if current_cut_screen_e >= 9:
                    break
                fade_in_e()

    pg.display.update()
    clock.tick(2)

# CREDITS
credits_sc = True
bunny = True
bunny_pic = pg.image.load(r"graphics\story\bunny.png").convert()
bunny_rect = bunny_pic.get_rect(center=(WIDTH // 2, HEIGHT // 2))
while credits_sc:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                if bunny:
                    bunny = False
                else:
                    credits_sc = False
            if event.key == pg.K_F11:
                fullscreen = False
                WIDTH = 1000
                HEIGHT = 700
                screen = pg.display.set_mode((WIDTH, HEIGHT))
                bunny_rect.x -= change_x
                bunny_rect.y -= change_y
                room_rect.x -= change_x
                room_rect.y -= change_y
    screen.fill(BG_COLOUR)
    cr_y = 7 * 3
    credit = "                          > CREDITS <$$ART: YOKOMONE$$MUSIC: MILENSKI$$WRITING:" \
             " YANSHI AND YOKOMONE$$CUTSCENES CODE: YANSHI$GAMEPLAY CODE: YOKOMONE"
    credit = credit.split("$")
    for txt in credit:
        screen.blit((font.render(txt, False, (255, 255, 255))),
                    (room_rect.x + 50 * 3, room_rect.y + cr_y * 3))
        cr_y += 10
    if bunny:
        screen.blit(bunny_pic, bunny_rect)
    pg.display.update()
