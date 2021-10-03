import json

card_values = {
    'J' : 10,
    'Q' : 10,
    'K' : 10,
    'A' : 1
} 

card_suits = ['Hearts', 'Diamonds', 'Clubs', 'Spades']

class Card:
    def __init__(self, card_type, suite):
        self.card_type = card_type
        self.suite = suite
        self.value = card_type if type(card_type) == int else card_values[card_type]
        self.card_name = str(card_type) + ' of ' + suite
    @staticmethod
    def count_value(cards):
        value = 0
        for card in cards:
            if type(card) == str:
                card = json.loads(card)
                value += int(card['value'])
            else:
                value += card.value
        return value
        
    def to_json(self):
        return json.dumps(self.__dict__)

def create_deck():
    deck = []
    for number in range(1, 11):
        for suite in card_suits:
            deck.append(Card(number, suite))
    for lettered_card in card_values:
        for suite in card_suits:
            deck.append(Card(lettered_card, suite))
    return deck

