import pygame
import constants

class ButtonClass:
    def __init__(self, x, y, width, height, color=(0,0,0), text="", text_color=(255,255,255), font_size = 25, font_type = None, draw_shape="rect", hitbox_shape = None, image = None):
        # Position und Größe werden relativ zur Bildschirmgröße berechnet
        self.x = x
        self.y = y
        self.width = width
        self.height = height
          
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font_size = font_size
        self.font_type = font_type
        
        self.draw_shape = draw_shape
        self.hitbox_shape = hitbox_shape or draw_shape  # Standardmäßig gleiche Form
        
        self.button_hitbox = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.image = None
        if image:   
            if isinstance(image, str):      #Wegem Kopie
                self.image = pygame.image.load(image).convert_alpha()   #Falls vorhanden: Bild reinladen
            else:
                self.image = image  
        
        # Schriftgröße abhängig von Buttonhöhe → skalierbar
        self.font = pygame.font.Font(font_type, int(self.font_size))
        
        
        #Hover-Wert
        self.hover_scale = 1.0
        self.target_scale = 1.0
        self.base_size = (self.x, self.y)
        
        #Bei non-image Knöpfen
        self.current_color = self.color
        self.hover_color = tuple(max(0,c-60) for c in self.color)
        #Ausgangsgrößen mit denen gerechnet wird
        self.original_x = x
        self.original_y = y
        self.original_width = width
        self.original_height = height

        
        
    def update_size_position(self, x, y, width, height):
        # Dynamisches Neupositionieren (z.B. Endscreen)
        scale_factor = min(width/self.width, height/self.height)
        
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.button_hitbox = pygame.Rect(self.x,self.y,self.width,self.height)
        
        self.font_size = self.font_size*scale_factor
        self.font = pygame.font.Font(self.font_type, int(self.font_size))
        
    def clone(self):
        return ButtonClass(
            self.x, self.y,
            self.width, self.height,
            self.color,
            text=self.text,
            text_color=self.text_color,
            font_size=self.font_size,
            font_type=self.font_type,
            draw_shape=self.draw_shape,
            hitbox_shape=self.hitbox_shape,
            image=self.image
    )
    def center_x_button(self):
        # Hilfsfunktion für Textpositionierung
        return self.x + 0.5*self.width
         
    def is_hovered(self, mouse_pos):
        mx, my = mouse_pos
        if self.hitbox_shape == "rect":
            return self.button_hitbox.collidepoint(mouse_pos)
        elif self.hitbox_shape == "ellipse":
            return self.in_ellipse_hitbox(mx, my)
        return False


    def border(self, screen, color):
        #Border um winning oder losing matchups zu markieren
        thickness = int(0.07*self.height)
        pygame.draw.ellipse(screen, color, self.button_hitbox.inflate(2*thickness, 2*thickness),width=thickness)
            
        
    def button_clicked(self, event):
        # Klickprüfung abhängig von Hitbox-Form
        if self.hitbox_shape == "rect":
            if event.type == pygame.MOUSEBUTTONDOWN and self.button_hitbox.collidepoint(event.pos):
                return True
        elif self.hitbox_shape == "ellipse":
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = event.pos
                return self.in_ellipse_hitbox(mx,my)
        return False
    
    def in_ellipse_hitbox(self,mx,my):
        cx = self.x + self.width / 2
        cy = self.y + self.height / 2
        rx = self.width / 2
        ry = self.height / 2
        # Mathematische Ellipsen-Gleichung für Trefferprüfung
        if ((mx-cx)**2)/(rx**2) + ((my-cy)**2)/(ry**2) <= 1:
            return True
        return False
    
    def animate(self, dt):
        mouse_pos = pygame.mouse.get_pos()
        speed = 20   #pro Sekunde
        if self.is_hovered(mouse_pos):
            self.target_scale = 1.2
            self.current_color = self.hover_color
        else: 
            self.target_scale = 1.0
            self.current_color = self.color 
        # Sanft annähern
        self.hover_scale += (self.target_scale - self.hover_scale) * speed * dt
        #Ab einer bestimmten Annäherung auf Zielwert springen
        if abs(self.hover_scale - self.target_scale) < 0.001:
            self.hover_scale = self.target_scale
        #Neue Größen -- immer vom Original ausgehen
        scaled_width = self.original_width * self.hover_scale
        scaled_height = self.original_height * self.hover_scale
        # Zentrieren damit er nicht nach rechts/unten wächst
        scaled_x = self.original_x + (self.original_width - scaled_width) / 2
        scaled_y = self.original_y + (self.original_height - scaled_height) / 2
        self.update_size_position(scaled_x, scaled_y, scaled_width, scaled_height)

    def draw_button(self, screen):
        # Dynamische Auswahl der Zeichenmethode
        draw_methods = {
            "rect": self.draw_rect_button,
            "ellipse": self.draw_ellipse_button,
            "image": self.draw_image_button
        }
        draw_methods.get(self.draw_shape, self.draw_rect_button)(screen)
        
    def draw_text_button(self, screen):
        # Zentrierter Text innerhalb der Hitbox
        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=self.button_hitbox.center)
        screen.blit(text_surface, text_rect)    
        
    def draw_rect_button(self, screen):
        pygame.draw.rect(screen, self.current_color, self.button_hitbox, border_radius=15)
        self.draw_text_button(screen)

    def draw_ellipse_button(self, screen):
        pygame.draw.ellipse(screen, self.current_color, self.button_hitbox)
        self.draw_text_button(screen)
        
    def draw_image_button(self, screen):
        # Bild wird auf Buttongröße skaliert
        if self.image is None:
            return
        scaled_image = pygame.transform.smoothscale(self.image, (int(self.width), int(self.height)))
        screen.blit(scaled_image, (self.x, self.y))

