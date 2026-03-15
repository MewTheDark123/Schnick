import math
import constants
import tools # type: ignore
from Buttons import ButtonClass


class BaseLayout:
    def calculate_font_size(self, items, button_width, button_height):
        longest =max(items, key=lambda item:len(item["text"]))  #Knopf mit längstem Text
        char_width = button_width /len(longest["text"])         #Wie breit darf der Text sein?
        return int(min(1.5*char_width, 0.7*button_height))      #Darf nicht in der Breite und nicht in der Länge überwiegen
        
class VerticalLayout(BaseLayout):
    def __init__(self, text_liste):
        self.items = [{"color":(126,54,164), "text":name, "text_color": (255,255,255), "font_type":None, "draw_shape":"rect"} for name in text_liste] 
        
        self.button_width = constants.SCREEN_WIDTH*0.3
        self.button_height = constants.SCREEN_HEIGHT*0.15
        self.spacing = constants.SCREEN_HEIGHT*0.05
        self.total_height = len(self.items)*self.button_height + len(self.items)*self.spacing
        font_size = tools.calculate_font_size(self.items, self.button_width, self.button_height)
        for item in self.items:
            item["font_size"] = font_size


        
        self.buttons = self.place_buttons_vertical()
    
    def place_buttons_vertical(self):
        buttons = []
        for i, item in enumerate(self.items):
            x = (constants.SCREEN_WIDTH-self.button_width)/2 
            y = (constants.SCREEN_HEIGHT-self.total_height)/2 + i*(self.button_height + self.spacing)
            buttons.append(ButtonClass(x,y,self.button_width,self.button_height, **item))
        return buttons
            
    

class CircleLayout(BaseLayout):
    def __init__(self, text_liste, center_x = 0.5*constants.SCREEN_WIDTH, center_y = 0.5*constants.SCREEN_HEIGHT):
        self.cx = center_x
        self.cy = center_y
        self.items = [{"color":(0,0,0), "text":name, "text_color": (255,255,255), "font_type":None, "draw_shape":"image", "hitbox_shape":"ellipse", "image": tools.resource_path(f"buttons/{name}.png")} for name in text_liste]    
        
        # Maximaler Radius damit Kreis auf Screen passt
        padding = constants.SCREEN_BASE*0.05    #kleiner Abstand zum Screen-Rand
        max_radius = min(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT) * 0.5 - padding
        
        
        # Optimale Größe und Radius berechnen
        self.radius, self.button_size = self.calculate_radius_and_size(max_radius)
        
        #Font size berechnen
        font_size = tools.calculate_font_size(self.items, self.button_size, self.button_size)
        for item in self.items:
            item["font_size"] = font_size
        

        self.buttons = self.place_buttons_circle()

    
    def calculate_radius_and_size(self, max_radius):
        if len(self.items) == 1:
            return max_radius * 0.3, max_radius * 0.3
        
        # Bedingungen: button_size = chord * 0.75 --> Button überlappen sich nicht (Button Size)
        # Und:         radius + button_size/2 ≤ max_radius --> Button passen auf Screen (Radius)
        #
        # chord = 2 * radius * sin(pi/n) ---- n ist Anzahl Buttons --> ist len(self.items)
        # button_size = chord * 0.75 = 2 * radius * sin(pi/n) * 0.75
        #
        # Einsetzen in Bedingung 2:
        # radius + radius * sin(pi/n) * 0.75 ≤ max_radius
        # radius * (1 + sin(pi/n) * 0.75) ≤ max_radius
        # radius ≤ max_radius / (1 + sin(pi/n) * 0.75)
        
        radius = max_radius / (1 + math.sin(math.pi / len(self.items)) * 0.75)
        chord = 2 * radius * math.sin(math.pi / len(self.items))
        button_size = chord * 0.75
        return radius, button_size


    def place_buttons_circle(self):
        buttons = []
        # Kreisförmige Anordnung der Buttons
        for i, item in enumerate(self.items):
            angle = math.radians(i * 360 / len(self.items))
            x = self.cx + self.radius * math.sin(angle) - self.button_size/2
            y = self.cy - self.radius * math.cos(angle) - self.button_size/2
            buttons.append(ButtonClass(x, y, self.button_size, self.button_size, **item))
        return buttons
    
    # def calculate_size(self):
    #     #Größe abhängig von Anzahl der Knöpfe
    #     angle_between = (2*math.pi)/len(self.items)
    #     distance = 2*self.radius * math.sin(angle_between / 2) #Geometrieformel für Abstand zweier Punkte
    #     size = distance*0.75 #0.75 als Puffer
    #     return size
    


