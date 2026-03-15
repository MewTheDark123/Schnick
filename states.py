import pygame
import time
import constants
import tools # type: ignore
import Layout
from Logic import RPSLogic, ThreeLogic, FifteenLogic, TheRockLogic, SevenLogic, SheldonLogic, TheGrandmasterLogic
from Buttons import ButtonClass

class States:
    def __init__(self, previous_state=None, show_back_button=True):
        self.previous_state=previous_state
        self.show_back_button = show_back_button
        if self.show_back_button:
            back_width = 0.05*constants.SCREEN_WIDTH
            back_height = 0.05*constants.SCREEN_WIDTH
            back_x = 0.05*constants.SCREEN_WIDTH - back_width/2
            back_y = 0.05*constants.SCREEN_HEIGHT - back_height/2

            back_draw_shape = "image"
            back_hitbox_shape = "ellipse"
            back_image = tools.resource_path(f"buttons/back.png")
            self.back_button = ButtonClass(back_x, back_y, back_width, back_height, draw_shape=back_draw_shape,hitbox_shape=back_hitbox_shape, image=back_image)
    
    #Hover
    def update(self, dt):
        if self.show_back_button:
            self.back_button.animate(dt)


class MenuState(States):
    def __init__(self):
        super().__init__(show_back_button=False)
        # Start-Button für den Wechsel in den Handsign-Auswahl-State
        buttons_list = ["VS Computer", "Multiplayer", "Challange"]
        self.layout = Layout.VerticalLayout(buttons_list)
        self.vs_computer_button = self.layout.buttons[0]
        self.multiplayer_button = self.layout.buttons[1]
        self.challange_button = self.layout.buttons[2]

    def handle_events(self, events):
        # Prüft alle Events; wechselt State bei Klick
        for event in events:
            if self.vs_computer_button.button_clicked(event):
                return SchnickSelection(self)
            if self.challange_button.button_clicked(event):
                return ChallangerSelection(self)
        return None
    
    def draw(self, screen):
        # Hintergrund und Button zeichnen
        screen.fill(constants.SCREEN_BACKGROUND) 
        for button in self.layout.buttons:
            button.draw_button(screen)

    def update(self, dt):
        super().update(dt)  #zurück button
        for button in self.layout.buttons:
            button.animate(dt)


class ChallangerSelection(States):      #Noch keine Modi, Grandmaster Bild nur als Platzhalter - muss epischer sein
    def __init__(self, previous_state):
        super().__init__(previous_state)
        #Layout
        buttons_list = ["The Rock", "Sheldon", "The Grandmaster", "Seven"]
        layout = Layout.CircleLayout(buttons_list)
        # Dynamische Button-Erzeugung
        self.challangers_list = [{"name":item["text"], "button":button, "logic":self.choose_game_logic(item["text"])} for item, button in zip(layout.items, layout.buttons)]

    def choose_game_logic(self, mode):
        self.logic = {"3er_Schnick": RPSLogic(),
                      "15er_Schnick": FifteenLogic(),
                      "The Rock":TheRockLogic(),
                      "Seven":SevenLogic(),
                      "Sheldon":SheldonLogic(),
                      "The Grandmaster":TheGrandmasterLogic()}  
        return self.logic[mode]      
    
    def handle_events(self, events):
        # Prüft Klicks auf Buttons; generiert Ergebnis-State
        for event in events:
            for challanger in self.challangers_list:
                if challanger["button"].button_clicked(event):                  
                    return HandsignSelection(challanger["logic"], self)
            if self.back_button.button_clicked(event):
                return self.previous_state  
        return None

    def draw(self, screen):
        # Hintergrund und alle Buttons zeichnen
        screen.fill(constants.SCREEN_BACKGROUND)
        for challanger in self.challangers_list:
            challanger["button"].draw_button(screen)
        self.back_button.draw_button(screen)

    def update(self, dt):
        super().update(dt)  #zurück button
        for challanger in self.challangers_list:
            challanger["button"].animate(dt)


