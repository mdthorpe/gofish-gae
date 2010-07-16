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

  def get_card_suit(self, card):
    suits = ["S","H","C","D"]
    index = card%4
    return suits[index] 

class Game(db.Model):
  in_progress = db.BooleanProperty()
  deck = db.ReferenceProperty(Hand)

  def log_event(self, player, description):
    game_event = GameEvent()
    game_event.game = self
    game_event.player = player
    game_event.description = description
    game_event.save()


class Player(db.Model):
  nickname = db.StringProperty()
  game = db.ReferenceProperty(Game)
  hand = db.ReferenceProperty(Hand)

  def is_ai_player(self):
    return False

  def get_hand_values(self):
    """
    Returns:
      a list of int card values that the player has
      in their hand.
    """
    player_cards = self.hand.get_cards()
    hand_values = set(player_cards)
    logging.debug(hand_values)
    return hand_values


  def take_cards(self, deck, num_cards):
    deck_cards = deck.get_cards()
    player_hand = self.hand.get_cards()

    for num in range(0,num_cards):
      if len(deck_cards) > 0:
        player_hand.append(deck_cards.pop(-1))

    deck.set_cards(deck_cards)
    self.hand.set_cards(player_hand)

  def ask_for_value(self, opponent, value):
    new_cards = opponent.take_by_value(value)

    self.game.log_event(self, "asked for " + opponent.nickname + "'s " + value + "'s")

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
    current_hand = self.hand.get_cards()
    new_cards = []
    for card in current_hand:
      card_value = self.hand.get_card_value(card)
      if card_value == value:
        new_cards.append(card)
        current_hand.remove(card)
    self.hand.set_cards(current_hand)
    self.save()
    return new_cards



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
      all_players.append(player)

    return random.choice(all_players)
    

  def random_card_value(self):
    value = random.randint(1,13)
    if value == "1": return "A"
    if value == "11": return "J"
    if value == "12": return "Q"
    if value == "13": return "K"
    return str(value)

class GameEvent(db.Model):
  game = db.ReferenceProperty(Game)
  player = db.ReferenceProperty(Player)
  description = db.StringProperty()
  time = db.DateTimeProperty(auto_now=True, auto_now_add=True)

