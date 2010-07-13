from google.appengine.ext import webapp

import models

class NewGame(webapp.RequestHandler):
  def get(self):
    game = Game().save()
    self.redirect('/game/' + str(game.id) )

class GameHandler(webapp.RequestHandler):
  def get(self, game_id):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Playing Game: ' + str(game_id) )

class GameMenu(webapp.RequestHandler):
  def get(self):
    self.response.headers['Content-Type'] = 'text/plain'
    self.response.out.write('Hello, webapp World!')

