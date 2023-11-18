import pygame, sys
from pytmx.util_pygame import load_pygame
maps = ['../Images/Maps/map1.tmx','../Images/Maps/map2.5.tmx','../Images/Maps/tutorial1.0.tmx']
BLUE_COLOR = 0
GREEN_COLOR = 1
RED_COLOR = 2
PINK_COLOR = 3
cooldown = 0
current_level = 0
pygame.init()
screen = pygame.display.set_mode((1680, 1000))
tmx_data = load_pygame(maps[current_level])
clock = pygame.time.Clock()
sprite_group = pygame.sprite.Group()
MOVEMENTSPEED = 5
health = 2
count = 0
boundary = []
blue = []
blue_pud = []
green = []
green_pud = []
red = []
red_pud = []
purple = []
purple_pud = []
win = []
winCon = pygame.image.load(("../Images/Objects/mushroom_3.png")).convert_alpha()
winCon = pygame.transform.scale(winCon, (1680, 1000))
playing = True
class SpriteSheet:

    def __init__(self, filename):
        """Load the sheet."""
        try:
            self.sheet = pygame.image.load(filename).convert_alpha()
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {filename}")
            raise SystemExit(e)


    def image_at(self, rectangle, colorkey = None):
        """Load a specific image from a specific rectangle."""
        # Loads image from x, y, x+offset, y+offset.
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size,pygame.SRCALPHA).convert_alpha()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey is -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)
        return image

    def images_at(self, rects, colorkey = None):
        """Load a whole bunch of images and return them as a list."""
        return [self.image_at(rect, colorkey) for rect in rects]

    def load_strip(self, rect, image_count, colorkey = None):
        """Load a whole strip of images, and return them as a list."""
        tups = [(rect[0]+rect[2]*x, rect[1], rect[2], rect[3])
                for x in range(image_count)]
        return self.images_at(tups, colorkey)

    def load_grid_images(self, num_rows, num_cols, x_margin=0, x_padding=0,
            y_margin=0, y_padding=0):
        """Load a grid of images.
        x_margin is space between top of sheet and top of first row.
        x_padding is space between rows.
        Assumes symmetrical padding on left and right.
        Same reasoning for y.
        Calls self.images_at() to get list of images.
        """
        sheet_rect = self.sheet.get_rect()
        sheet_width, sheet_height = sheet_rect.size

        # To calculate the size of each sprite, subtract the two margins,
        #   and the padding between each row, then divide by num_cols.
        # Same reasoning for y.
        x_sprite_size = ( sheet_width - 2 * x_margin
                - (num_cols - 1) * x_padding ) / num_cols
        y_sprite_size = ( sheet_height - 2 * y_margin
                - (num_rows - 1) * y_padding ) / num_rows

        sprite_rects = []
        for row_num in range(num_rows):
            for col_num in range(num_cols):
                # Position of sprite rect is margin + one sprite size
                #   and one padding size for each row. Same for y.
                x = x_margin + col_num * (x_sprite_size + x_padding)
                y = y_margin + row_num * (y_sprite_size + y_padding)
                sprite_rect = (x, y, x_sprite_size, y_sprite_size)
                sprite_rects.append(sprite_rect)

        grid_images = self.images_at(sprite_rects)
        print(f"Loaded {len(grid_images)} grid images.")

        return grid_images


class Player(pygame.sprite.Sprite):

    def __init__(self,pos,group):
        super().__init__(group)
        self.images = [
            SpriteSheet('../Images/Sprites/beeeiigcube1.2.png').load_grid_images(4, 1, x_margin=0, x_padding=0, y_margin=0, y_padding=0),
            SpriteSheet('../Images/Sprites/Green.png').load_grid_images(4, 1, x_margin=0, x_padding=0, y_margin=0, y_padding=0),
            SpriteSheet('../Images/Sprites/Red.png').load_grid_images(4, 1, x_margin=0, x_padding=0, y_margin=0, y_padding=0),
            SpriteSheet('../Images/Sprites/Pink.png').load_grid_images(4, 1, x_margin=0, x_padding=0, y_margin=0, y_padding=0)]
        self.image = self.images[0][0]
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.toggle = True
        self.togglesize = False
        self.size = 55
        self.color = 0
        self.cubecycle = 0
        rectangle = self.rect
        self.startpos = pos
    def next_level(self):
        global current_level
        current_level += 1

    def reset(self):
        global tmx_data

        self.image = self.images[0][0]
        self.color = 0
        self.rect = self.image.get_rect(center = self.startpos)
        tmx_data = load_pygame(maps[current_level])
        colorreset()
        draw_map()
    def input(self):
        global cooldown
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0
        if keys[pygame.K_LCTRL]:
            self.toggle = not self.toggle
        if self.toggle:
            self.speed = 10
        elif not self.toggle:
            self.speed = 5
        if keys[pygame.K_p]:
            # player.next_level()
            player.reset()

        if keys[pygame.K_b]:
            if cooldown == 0 and player.color != 3:
                self.color += 1
                cooldown = 10
            elif cooldown == 0 and player.color ==3:
                self.color = 0
                cooldown = 10


        # if keys[pygame.K_v]:
        #     self.image = pygame.image.load('../Images/Objects/New Piskel-1.png.png')
        #     self.size = 32


    def update(self):
        self.input()
        # if player.rect.collidelistall()
        future = pygame.Rect([self.rect.x, self.rect.y, self.size,self.size])
        future.center += self.direction * self.speed
        if not checkbounds(future,player.color):
            self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = pygame.math.Vector2()

    def custom_draw(self):
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            # player.color = 1
            player.image = player.images[player.color][player.cubecycle]
            screen.blit(sprite.image,sprite.rect)
