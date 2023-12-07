import pygame as pg

class SurfaceManager:
    
    @staticmethod
    def get_surface_from_sprisheet(img_path:str, cols: int, row: int, step = 1,  flip: bool = False) -> list[pg.surface.Surface]:
        sprites_list = list()
        surface_img = pg.image.load(img_path)
        frame_width = int(surface_img.get_width()/cols)
        frame_heigh = int(surface_img.get_height()/row)
        
        for row in range(row):
            
            for column in range(0, cols, step):
                x_asist = column *  frame_width
                y_asist = row * frame_heigh

                frame_surface = surface_img.subsurface(x_asist, y_asist, frame_width, frame_heigh)

                if flip:
                    frame_surface = pg.transform.flip(frame_surface, True, False)
                sprites_list.append(frame_surface)
        
        return sprites_list


