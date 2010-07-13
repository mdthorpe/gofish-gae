import os
import cgi

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
    self.response.headers.add_header('Set-Cookie','nickname='+nickname+'; expires:Sun, 31-May-2050 23:59:59 GMT; path=/;')
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
    nickname = self.request.cookies.get('nickname', '')
    num_ai_opponents = cgi.escape(self.request.get('num_ai_opponents'))
    if nickname and num_ai_opponents:
      game = Game(human_player=nickname, num_ai_opponents=int(num_ai_opponents)).save()
      self.redirect('/game/' + str( game.id() ) + '/start' )
    else:
      self.redirect('/game/new')


class GameHandler(webapp.RequestHandler):
  def get(self, game_id, action=None):

    try:
      game = Game.get_by_id(int(game_id))
    except:
      self.redirect('/')

    if action == 'start':
      game = Game.get_by_id(int(game_id))
      game.in_progress = True
      game.save()
      self.redirect('/game/' + str(game_id) )

    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Playing Game: ' + game_id )


class GameMenu(webapp.RequestHandler):
  def get(self):
    nickname = self.request.cookies.get('nickname')
    
    if nickname:
      path = os.path.join(os.path.dirname(__file__), 'views/main_menu.html')
      self.response.out.write(template.render(path, {'nickname': nickname}))
    else:
      self.redirect('/nickname/set')
          
