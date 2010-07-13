#!/usr/bin/env python

import random

"""
Custom exception classes
"""
class GameInProgress(Exception):
  def __init__(self, value):
    self.value = value
  def __str__(self):
    return repr(self.value)

"""
Game players
"""
class Player(object):
  opponents = list()
  books = list()

  def __init__(self,player_nick,game_deck):
    self.player_nick = player_nick
    self.hand = Hand()
    self.game_deck = game_deck

  def __str__(self):
    return self.player_nick

  def take_turn(self):
    print self.opponents

  def show_hand(self):
    s = ""
    for card in self.hand.cards:
      s = s + " | " + str(card)
    return s

  def count_books(self):
    for check_value in range(0,13):
      t_cards = 0
      for card in self.hand.cards:
        if card.get_value() == check_value:
          t_cards = t_cards + 1
      if t_cards == 4:
        print "Found book for " + str(card.get_value())
        cards_in_book = self.hand.collect_book(check_value)
        print cards_in_book
        self.books.extend(cards_in_book)

  def show_books(self):
    s = ""
    for card in self.books:
      s = s + str(card)
    return s

  def go_fish(self):
    try:
      self.hand.cards.append( self.game_deck.pick_from_top() )
    except:
      pass

"""
AI Player logic
"""
class AiPlayer(Player):

  """
  AI Player turn logic
  """
  def take_turn(self):
    print "---- TURN " + self.__str__() + " ----"

    print "My strating hand: " + self.show_hand()

    opponent = self.pick_opponent()
    print "Opponent: " + str(opponent)

    # Grab a random card from my hand and look at the value
    rnd_index = random.randint(0, len(self.hand.cards)-1 )
    card_value = self.hand.cards[rnd_index].get_value()
    print "Asking for: " + str(card_value)

    # Ask target for cards of card_value
    opponent_cards = opponent.ask_cards(card_value)
    if opponent_cards:
      self.hand.cards.extend(opponent_cards)
    else:
      print "Go Fish"
      self.go_fish()

    self.count_books()
    print self.show_books()
    print "My ending hand: " + self.show_hand()

  """
  Pick a target player
  """
  def pick_opponent(self):
    rnd_index = random.randint(0, len(self.opponents)-1 )
    return self.opponents[rnd_index]

  """
  An opponent player asks for cards of a certain face value.
  Returns a list of Cards that match the target value
  """
  def ask_cards(self,card_value):
    remit_cards = list()
    for card in self.hand.cards:
      if card.get_value() == card_value:
        print self.__str__() + " has card: " + card.__str__()
        remit_cards.append(card)
        self.hand.cards.remove(card)
    return remit_cards




"""
Playing Card
"""
class Card(object):
  SUITS = ['C','D','H','S']

  def  __init__(self,card_number):
    self.card_number = card_number
  
  def get_value(self):
    return (self.card_number%13)+1

  def get_suit(self):
    return self.SUITS[(self.card_number/13)]

  def __str__(self):
    return str(self.get_value()) + str(self.get_suit())

"""
A collection of playing cards
"""
class Hand(object):
  cards = list() # A list of Card objects

  def collect_book(self,card_value):
    book = list()
    for card in self.cards:
      if card.get_value() == card_value:
        book.append(card)
        self.cards.remove(card)
    print book
    return book


"""
Special Deck version of a Hand object. Used as the game deck
"""
class Deck(Hand):

  def __init__(self):
    for i in range(0,52): 
      self.cards.append(Card(i))
      random.shuffle(self.cards)

  def shuffle(self):
    random.shuffle(self.cards)

  def pick_from_top(self):
    return self.cards.pop(0)

"""
GoFish Game object. Handles game play.
"""
class GoFishGame(object):
  starting_hand_size = 7

  game_deck = None
  in_progress = False
  players = list()

  def __init__(self):
    self.game_deck = Deck()

  def add_player(self, player_nick, ai_player):
    if self.in_progress:
      raise GameInProgress("New players not allowed")

    if ai_player:
      self.players.append(AiPlayer(player_nick, self.game_deck))
    else:
      self.players.append(Player(player_nick, self.game_deck))

  def start_game(self):
    # Deal 7 Cards to players
    for player in self.players:
      player_hand = Hand()
      player_hand.cards = self.deal_from_deck(self.starting_hand_size)
      player.hand = player_hand

      # Create a list of Players that aren't this player
      # and assign them to the opponents list.
      opponents = list()
      for opponent in self.players:
        if not opponent == player:
          opponents.append(opponent)
      player.opponents = opponents

    self.in_progress = True

  def deal_from_deck(self, num_cards=1):
    dealt_cards = list()
    for i in range(0,num_cards):
      dealt_cards.append( self.game_deck.pick_from_top() )
    return dealt_cards

  def do_round(self):
    for player in self.players:
      player.take_turn()

    if len(self.game_deck.cards) == 0:
      self.in_progress = False

"""
main class
"""
def main():
  go_fish_game = GoFishGame()

  go_fish_game.add_player("AIBot1",True)
  go_fish_game.add_player("AIBot2",True)
  #go_fish_game.add_player("AIBot3",True)

  go_fish_game.start_game()

  while go_fish_game.in_progress:
    go_fish_game.do_round()

if __name__ == "__main__":
  main()
