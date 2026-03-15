import random


class RPSLogic:
    def __init__(self, p1_input = None):
        self.options = []
        #players
        self.p1 = "Player"
        self.p2 = "Computer"
        #inputs
        self.p1_input = p1_input
        self.p2_input = None
        # Regeln werden dynamisch generiert → leicht erweiterbar
        self.rules = self.define_rules() 
    
    
    def define_rules(self):
        # Erzeugt für jedes Symbol die Liste der besiegten Symbole
        rules = {}
        n = len(self.options)
        beating_number = (n - 1) // 2  # jedes Element schlägt die Hälfte der anderen
        
        for i, elem in enumerate(self.options):
            beating = []
            for j in range(1, beating_number + 1):
                beaten_index = (i + j) % n  # zyklische Regel-Logik
                beating.append(self.options[beaten_index])
            rules[elem] = beating

        return rules

    def player_chooses(self, p1_input):
        self.p1_input = p1_input
        
    def computer_chooses(self):  
        # Zufällige KI-Entscheidung
        return random.choice(self.options) 
    
    def check(self):
        self.p2_input = self.computer_chooses()
        # Vergleich der Eingaben basierend auf generierten Regeln
        if self.p1_input == self.p2_input:
            return "tie"
        elif self.p2_input in self.rules[self.p1_input]:
            return "p1_wins"
        elif self.p1_input in self.rules[self.p2_input]:
            return "p2_wins"

class ThreeLogic(RPSLogic):
    def __init__(self, p1_input=None):
       # Spielvariante: 3er System
        super().__init__(p1_input) 
        self.options = ["paper", "rock", "scissors"]
        self.rules = self.define_rules() 
        
class FifteenLogic(RPSLogic):
    def __init__(self, p1_input=None):
        super().__init__(p1_input)
        self.options = ["rock", "fire","scissors", "snake","human","tree", "wolf","sponge","paper", "air", "water", "dragon","devil","lightning", "gun"]
        self.rules = self.define_rules()

        
        
class TheRockLogic(RPSLogic):
    def __init__(self, p1_input=None):
        super().__init__(p1_input)
        self.options = ["paper", "rock", "scissors"]
        self.rules = self.define_rules()
        self.p2 = "The Rock"
    
    def computer_chooses(self):
        return "rock"

class SevenLogic(RPSLogic):
    def __init__(self, p1_input=None):
        super().__init__(p1_input)
        self.options = ["paper", "rock", "scissors"]
        self.rules = self.define_rules()
        self.p2 = "Seven"
   
    def computer_chooses(self):
        if random.random() <0.2:
           return "Thousand Demon Daggers"        #zu 10% geht seven crazy mit seinem Schwert und gewinnt einfach
        else:                                           #Sonst macht er immer Schere
            return "Qi Scissors"
    
    def check(self):
        self.p2_input = self.computer_chooses()
        if self.p2_input == "Thousand Demon Daggers":
            return "p2_wins"
        elif self.p1_input == "scissors":
            return "tie"
        elif "scissors" in self.rules[self.p1_input]:
            return "p1_wins"
        elif self.p1_input in self.rules["scissors"]:
            return "p2_wins" 

class SheldonLogic(RPSLogic):
    def __init__(self, p1_input=None):
        super().__init__(p1_input)    
        self.options = ["paper", "rock", "scissors", "lizard", "spock"]
        self.rules = self.define_rules()
        self.p2 = "Sheldon"


class TheGrandmasterLogic(RPSLogic):
    def __init__(self, p1_input=None):
        super().__init__(p1_input)
        self.options = ["rock", "fire","scissors", "snake","human","tree", "wolf","sponge","paper", "air", "water", "dragon","devil","lightning", "gun"]
        self.rules = self.define_rules()
        self.p2 = "The Grandmaster"
    
    
    def computer_chooses(self):
        if random.random() <0.02:     #Wählt mit 2% Wahrscheninlichkeit zufällig
            return random.choice(self.options)
        else:                       #Sonst nimmt er immer das was den Gegner besiegt
            return random.choice(self.get_winning(self.p1_input)) 
    
    def get_winning(self, input):
        winning = []
        for option in self.options:
            if option != input and option not in self.rules[input]:
                winning.append(option)
        return winning