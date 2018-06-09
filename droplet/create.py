import digitalocean
import logging

class createDroplet:
   def __init__(self, dropletSize, token):
     
     # https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
     self.logger = logging.getLogger(__name__)
     self.logger.debug ("Creating droplet of size "+dropletSize)
     self.token = token

   def writeDroplet(self, size):
     droplet = digitalocean.Droplet(token=self.token,
                               name='TestDroplet',
                               region='nyc3', # New York 3
                               image='ubuntu-18-04-x64',
                               size_slug=size,
                               private_networking=True, 
                               backups=True)
     droplet.create()

     actions = droplet.get_actions()
     for action in actions:
        action.load()
        self.logger.debug("CREATION STATUS: " + action.status)
        # at some point, may want to look into my own loop
        # or recursion for additional logging, but the
        # built-in "action.wait()" in the the digitalocean
        # library should suffice.
        action.wait()
        self.logger.debug("CREATION STATUS: " + action.status)