class DuelLayout(BaseLayout):
    def __init__(self, button_p1, button_p2):
        
        #Space zwischen Labels und Buttons
        label_buttons_space = 0.05*constants.SCREEN_HEIGHT
        
        #Play again button
        #Größe
        self.play_again_width = constants.SCREEN_WIDTH*0.25
        self.play_again_height = constants.SCREEN_HEIGHT*0.08
        #item
        play_again_item = {"color":(0,0,0), "text":"Play Again", "text_color":(255, 255, 255), "font_type":None, "draw_shape":"rect"}
        
        #Choice-Buttons
        #Größe
        self.choice_size = constants.SCREEN_BASE*0.22
        #Positionen
        self.p1_x = constants.SCREEN_WIDTH*0.25 - self.choice_size/2    #Auswahl Spieler 1
        self.p2_x = constants.SCREEN_WIDTH*0.75 - self.choice_size/2    #Auswahl Spieler 2
        
        self.choice_y = constants.SCREEN_HEIGHT*0.4 - self.choice_size/2
        
        #Labels
        #Größe
        self.player_label_size = int(constants.SCREEN_HEIGHT*0.05)
        self.symbol_label_size = int(constants.SCREEN_HEIGHT*0.07)
        #Positionen
        self.label_p1_x = constants.SCREEN_WIDTH*0.25
        self.label_p2_x = constants.SCREEN_WIDTH*0.75
        
        self.player_label_y = self.choice_y - label_buttons_space
        self.symbol_label_y = self.choice_y + self.choice_size + label_buttons_space
        #Farbe
        self.label_color = (0,0,0)
        
        #Vs
        #Größe
        self.vs_size = int(self.choice_size) #gleich groß wie Buttons
        #Position -- gleich wie choice Buttons
        self.vs_x = constants.SCREEN_WIDTH*0.5
        self.vs_y = constants.SCREEN_HEIGHT*0.4
        #font
        self.vs_font_type = tools.resource_path("fonts/Bangers-Regular.ttf")
        #Farbe
        self.vs_color = (0,0,0)
                
        #Outcome 
        #Größe
        self.outcome_size = int(constants.SCREEN_HEIGHT*0.1)
        #Position
        self.outcome_x = constants.SCREEN_WIDTH*0.5
        self.outcome_y = constants.SCREEN_HEIGHT*0.625

        
        #Play Again Button Position
        self.play_again_x = constants.SCREEN_WIDTH*0.5-self.play_again_width/2
        self.play_again_y = constants.SCREEN_HEIGHT*0.78-self.play_again_height/2
        
        #Play Again Button Font size
        play_again_font_size = tools.calculate_font_size([play_again_item], self.play_again_width, self.play_again_height)
        play_again_item["font_size"] = play_again_font_size

        #Choice Buttons updaten
        button_p1.update_size_position(self.p1_x, self.choice_y, self.choice_size, self.choice_size)
        button_p2.update_size_position(self.p2_x, self.choice_y, self.choice_size, self.choice_size)
        
        
        #Play Again Button erstellen
        self.play_again_button = ButtonClass(self.play_again_x, self.play_again_y, self.play_again_width, self.play_again_height, **play_again_item)
