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
    self.response.out.write('<html><body>You wrote:<pre>')
    self.response.out.write(cgi.escape(self.request.get('nickname')))
    self.response.out.write('</pre></body></html>')
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
      deck = Deck()
      shuffled_cards = range(0,52)
      for x in range(0,5): random.shuffle(shuffled_cards)
      deck.cards = shuffled_cards
      deck.save()

      # Create new game
      game = Game(
          human_player=nickname, 
          num_ai_opponents=int(num_ai_opponents),
          game_deck=deck
      ).save()

      # Add Opponents
      for ai_opponent in range(0,int(num_ai_opponents)):
        ai_player = AiPlayer()
        ai_player.game = game
        ai_player.nickname = "AI_Player_"+str(ai_opponent+1)
        ai_player.save()

      self.redirect('/game/' + str( game.id() ) + '/start' )
    else:
      self.redirect('/game/new')


class GameHandler(webapp.RequestHandler):

  def get(self, game_id, action=None):
    nickname = self.request.cookies.get('nickname', '')

    try:
      game = Game.get_by_id(int(game_id))
    except:
      self.redirect('/')

    if action == 'start':
      game = Game.get_by_id(int(game_id))
      game.in_progress = True
      game.save()
      self.redirect('/game/' + str(game_id) )

    path = os.path.join(os.path.dirname(__file__), 'views/play_game.html')
    self.response.out.write(
        template.render(path, {
          'game_id': game_id,
          'nickname': nickname,
          'game': game,
          })
        )

class GameMenu(webapp.RequestHandler):

  def get(self):
    nickname = self.request.cookies.get('nickname')
    
    if nickname:
      path = os.path.join(os.path.dirname(__file__), 'views/main_menu.html')
      self.response.out.write(template.render(path, {'nickname': nickname}))
    else:
      self.redirect('/nickname/set')
          