class SchnickSelection(States):
    def __init__(self, previous_state):
        super().__init__(previous_state)
        button_list =["3er Schnick", "15er Schnick"]
        self.layout = Layout.VerticalLayout(button_list)
        self.threeSchnick = self.layout.buttons[0]
        self.fifteenSchnick = self.layout.buttons[1]
    
    def handle_events(self, events):
        for event in events:
            if self.threeSchnick.button_clicked(event):
                return HandsignSelection(ThreeLogic(), self)
            elif self.fifteenSchnick.button_clicked(event):
                return HandsignSelection(FifteenLogic(), self)
            elif self.back_button.button_clicked(event):
                return self.previous_state                
        return None
    
    def draw(self, screen):
        # Hintergrund und Button zeichnen
        screen.fill(constants.SCREEN_BACKGROUND) 
        self.threeSchnick.draw_button(screen)
        self.fifteenSchnick.draw_button(screen)
        self.back_button.draw_button(screen)
            
    def update(self, dt):
        super().update(dt)  #zurück button
        for button in self.layout.buttons:
            button.animate(dt)     
            
               
class HandsignSelection(States):
    def __init__(self, logic, previous_state):
        super().__init__(previous_state)
        # Spiel-Logik für 3er Schnick-Schnack-Schnuc
        self.logic = logic
        #Layout
        layout = Layout.CircleLayout(self.logic.options)
        # Dynamische Button-Erzeugung
        self.handsigns_list = [{"name":item["text"], "button":button} for item, button in zip(layout.items, layout.buttons)]
    


    def handle_events(self, events):
        # Prüft Klicks auf Buttons; generiert Ergebnis-State
        for event in events:
            for handsign in self.handsigns_list:
                if handsign["button"].button_clicked(event):                  
                    player_input = handsign["name"]
                    self.logic.player_chooses(player_input)
                    outcome = self.logic.check()
                    time.sleep(0.2)      #Wartezeit für Spannung
                    return EndScreen(outcome, self.logic.p1, self.logic.p2, player_input, self.logic.p2_input, self.handsigns_list, self.logic, self.previous_state)
            if self.back_button.button_clicked(event):
                return self.previous_state  
        return None

    def draw(self, screen):
        # Hintergrund und alle Buttons zeichnen
        screen.fill(constants.SCREEN_BACKGROUND)
        for handsign in self.handsigns_list:
            handsign["button"].draw_button(screen)
        for handsign in self.handsigns_list:
            mouse_pos = pygame.mouse.get_pos()
            if handsign["button"].is_hovered(mouse_pos):
                self.beat_indicator(handsign["name"], screen)
        self.back_button.draw_button(screen)

    def update(self, dt):
        super().update(dt)  #zurück button
        for handsign in self.handsigns_list:
            handsign["button"].animate(dt)
    
    def beat_indicator(self, name, screen):
        for handsign in self.handsigns_list:
            if handsign["name"] in self.logic.rules[name]:
                handsign["button"].border(screen, constants.WIN_GREEN)
            elif handsign["name"] != name:
                handsign["button"].border(screen, constants.LOSE_RED)



