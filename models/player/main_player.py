import pygame as pg
from models.auxiliar import SurfaceManager as sf
from models.constantes import *
from world import World


class Jugador():
    def __init__(self, coordenada_x, coordenada_y, frame_rate = 100, speed_walk = 6, speed_run = 12,gravity = 28, delta_ms = 100, speed_jump = 20)-> None:
        self.__iddle_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\idle\\idle.png",6,1,) 
        self.__iddle_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\idle\\idle.png",6,1, flip = True)
        self.__walk_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\walk\\Walk.png",7,1,)
        self.__walk_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\walk\\Walk.png",7,1, flip = True)
        self.__jump_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\jump\\Jump.png",11,1,)
        self.__jump_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\jump\\Jump.png",11,1, flip = True)
        self.__run_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\run\\Run.png",8,1,)
        self.__run_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\run\\Run.png",8,1, flip = True)
        self.__shot_r = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\shot\\shot.png", 7, 1)
        self.__shot_l = sf.get_surface_from_sprisheet(".\\assets\\img\\player\\shot\\shot.png" ,7, 1, flip=True)
        
        ########################
        """IMAGES AND ANIMATION"""############
        ########################
        self.__actual_animation = self.__iddle_r #Tomamos la lista entera de surfaces. Contiene cada frame de la animacion
        self.__initial_frame = 0
        self.__player_animation_time = 0
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame] #Definimos cual va a ser el frame de toda la lista que comience la animacion
        self.__frame_rate = frame_rate
        self.__image = pg.image.load('assets\img\player\player.png')
        #########################
        """POSITION X AND Y"""############
        ########################
        self.__rect = self.__actual_image_animation.get_rect()
        self.__rect.x = coordenada_x
        self.__rect.y = coordenada_y
        #########################
        """COLISIONS"""############
        ########################
        self.rect_collission = pg.Rect(coordenada_x, coordenada_y, 40, 80)
        self.__widht = 40
        self.__height = 80
 
        #########################
        """MOVEMENT IN X AND Y"""############
        ########################
        self.__speed_walk = speed_walk #Velocidad de caminata
        self.__speed_run = speed_run #Velocidad corriendo
        self.__speed_jump = speed_jump
        self.__gravity = gravity
        
        ########################
        """FLAGS"""############
        ########################
        self.__on_ground = False
        self.__on_platform = False
        self.__is_looking_right = True
        self.__is_jumping = False        
        self.__is_shooting = False


        ########################
        self.delta_ms = delta_ms
        #######################
        ########################
        """MOVEMENTS"""############
        ########################
        self.__movement_in_x = 0
        """¡¡ATENCION!! NO CONFUNDIR MOVE_X CON COORDENADAS DE APARICION"""
        self.__movement_in_y = 0
        """¡¡ATENCION!! NO CONFUNDIR MOVE_Y CON COORDENADAS DE APARICION"""

    def __gravity_force(self, delta_ms):

        if self.__rect.bottom <= ALTO_VENTANA -50:

            self.__movement_in_y += self.__gravity * (delta_ms/self.__frame_rate)
            gravity_speed = 0
            if self.__movement_in_y > 10:
                    self.__movement_in_y = 10
                    gravity_speed += self.__movement_in_y
                    self.__movement_in_x = 0
                    self.__is_jumping = True
                    self.__on_ground= False
                    self.__on_platform = False
        else:
            gravity_speed = 0
            self.__movement_in_x = 0
            self.__is_jumping = False
            self.__on_ground = True
            self.__on_platform = True
        
        return gravity_speed
    def walk(self, direction_walk:str = 'Right'):
        x= 0
        match direction_walk:
            case 'Right':
                look_right = True
                if not self.__is_jumping:
                    x =self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    
                else:
                    x = self.__set_x_animations_preset(self.__speed_walk, self.__walk_r, look_r = look_right)
                    
            case 'Left':
                look_right = False
                if not self.__is_jumping:
                    x = self.__set_x_animations_preset(self.__speed_walk, self.__walk_l, look_r = look_right)
                    
                else:
                    x = self.__set_x_animations_preset(self.__speed_walk, self.__walk_l, look_r = look_right)
                    
        return x  
    def run(self, direction_walk: str = "Right"):
        print("Corriendo")
        if self.__is_jumping:
            x = self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = True)
        else:

            match direction_walk:
                case 'Right':
                    look_right = True
                    x = self.__set_x_animations_preset(self.__speed_run, self.__run_r, look_r = look_right)
                case 'Left':
                    look_right = False
                    x= self.__set_x_animations_preset(self.__speed_run, self.__run_l, look_r = look_right)
        return x
    def jump(self, delta_ms): 
        # print("ENTRO")
        y = 0
        x = 0
        if not self.__is_jumping:
            if self.__is_looking_right:
                y,x = self.__set_and_animations_preset_y(-self.__speed_jump, self.__jump_r, True, delta_ms)
            else:
                y,x = self.__set_and_animations_preset_y(-self.__speed_jump, self.__jump_l, False, delta_ms)

            self.__gravity_force(delta_ms)
        else:   
            y= 0
            x = 0
        return y, x
    def stay(self):
        print("stay")
        ####RESVISAR EL STAY PORQUE NO HACE BIEN SU FUNCIÓN
        if self.__on_ground or self.__on_platform:
            if not (self.__is_jumping and self.__is_shooting):
                # if self.__actual_animation not in (self.__shot_r, self.__shot_l): 
                    
                    if self.__actual_animation != self.__iddle_r or self.__actual_animation != self.__iddle_l:
                        self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
                        # self.__initial_frame = 0 
                        print("Quieto iddle")
                        self.__movement_in_x = 0
                        self.__movement_in_y = 0
            
            elif self.__is_shooting:
                if self.__actual_animation != self.__shot_r if self.__is_looking_right else self.__shot_l:
                    self.__actual_animation  = self.__shot_r if self.__is_looking_right else self.__shot_l
        else:
            if not self.__on_ground and self.__is_shooting:
                print("acá no entra mucho tiempo me pareceeeeeeeeeeeeeeeeeeeeeeee")
                self.__actual_animation = self.__shot_r if self.__is_looking_right else self.__shot_l
                self.__initial_frame = 0 
                
            else:
                self.__actual_animation = self.__jump_r if self.__is_looking_right else self.__jump_l
                self.__initial_frame = 0 
        return self.__movement_in_x
    def __set_x_animations_preset(self, speed_action_movement, animation_list: list, look_r:bool):
        """
        ¿Qué hace?
        El método 'set_x_animations_preset' permite modificar la posición horizontal en el eje x del main_player

        ¿Qué recibe?
        Recibe tres parámetros que son:
        'speed_action_movement'
        'animation_list': de tipo list. Que contiene cada frame de los spritesheet de los distintos movimientos 
        'look_r' : indica la direccion en donde está mirando el jugador
        ¿Qué devuelve?
        Retorna movement_in_x que es la cantidad de pixeles que se va a desplazar 'self.__rect.x' en el eje x
        """
        movement_in_x = 0
        
        self.__movement_in_x  = speed_action_movement
        if self.__actual_animation != animation_list:
            self.__actual_animation = animation_list
            self.__inital_frame = 0
        self.__is_looking_right = look_r
        if self.__is_looking_right:
            movement_in_x +=self.__movement_in_x
        else:
            movement_in_x += -self.__movement_in_x  

        return movement_in_x
    def __set_and_animations_preset_y(self, speed_action_movement,animation_list: list[pg.surface.Surface], look_r : bool, delta_ms):
        '''
        ¿Qué hace?
        El método '__set_and_animations_preset' permite modificar la posicion horiontal en el eje y del 'main_player'

        ¿Qué recibe?
        'speed_action_movement' la velocidad (cantidad de pixeles) en la que se va a desplazar 'self.__rect.x' en el eje x de la pantalla
        'animation_list': de tipo list. Que contiene cada frame de los spritesheet de los distintos movimientos 
        'look_r' : indica la direccion en donde está mirando el jugador
        ¿Qué devuelve?
        Retorna movement_in_y que es la cantidad de pixeles que se va a desplazar 'self.__rect.y' en el eje y de la pantalla
        '''
        self.__is_looking_right = look_r
        movement_in_y = 0
        movement_in_x = 0
        self.__movement_in_y = speed_action_movement
        self.__movement_in_x = 0
        # movement_in_y = -15
        # *( delta_ms / self.__frame_rate)
        '''
        'self.__movement_in_y' toma el valor del salto en negativo, puesto que controla el movimiento de la imagen de 'main_player'
        sobre el 'eje_y'
        '''
        # self.__movement_in_x = 0
        self.__movement_in_x = self.__speed_walk if self.__is_looking_right else -self.__speed_walk
        '''
        Estamos diciendo que los pixeles de movimiento sobre el 'eje_x' es igual a la velocidad de caminata (__speed_walk en positivo) siempre 
        y cuando el valor de '__is_looking_right' sea true. Ya que, eso garantiza que 'main_personaje' mira a la derecha. 
        Caso contrario será negativo '-__speed_walk' ya que de esta forma se desplazará hacia la izquieda en el eje x

        '''
        if self.__actual_animation != animation_list: #self.__jump_r if self.__is_looking_right else self.__jump_l
            self.__actual_animation = animation_list
            self.__initial_frame = 0
            
        '''
        establece que la animación actual ('__actual_animation') es igual a la lista que almacena las sprites recortadas del salto der
        ('__jump_r')  siempre y cuando '__is_looking_right' sea True. Caso contrario será ('__jump_l')
        '''

        #aaaa
        
        # if self.__initial_frame > len(self.__actual_animation) - 1:
        #     self.__actual_animation = self.__iddle_r if self.__is_looking_right else self.__iddle_l
        '''
        Seteamos con valor inicial de todos los sprites el indice 0. O sea el primero de la lista en '__actual_animation'
        '''
        self.__is_jumping = True
        '''
        Estado de salto en verdadero por que está saltando pero acá hay que cambiar algo, pues, salta y no puede quedar en verdadero, debe cambiar
        '''
        # self.__on_platform = False
        # self.__on_ground = False
        movement_in_y += self.__movement_in_y
        movement_in_x += self.__movement_in_x
        return movement_in_y, movement_in_x
    def do_animation(self, delta_ms):
        if DEBUG:
            print("DO ANIMATION DEBUG")
            
        self.__player_animation_time += delta_ms
        if DEBUG:
            print(f"Tiempo de animación{self.__frame_rate}")
            print(f"fotograma numero {self.__initial_frame} de {len(self.__actual_animation)}")
        if self.__player_animation_time >= self.__frame_rate:
            if DEBUG:
                print(f"REINICIO DE FRAME. SIGUIENTE ANIMACIÓN ")
            self.__player_animation_time = 0
            self.__initial_frame = (self.__initial_frame + 1) % len(self.__actual_animation)
    def moviment_control(self, key_get_pressed, delta_ms, world):
        #GET PRESSED KEY
        movement_in_x = 0
        movement_in_y = 0
        if not key_get_pressed[pg.K_LEFT] and not key_get_pressed[pg.K_RIGHT] and not self.__is_jumping:
            movement_in_x = self.stay()
        if key_get_pressed[pg.K_LEFT]:
            movement_in_x = self.walk("Left")
        if key_get_pressed[pg.K_RIGHT]:
            movement_in_x = self.walk("Right")
        if key_get_pressed[pg.K_LEFT] and key_get_pressed[pg.K_LSHIFT]:
            movement_in_x = self.run("Left")
        if key_get_pressed[pg.K_RIGHT] and key_get_pressed[pg.K_LSHIFT]:
            movement_in_x = self.run("Right")          
        if key_get_pressed[pg.K_SPACE]:
            print("SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS")
            movement_in_y, movement_in_x = self.jump(delta_ms)
            # if not self.__is_jumping:
            #     movement_in_x = self.__movement_in_x = self.__speed_walk/2 if self.__is_looking_right else -self.__speed_walk/2
            # else:
            #     movement_in_x = 0
            # movement_in_y, movement_in_x = self.jump(delta_ms)
            # self.__is_jumping = False
            # self.__on_ground = True
            # self.__on_platform = True
        #update player coordinates
        gravity = self.__gravity_force(delta_ms)
        movement_in_y += gravity
        collission_movement_in_y = self.check_colisions(world, movement_in_y)
        movement_in_y = collission_movement_in_y


        self.__rect.x += movement_in_x
        self.__rect.y += movement_in_y
        self.rect_collission.x = self.__rect.x+45
        self.rect_collission.y = self.__rect.y+50
        # self.__set_edges_limits()
        # self.__set_edge_limits_x()
        # self.__set_edge_limits_y()
    def draw(self, screen):
        #animacion actual
        self.__actual_image_animation = self.__actual_animation[self.__initial_frame]
        #posicion actual de la imagen
        self.__rect.y = min(self.__rect.y, ALTO_VENTANA - self.__actual_image_animation.get_height()) 
        
        #Dibujamos el rectangulo de colisón
        pg.draw.rect(screen, (255, 255, 255), self.rect_collission,2) 
        #bliteamos imagen actual
        screen.blit(self.__actual_image_animation, self.__rect) 

    def check_colisions(self, world, movement_in_y):
        for tile in world.tile_list:
             #ckeck for colission in y direction
             if tile [1].colliderect(self.rect_collission.x, self.rect_collission.y + self.__movement_in_y, self.__height, self.__height):
                #check below the ground - JUMPING
                if movement_in_y < 0:
                        movement_in_y = tile[1].bottom - self.rect_collission.top
                        self.__on_ground = False
                        self.__on_platform = False
                        self.__is_jumping = True
                #check below the ground - FALLING
                if movement_in_y >= 0:
                        movement_in_y = tile[1].top - self.rect_collission.bottom
                        self.__on_ground = True
                        self.__on_platform = True
                        self.__is_jumping = False
        return movement_in_y        
            
    def update(self,key_get_pressed, delta_ms,screen, world):
        #DRAW PLAYER
        self.draw(screen)
        
        
        #UPDATE PLAYER COORDINATES
        self.moviment_control(key_get_pressed, delta_ms, world)
        #ANIMATION
        self.do_animation(delta_ms)

        if DEBUG:
            print(f"X = {self.__rect.x}, Y = {self.__rect.y}")
            print(f"is jumping?: {self.__is_jumping}")
            print(f"on ground?: {self.__on_ground}")
            print(f"is on platform?: {self.__on_platform}")
            print(f"is looking right?: {self.__is_looking_right}")