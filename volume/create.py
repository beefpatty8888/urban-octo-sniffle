import datetime
import digitalocean
import logging

class createVolume:
   def __init__(self, token):
     self.logger = logging.getLogger(__name__)
     self.token = token
     self.volume = None

   def writeVolume(self, volumeSize, volumeDescription):
 
     self.volumeSize = volumeSize

     if volumeDescription == None:
        self.volumeDescription = "No droplet specified"
     else:
        self.volumeDescription = "For droplet "+str(volumeDescription)

     self.logger.debug("Creating volume of size "+self.volumeSize)
     self.logger.debug("Creating volume of description "+self.volumeDescription)

     self.volume = digitalocean.Volume(token=self.token,
                                  size_gigabytes = int(self.volumeSize),
                                  name = str(datetime.datetime.now()),
                                  description = self.volumeDescription,
                                  region = 'nyc3' # static for now, though it should be a parameter.
                                  )
     self.volume.create()

   def attachVolume (self, dropletID, region):
     self.dropletID = dropletID
     self.region = region

     self.volume.attach(self.dropletID, self.region)
      
