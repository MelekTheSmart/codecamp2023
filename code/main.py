import pygame, sys
from pytmx.util_pygame import load_pygame

pygame.init()
screen = pygame.display.set_mode((1280,720))
tmx_data = load_pygame('../Images/Maps/map1.tmx')

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
object_layer = tmx_data.get_layer_by_name('Object Layer 1')
for obj in object_layer:
    if obj.type == "Building":
        print(obj)


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
        pygame.display.update()