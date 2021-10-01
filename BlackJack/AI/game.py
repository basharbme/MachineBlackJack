import json
import random
try:
    from card import Card, create_deck
    from probability import probability_advice
except(ModuleNotFoundError):
    from AI.card import Card, create_deck

def value_if_not_none(value, alternative):
    return value if value != None else alternative


class Game:
    def __init__(self, files = None, files_lock = None, deck = None, state = None, chain = None):
        self.state = value_if_not_none(state, {
            "dealer" : [],
            "self" : []
        })
        self.chain =  value_if_not_none(chain, {})
        self.deck = value_if_not_none(deck, create_deck())
        self.files = files
        self.files_lock = files_lock

    def deal_card(self):
        card = random.choice(self.deck)
        self.deck.remove(card)
        return card

    def make_choice(self, dealer, player):
        res = probability_advice(self.deck, dealer, player)
        return 1 if res['hit'] > res['stay'] else 0
        
    
    
    def next_round(self, choice = None):
        end_game = False
        if len(self.chain) == 0:
            self.state['dealer'].append(self.deal_card())
            self.state['self'].append(self.deal_card())
            self.state['self'].append(self.deal_card())
            self.chain['data/root.txt'] = ''
        else:
            dealer = Card.count_value(self.state['dealer'])
            own = Card.count_value(self.state['self'])
            file_name = 'data/'+str(dealer) + "_" + str(own)+'.txt'
            choice = self.make_choice(dealer, own)
            if choice == '1':
                self.state['self'].append(self.deal_card())
                self.chain[file_name] = int(choice)
            else:
                end_game = True
        current_value = Card.count_value(self.state['self'])
        if current_value >= 21:
            end_game = True
        return end_game
    
    def finish_game(self):
        score = Card.count_value(self.state['self'])
        if score <= 21:
            while Card.count_value(self.state['dealer']) <= 13:
                self.state['dealer'].append(self.deal_card())
        won = (score <= 21 and score > Card.count_value(self.state['dealer']))
        #print(score, "is my score and ", Card.count_value(self.state['dealer']), "is the dealer's")
        #print(self.chain)
        return won     
    
    def learn(self, result):
        self.chain['data/root.txt'] = result
        for link in self.chain:
            if result:
                if self.files != None:
                    self.files[link].append(self.chain[link])
                else:
                    with open('BlackJack/AI/'+link, 'a') as file:
                        file.write(str(self.chain[link]))
            # else:
            #     print(self.chain[link])
            #     if self.files != None:
            #         self.files[link].append(str(not int(self.chain[link])))
            #     else:
            #         with open('BlackJack/AI/'+link, 'a') as file:
            #             file.write(str(not int(self.chain[link])))
            
    def to_json(self):
        res = {}
        res['deck'] = []
        res['dealer'] = []
        res['self'] = []
        res['chain'] = self.chain
        for card in self.deck:
            res['deck'].append((card.to_json() if type(card) != str else card))
        for card in self.state['dealer']:
            res['dealer'].append((card.to_json() if type(card) != str else card))
        for card in self.state['self']:
            res['self'].append((card.to_json() if type(card) != str else card))
        return json.dumps(res)
        