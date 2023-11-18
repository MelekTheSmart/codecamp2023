import pygame, sys
from pytmx.util_pygame import load_pygame

cooldown = 0
class Player(pygame.sprite.Sprite):
    def __init__(self,pos,group):
        super().__init__(group)
        # self.image = pygame.image.load('../Images/Objects/mushroom_3.png')
        self.image = pygame.image.load('../Images/Objects/New Piskel-1.png.png')
        self.rect = self.image.get_rect(center = pos)
        self.direction = pygame.math.Vector2()
        self.speed = 5
        self.toggle = True
        self.togglesize = False
        self.size = 32

        rectangle = self.rect


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
            self.speed = 20
        elif not self.toggle:
            self.speed = 5
        if keys[pygame.K_b]:
            centerpos = (self.rect.center)
            if not self.togglesize and cooldown>=0:
                self.image = pygame.image.load('../Images/Objects/New Piskel-1.png (2).png')
                self.rect = self.image.get_rect(center=centerpos)
                self.size = 64
                self.togglesize = True
                cooldown = 10
                self.speed = 5
            elif self.togglesize and cooldown>=0:
                self.image = pygame.image.load('../Images/Objects/New Piskel-1.png.png')
                self.rect = self.image.get_rect(center=centerpos)
                self.size = 32
                self.togglesize = False
                cooldown = 10
                self.speed = 10
        # if keys[pygame.K_v]:
        #     self.image = pygame.image.load('../Images/Objects/New Piskel-1.png.png')
        #     self.size = 32


    def update(self):
        self.input()
        future = pygame.Rect([self.rect.x, self.rect.y, self.size,self.size])
        future.center += self.direction * self.speed
        if not checkbounds(future):
            self.rect.center += self.direction * self.speed

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()

        self.offset = pygame.math.Vector2()

    def custom_draw(self):
        for sprite in sorted(self.sprites(),key = lambda sprite: sprite.rect.centery):
            screen.blit(sprite.image,sprite.rect)

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
pygame.init()
screen = pygame.display.set_mode((1680, 1000))
tmx_data = load_pygame('../Images/Maps/map1.tmx')
clock = pygame.time.Clock()
sprite_group = pygame.sprite.Group()
camera_group = CameraGroup()
MOVEMENTSPEED = 5
health = 2
def checkbounds(playerrec):
    check = False
    if (playerrec.collidelistall(tiles)): #this tests every tile with the player rectangle
        check = True
    return check
tiles = []
collision = tmx_data.get_layer_by_name('Collisions')
for x, y, tile in collision:
    if tile:
        tiles.append(pygame.Rect([(x*128), (y*128), 128, 128]));
# camera_group = pygame.sprite.Group()
#Go throuh layers
for layer in tmx_data.visible_layers:
    # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
     if hasattr(layer,'data'):
         for x,y,surf in layer.tiles():
            pos = (x * 128, y*128)
            Tile(pos = pos, surf = surf, groups = sprite_group)

for obj in tmx_data.objects:
    pos = (obj.x, obj.y)
    if obj.image:
        Tile(pos = pos, surf=obj.image, groups = camera_group)
# print(tmx_data.layers)
#
# for layer in tmx_data.visible_layers:
#     print (layer)
#
# print(tmx_data.layernames)
#
# for obj in tmx_data.objectgroups:
#     print(obj)

# get tiles
# layer = tmx_data.get_layer_by_name('Floor')
# for x,y,surf in layer.tiles(): # get all the information
#     print(x * 128)
#     print(y * 128)
#     print(surf)
#
# print(layer.data)
# print(layer.name)
# print(layer.id)

# get objects
# object_layer = tmx_data.get_layer_by_name('Object Layer 1')
# for obj in object_layer:
#     if obj.type == "Building":
#         print(obj)


# for obj in tmx_data.objects:
#     # print(obj.x)
#     # print(obj.y)
#     # print(obj.image)
#     if obj.type() == 'Building':
#         print(obj)
player = Player((240,240),camera_group)
while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit
        # print(player.rect)
        if checkbounds(player.rect):
            print("help")
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
        clock.tick(120)