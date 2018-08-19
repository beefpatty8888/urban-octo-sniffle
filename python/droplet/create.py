import digitalocean
import logging

class createDroplet:
   def __init__(self, token):
     
     # https://fangpenlin.com/posts/2012/08/26/good-logging-practice-in-python/
     self.logger = logging.getLogger(__name__)
     self.token = token
     self.dropletID = None
     self.dropletIP = None

   def writeDroplet(self, size, name):

     self.logger.debug ("Creating droplet of size "+size)

     manager = digitalocean.Manager(token=self.token)
     keys = manager.get_all_sshkeys()

     droplet = digitalocean.Droplet(token=self.token,
                               name=name,
                               region='nyc3', # New York 3
                               image='ubuntu-18-04-x64',
                               size_slug=size,
                               private_networking=True,
                               ssh_keys=keys,
                               backups=True)
     droplet.create()

     actions = droplet.get_actions()
     for action in actions:
        action.load()
        self.logger.info("CREATION STATUS: " + action.status)
        # at some point, may want to look into my own loop
        # or recursion for additional logging, but the
        # built-in "action.wait()" in the the digitalocean
        # library should suffice.
        action.wait()
        self.logger.info("CREATION STATUS: " + action.status)

     self.dropletID = droplet.id
     self.dropletIP = droplet.load().ip_address
 

     self.logger.info("Droplet ID: "+str(self.dropletID))
     self.logger.info("Droplet IP: "+str(self.dropletIP))




