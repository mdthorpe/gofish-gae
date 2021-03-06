#!/usr/bin/env python

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

import views
import logging

def main():
    logging.getLogger().setLevel(logging.DEBUG)
    app = webapp.WSGIApplication(
         [
           ('/', views.GameMenu),
           ('/nickname/set/', views.SetNickHandler),
           ('/game/new/', views.NewGameHandler),
           ('/game/(\d+)/', views.GameHandler),
           ('/game/(\d+)/(.+)/', views.GameHandler),
         ],
         debug=True)

    run_wsgi_app(app)

if __name__ == "__main__":
    main()
