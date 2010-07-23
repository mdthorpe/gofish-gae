import random
import logging

from google.appengine.ext import db

class Hand(db.Model):
  cards = db.ListProperty(int)
  discards = db.ListProperty(int)

  def get_cards(self): 
    return self.cards

  def set_cards(self,new_cards):
    self.cards = new_cards
    self.save()
    return self.cards

  def get_fancy_cards(self):
    fancy_cards = []
    for card in self.cards:
      card_value = self.get_card_value(card)
      card_suit = self.get_card_suit(card)
      fancy_cards.append(card_value+card_suit)
    return fancy_cards

  def get_card_value(self, card):
    value = str((card/4)+1)
    if value == "1": return "A"
    if value == "11": return "J"
    if value == "12": return "Q"
    if value == "13": return "K"
    return value

  def get_cards_by_value(self, value):
    card_list = []
    for card in self.cards:
      if self.get_card_value(card) == value:
        card_list.append(card)
    return card_list

  def remove_cards_by_value(self, value):
    for card in self.cards:
      if self.get_card_value(card) == value:
        self.cards.remove(card)
    self.save()

  def get_card_suit(self, card):
    suits = ["S","H","C","D"]
    index = card%4
    return suits[index] 

  """
    Returns: A list of card values.
    This list can be used by AI players to guess with
  """
  def get_card_values(self):
    card_values = []
    for card in self.cards:
      card_values.append(self.get_card_value(card))
    card_values = list(set(card_values))
    return card_values

  """
    Returns: int count of all cards of a given value
  """
  def count_by_value(self, value):
    cards = self.get_cards_by_value(value)
    logging.debug(["count_by_value", value, len(cards)])
    return len(cards)


class Game(db.Model):
  in_progress = db.BooleanProperty()
  deck = db.ReferenceProperty(Hand)
  turn_number = db.IntegerProperty(default=1)

  def log_event(self, player, description):
    game_event = GameEvent()
    game_event.game = self
    game_event.player = player
    game_event.description = description
    game_event.turn_number = self.turn_number
    game_event.save()

  def new_turn(self):
    self.turn_number = self.turn_number + 1
    self.save()


class Player(db.Model):
  nickname = db.StringProperty()
  game = db.ReferenceProperty(Game)
  hand = db.ReferenceProperty(Hand)
  score = db.IntegerProperty(default=0)

  def is_ai_player(self):
    return False

  def take_cards(self, deck, num_cards):
    deck_cards = deck.get_cards()
    player_hand = self.hand.get_cards()

    for num in range(0,num_cards):
      if len(deck_cards) > 0:
        player_hand.append(deck_cards.pop(-1))

    deck.set_cards(deck_cards)
    self.hand.set_cards(player_hand)

  def ask_for_value(self, opponent, value):

    self.game.log_event(self, "asked for " + opponent.nickname + "'s " + value + "'s")
    new_cards = opponent.take_by_value(value)

    if len(new_cards) > 0:
      current_cards = self.hand.get_cards()
      current_cards.extend(new_cards)
      self.hand.set_cards(current_cards)
      self.save()
      return True
    else:
      self.take_cards(self.game.deck,1)
      self.game.log_event(self, " went fishing")
      return False
     
  def take_by_value(self, value):
    new_cards = self.hand.get_cards_by_value(value)
    self.hand.remove_cards_by_value(value)
    if len(new_cards) > 0:
      self.game.log_event(self, " gave up their " + value + "'s")
    return new_cards

  """
  Find groups of four cards of the same value.
  For each group increase score by 1 and remove the four cards
  """
  def search_books(self):
    card_values = self.hand.get_card_values()
    logging.debug(["card_values",card_values])
    for val in card_values:
      if self.hand.count_by_value(val) == 4:
        self.score_book(val)

  def score_book(self, value):
    self.hand.remove_cards_by_value(value)
    self.score = self.score + 1
    self.save()

class AiPlayer(Player):
  """
  Will eventually contain actual game logic methods
  like "do_turn"
  """
  def is_ai_player(self):
    return True

  def random_opponent(self):
    all_players = []

    # add human player
    all_players.append(Player.all().filter('game =', self.game.key()).fetch(1)[0])

    for player in AiPlayer.all().filter('game =', self.game.key()).fetch(10):
      if player.nickname != self.nickname:
       all_players.append(player)

    return random.choice(all_players)

  # Return a random card value from a players hand
  def random_card_value(self):
    card_values = self.hand.get_card_values()
    value = random.choice(card_values)
    return str(value)

class GameEvent(db.Model):
  game = db.ReferenceProperty(Game)
  player = db.ReferenceProperty(Player)
  description = db.StringProperty()
  turn_number = db.IntegerProperty()
  time = db.DateTimeProperty(auto_now=True, auto_now_add=True)

