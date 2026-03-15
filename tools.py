import sys
import os

#prüfen ob .exe und gegebenenfalls Pfad anpassen
def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return relative_path


#Schriftgröße berechnen
def calculate_font_size(items, button_width, button_height):
    longest =max(items, key=lambda item:len(item["text"]))  #Knopf mit längstem Text
    char_width = button_width /len(longest["text"])         #Wie breit darf der Text sein?
    return int(min(1.5*char_width, 0.7*button_height))      #Darf nicht in der Breite und nicht in der Länge überwiegen
