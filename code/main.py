import pygame, sys
from pytmx.util_pygame import load_pygame

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)


pygame.init()
screen = pygame.display.set_mode((1280,720))
tmx_data = load_pygame('../Images/Maps/map1.tmx')
sprite_group = pygame.sprite.Group()

#Go throuh layers
for layer in tmx_data.visible_layers:
    # if layer.name in ('Floor', 'Plants and rocks', 'Pipes')
     if hasattr(layer,'data'):
         for x,y,surf in layer.tiles():
            pos = (x * 128, y*128)
            Tile(pos = pos, surf = surf, groups = sprite_group)

for obj in tmx_data.objects:
    pos = (obj.x, obj.y)
    if obj.type:
        Tile(pos = pos, surf=obj.image, groups = sprite_group)
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

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit

        screen.fill('black')
        sprite_group.draw(screen)
        
        for obj in tmx_data.objects:
            pos = (obj.x, obj.y)
            if obj.type == 'Shape':
                if obj.name == 'Marker':
                    pygame.draw.circ.e(screen, 'red',(obj.x,obj.y),5)
                if obj.name == 'Rectangle':
                    rect = pygame.Rect(obj.x,obj.y,obj.width,obj.height)
                    pygame.draw.rect(screen,'yellow',rect)
        pygame.display.update()