import random

from google.appengine.ext import db

class Card(object):
  card_number = db.IntegerProperty()

  def __init__(self, card_number):
    self.card_number = card_number

class Deck(db.Model):
  cards = db.ListProperty(int)
  discards = db.ListProperty(int)

  def __init__(self):
    self.cards = range(0,52) 

class Player(db.Model):
  player_nick = db.StringProperty()

class Game(db.Model):
  players = db.ReferenceProperty(Player)
  game_deck = db.ReferenceProperty(Deck)
  in_progress = db.BooleanProperty()