class EndScreen(States):
    def __init__(self, outcome, p1, p2, p1_input, p2_input, handsigns_list, logic, previous_state_handsign_selection):
        super().__init__(show_back_button=False)
        self.handsigns_list = handsigns_list
        self.logic = logic
        self.previous_state_handsign_selection = previous_state_handsign_selection
        # Ergebnis, Spieler und gewählte Zeichen speichern
        self.outcome = outcome 
        self.p1 = p1
        self.p2 = p2
        self.p1_input = p1_input
        self.p2_input = p2_input
        
        #Gewählte Knöpfe
        self.p1_choice = self.find_button(self.p1_input)
        self.p2_choice = self.find_button(self.p2_input)

            #Bei einem Untentschieden Button verdoppeln
        if self.p1_choice == self.p2_choice:
            self.p2_choice = self.p1_choice.clone()

        #item für play again button
        self.layout = Layout.DuelLayout(self.p1_choice, self.p2_choice)
        
        # Button zum Neustarten
        self.play_again_button = self.layout.play_again_button
            
    def find_button(self, input):
        #Buttons zur jeweiligen Choice rausfinden
        for handsign in self.handsigns_list:
            if handsign["name"] == input:
                return handsign["button"]
        # Falls der Knopf nicht in der Liste ist, neuen Knopf mit richtigem Bild erstellen
        button = self.p1_choice.clone()
        button.image = pygame.image.load(tools.resource_path(f"buttons/{input}.png")).convert_alpha()
        button.text = input
        return button
    
    
    def draw(self, screen): 
        # Zeichnet Hintergrund, Buttons, Handzeichen und Ergebnis
        screen.fill(constants.SCREEN_BACKGROUND)
        
        #Auswahl-Buttons
        self.p1_choice.draw_button(screen)
        self.p2_choice.draw_button(screen)
        
        
        #Spieler-Labels
        self.draw_label(screen, self.p1, (self.layout.label_p1_x, self.layout.player_label_y), self.layout.player_label_size)
        self.draw_label(screen, self.p2, (self.layout.label_p2_x, self.layout.player_label_y), self.layout.player_label_size)
        
        #Symbol-Labels
        self.draw_label(screen, self.p1_input, (self.layout.label_p1_x, self.layout.symbol_label_y), self.layout.symbol_label_size)
        self.draw_label(screen, self.p2_input, (self.layout.label_p2_x, self.layout.symbol_label_y), self.layout.symbol_label_size)        
        
        #Vs
        self.draw_vs(screen)
        
        #Egebnis
        self.draw_outcome(screen)
        
        #Play-Again-Button
        self.play_again_button.draw_button(screen)
        

    
    def draw_outcome(self, screen):
        outcomes = {"p1_wins": ("You Win", (constants.WIN_GREEN), (constants.WIN_GREEN), (constants.LOSE_RED)),
                    "p2_wins" : ("You Lose", (constants.LOSE_RED), (constants.LOSE_RED), (constants.WIN_GREEN)),
                    "tie" : ("Tie", (0, 0, 0), None, None)
                    }    
        text, color, p1_border, p2_border = outcomes[self.outcome]
        outcome_font = pygame.font.Font(None, self.layout.outcome_size)
        if self.outcome != "tie":
            self.p1_choice.border(screen, p1_border)
            self.p2_choice.border(screen, p2_border)
        text_surface = outcome_font.render(text, True, color)
        text_rect = text_surface.get_rect(center = (self.layout.outcome_x, self.layout.outcome_y))
        screen.blit(text_surface, text_rect)
        
    
    def draw_label(self, screen, player_name, position, size):
        # Text oberhalb des gewählten Buttons
        label_font = pygame.font.Font(None, size)
        text_surface = label_font.render(player_name, True, self.layout.label_color)
        text_rect = text_surface.get_rect(center=(position))
        screen.blit(text_surface, text_rect)  
        
    def draw_vs(self,screen):
        vs_font = pygame.font.Font(self.layout.vs_font_type, self.layout.vs_size)
        text_surface = vs_font.render("Vs", True, self.layout.vs_color)
        text_rect = text_surface.get_rect(center=(self.layout.vs_x, self.layout.vs_y))
        screen.blit(text_surface, text_rect)  
        
    def handle_events(self, events):
        # Prüft Klick auf „Play again“; startet neues Spiel
        for event in events:
            if self.play_again_button.button_clicked(event):
                return HandsignSelection(self.logic, self.previous_state_handsign_selection)     #play again soll zurück zur Handsignselection
        return None
    
    def update(self, dt):
        self.play_again_button.animate(dt)  