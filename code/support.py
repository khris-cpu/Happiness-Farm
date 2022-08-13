from  os import walk
import pygame

## import any folder
def import_folder(path) :
    surface_list = []

    for _, __ , img_files in walk(path):
        for image in img_files:
            full_path = path + "/"+ image
            image_surf = pygame.image.load(full_path).convert_alpha() ## Load Image and Convert
            surface_list.append(image_surf)

    return surface_list  ## List That have all image that already convert