camera_group = CameraGroup()
class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)

def checkbounds(playerrec,color):
    global blue, playing
    check = False
    if (playerrec.collidelistall(blue_pud)):  # this tests every tile with the player rectangle for blue puddle
        player.color = BLUE_COLOR
        player.togglesize = True
    if (playerrec.collidelistall(green_pud)):  # this tests every tile with the player rectangle
        player.color = GREEN_COLOR
        player.togglesize = False
    if (playerrec.collidelistall(red_pud)):  # this tests every tile with the player rectangle
        player.color = RED_COLOR
        player.togglesize = False
    if (playerrec.collidelistall(purple_pud)):  # this tests every tile with the player rectangle
        player.color = PINK_COLOR
        player.togglesize = False
    if (playerrec.collidelistall(win)):  # this tests every tile with the player rectangle
        gotoquick = 1
        if current_level == len(maps)-1:
            screen.blit((winCon),(0,0))
            playing = False
        else:
            player.next_level()
            player.reset()
    if color != BLUE_COLOR:
        if (playerrec.collidelistall(blue)):  # this tests every tile with the player rectangle
            check = True
    if color != GREEN_COLOR:
        if (playerrec.collidelistall(green)):  # this tests every tile with the player rectangle
            check = True
    if color != RED_COLOR:
        if (playerrec.collidelistall(red)):  # this tests every tile with the player rectangle
            check = True
    if color != PINK_COLOR:
        if (playerrec.collidelistall(purple)):  # this tests every tile with the player rectangle
            check = True
    if (playerrec.collidelistall(boundary)): #this tests every tile with the player rectangle
        check = True
    return check


def colorreset():
    global boundary, blue, blue_pud, green,green_pud,red,red_pud,purple,purple_pud,win
    boundary = []
    collision = tmx_data.get_layer_by_name('Collisions')
    for x, y, tile in collision:
        if tile:
            boundary.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    #Blue
    blue = []
    bluetiles = tmx_data.get_layer_by_name('BlueTiles')
    for x, y, tile in bluetiles:
        if tile:
            blue.append(pygame.Rect([(x*32), (y*32), 32, 32]));

    blue_pud = []
    blue_puddle = tmx_data.get_layer_by_name('BluePuddle')
    for x, y, tile in blue_puddle:
        if tile:
            blue_pud.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    #Blue

    #Green
    green = []
    greentiles = tmx_data.get_layer_by_name('GreenTiles')
    for x, y, tile in greentiles:
        if tile:
            green.append(pygame.Rect([(x*32), (y*32), 32, 32]));

    green_pud = []
    green_puddle = tmx_data.get_layer_by_name('GreenPuddle')
    for x, y, tile in green_puddle:
        if tile:
            green_pud.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    #Green

    #Red
    red = []
    redtiles = tmx_data.get_layer_by_name('RedTiles')
    for x, y, tile in redtiles:
        if tile:
            red.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    red_pud = []
    red_puddle = tmx_data.get_layer_by_name('RedPuddle')
    for x, y, tile in red_puddle:
        if tile:
            red_pud.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    #Red

    #purple
    purple = []
    purpletiles = tmx_data.get_layer_by_name('PurpleTiles')
    for x, y, tile in purpletiles:
       if tile:
           purple.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    purple_pud = []
    purple_puddle = tmx_data.get_layer_by_name('PurplePuddle')
    for x, y, tile in purple_puddle:
       if tile:
           purple_pud.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    #WinCondition/NextLevel
    win = []
    wintiles = tmx_data.get_layer_by_name('WinTiles')
    for x, y, tile in wintiles:
       if tile:
           win.append(pygame.Rect([(x*32), (y*32), 32, 32]));
    #WinCondition/NextLevel
colorreset()


# camera_group = pygame.sprite.Group()
#Go throuh layers
def draw_map():
    for layer in tmx_data.visible_layers:
        # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
         if hasattr(layer,'data'):
             for x,y,surf in layer.tiles():
                pos = (x * 32, y*32)
                Tile(pos = pos, surf = surf, groups = sprite_group)

    for obj in tmx_data.objects:
        pos = (obj.x, obj.y)
        if obj.image:
            Tile(pos = pos, surf=obj.image, groups = camera_group)
draw_map()
player = Player((64,64),camera_group)
while playing:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        # print(player.rect)
    sprite_group.update()
    sprite_group.draw(screen)
    camera_group.update()
    camera_group.custom_draw()
    for obj in tmx_data.objects:
        pos = (obj.x, obj.y)
        if obj.type == 'Shape':
            if obj.name == 'Marker':
                pygame.draw.circle(screen, 'red',(obj.x,obj.y),5)
            if obj.name == 'Rectangle':
                rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                pygame.draw.rect(screen,'yellow',rect)
            if obj.name == 'Elipse':
                rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                pygame.draw.ellipse(screen, 'blue', rect)
            if obj.name == 'Polygon':
                points = [(point.x,point.y) for point in obj.points]
                pygame.draw.polygon(screen,'green',points)

    if cooldown > 0:
        cooldown = cooldown - 1
        # print(cooldown)
    pygame.display.update()
    if count == 5:
        player.cubecycle += 1
        if player.cubecycle > 3:
            player.cubecycle = 0
        # print (player.cubesize)
    if count == 10  :
        count = 0
    else:
        count += 1
        clock.tick(30)
while True:
    for events in pygame.event.get():  # get all pygame events
        if events.type == pygame.QUIT:  # if event is quit then shutdown window and program
            pygame.quit()
            sys.exit()