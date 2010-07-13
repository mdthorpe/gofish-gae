from google.appengine.ext import webapp

from models import *

class NewGame(webapp.RequestHandler):
  def get(self):
    game = Game().save()
    self.redirect('/game/' + str(game.id()) )

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
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Main Game Menu')

