import os
import cgi
import random

from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from models import *

class SetNickHandler(webapp.RequestHandler):

  def get(self):
    path = os.path.join(os.path.dirname(__file__), 'views/set_nick.html')
    self.response.out.write(template.render(path, {}))

  def post(self):
    nickname = cgi.escape(self.request.get('nickname'))
    self.response.headers.add_header('Set-Cookie','nickname='+nickname+'; expires:Tue, 19-Jan-2038 03:14:18 UTC; path=/;')
    self.redirect('/')


class NewGameHandler(webapp.RequestHandler):

  def get(self):
    nickname = self.request.cookies.get('nickname', '')
    if nickname:
      path = os.path.join(os.path.dirname(__file__), 'views/new_game.html')
      self.response.out.write(template.render(path, {'nickname': nickname}))
    else:
      self.redirect('/')

  def post(self):
    """
    Setup a new game
    """
    nickname = self.request.cookies.get('nickname', '')
    num_ai_opponents = cgi.escape(self.request.get('num_ai_opponents'))

    if nickname and num_ai_opponents:
      # Create new game deck
      deck = Hand()
      shuffled_cards = range(0,52)
      for x in range(0,5): random.shuffle(shuffled_cards)
      deck.cards = shuffled_cards
      deck.save()

      # Create new game
      game = Game(deck=deck).save()

      # Add Player
      human_player = Player(nickname=nickname, game=game, hand=Hand().save())
      human_player.save()

      # Add Opponents
      for ai_opponent in range(0,int(num_ai_opponents)):
        ai_player = AiPlayer()
        ai_player.game = game
        ai_player.nickname = "AI_Player_"+str(ai_opponent+1)
        ai_player.hand = Hand().save()
        ai_player.save()

      self.redirect('/game/' + str( game.id() ) + '/' )
    else:
      self.redirect('/game/new/')


class GameHandler(webapp.RequestHandler):

  def get(self, game_id, action=None):
    nickname = self.request.cookies.get('nickname', '')

    try:
      game = Game.get_by_id(int(game_id))
    except:
      self.redirect('/')
      return

    if game is None: 
      self.redirect('/')
      return

    try:
      human_player = Player.all().filter('game =', game.key()).fetch(1)[0]
      ai_players = AiPlayer.all().filter('game =', game.key()).fetch(10)
    except AttributeError, why:
      self.redirect('/')
      return

    # handle game actions that use GET
    if action == "deal":
      self.deal_cards(game, [human_player])
      self.deal_cards(game, ai_players)
      self.redirect('/game/'+str(game_id)+'/')

    game_events = GameEvent.all().filter('game =', game.key()).order("-time").fetch(25)
 
    # Write out the view
    path = os.path.join(os.path.dirname(__file__), 'views/play_game.html')
    self.response.out.write(
        template.render(path, {
          'game_id': game_id,
          'deck':  game.deck.get_cards(),
          'game': game,
          'human_player' : human_player,
          'ai_players' : ai_players,
          'game_events' : game_events,
          })
        )

  def post(self, game_id, action=None):

    # Handle game actions that use POST
    if action == "ask":
      # Do human player turn
      ask_opponent = cgi.escape(self.request.get('ask_opponent'))
      ask_value = cgi.escape(self.request.get('ask_value'))

      game = Game.get_by_id(int(game_id))
      human_player = Player.all().filter('game =', game.key()).fetch(1)[0]
      ai_opponent = AiPlayer.get(ask_opponent)

      human_player.ask_for_value(ai_opponent,ask_value)
      human_player.search_books()

      # Do ai players turns
      for ai_player in AiPlayer.all().filter('game =', game.key()).fetch(10):
        # Ask a random player for a card of a random value
        ai_player.ask_for_value(ai_player.random_opponent(), ai_player.random_card_value())
        ai_player.search_books()

      self.redirect('/game/'+str(game_id)+'/')
      return
    

  def deal_cards(self,game,players):
    for player in players:
      player.take_cards(game.deck,7)
    game.in_progress=True
    game.save()

  def card_value(self, card_number):
    return (card/4)+1


class GameMenu(webapp.RequestHandler):

  def get(self):
    nickname = self.request.cookies.get('nickname')
    
    if nickname:
      path = os.path.join(os.path.dirname(__file__), 'views/main_menu.html')
      self.response.out.write(template.render(path, {'nickname': nickname}))
    else:
      self.redirect('/nickname/set/')
          
