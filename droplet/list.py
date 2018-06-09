import digitalocean
import logging

class listDroplets:
   def __init__(self, token):
     self.token = token

   def getList(self):
     self.logger = logging.getLogger(__name__)
     self.logger.debug ("Listing droplets")

     manager = digitalocean.Manager(token=self.token)
     myDroplets = manager.get_all_droplets()
     self.logger.debug(myDroplets)
 
     # see https://developers.digitalocean.com/documentation/v2/#list-all-droplets
     # for all attributes in the response.
     for droplet in myDroplets:
        self.logger.debug(str(droplet.id) + 
                         ";" + droplet.name + 
                         ";" + droplet.image["distribution"] + 
                         ";" + str(droplet.networks["v4"]))

