import random
import os

# 1. Klass för kort
class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit
    
    def __str__(self):
        return f"{self.rank}{self.suit}"

# 2. Klass för kortlek
class Deck:
    def __init__(self):
        ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"]
        suits = ["♠", "♥", "♣", "♦"]
        self.cards = [Card(rank, suit) for rank in ranks for suit in suits]  # Skapar kortleken

    # 3. Spara kortleken till fil (med UTF-8-kodning)
    def save_to_file(self, filename="deck.txt"):
        try:
            with open(filename, "w", encoding="utf-8") as file:  # Ange UTF-8-kodning här
                for card in self.cards:
                    file.write(f"{card.rank},{card.suit}\n")
            print("Kortleken har sparats i filen.")
        except Exception as e:
            print(f"Fel vid sparande till fil: {e}")

    # 4. Läs in kortleken från fil (med UTF-8-kodning)
    def load_from_file(self, filename="deck.txt"):
        try:
            if not os.path.exists(filename):
                print(f"Filen '{filename}' finns inte. Skapar en ny kortlek.")
                return
            with open(filename, "r", encoding="utf-8") as file:  # Ange UTF-8-kodning här
                self.cards = []
                for line in file:
                    rank, suit = line.strip().split(",")
                    self.cards.append(Card(rank, suit))
            print("Kortleken har lästs in från filen.")
        except Exception as e:
            print(f"Fel vid läsning från fil: {e}")
            print("Skapar en ny kortlek.")
            self.__init__()  # Återställer kortleken om det blir ett fel

    def show_all_cards(self):
        for card in self.cards:
            print(card)

    def draw_card(self):
        if self.cards:
            drawn_card = self.cards.pop(0)  # Tar bort och returnerar det första kortet
            print(f"Du drog: {drawn_card}")  # Visar vilket kort som drogs
            return drawn_card
        else:
            print("Kortleken är tom!")
            return None

    def shuffle(self):
        random.shuffle(self.cards)   


# Skapa kortlek och hantera filer
deck = Deck()
deck.load_from_file()   # Försök läsa in kortlek från fil
deck.shuffle()          # Blandar kortleken
deck.show_all_cards()   # Visar alla kort
deck.draw_card()        # Drar ett kort och visar det
deck.save_to_file()     # Sparar den nya kortleken till fil
