import random

class Card(object):
  card_number = IntegerProperty()

  def __init__(self, card_number):
    self.card_number = card_number

class Deck(db.Model):
  cards = ListProperty(Card)

  def __init__(self):
    for i in range(0,52): 
      self.cards.append(Card(i))
      #random.shuffle(self.cards)


class Player(db.Model):
  player_nick = StringProperty()

class GoFishGame(db.Model):
  players = ListProperty(Player)
  game_deck = ReferenceProperty(Deck)
