import datetime
import digitalocean
import logging

class createVolume:
   def __init__(self, token):
     self.logger = logging.getLogger(__name__)
     self.token = token
     self.volume = None

   def writeVolume(self, volumeSize, volumeDescription = None):
 
     self.volumeSize = volumeSize

     if volumeDescription == None:
        self.volumeDescription = "No description specified"
        volumeName = str(datetime.datetime.now())
     else:
        self.volumeDescription = str(volumeDescription)
        volumeName = volumeDescription+"_volume"

     self.logger.debug("Creating volume of size "+str(self.volumeSize))
     self.logger.debug("Creating volume of description "+self.volumeDescription)

     self.volume = digitalocean.Volume(token=self.token,
                                  size_gigabytes = int(self.volumeSize),
                                  name = volumeName,
                                  description = self.volumeDescription,
                                  region = 'nyc3' # static for now, though it should be a parameter.
                                  )
     self.volume.create()

   def attachVolume (self, dropletID, region):
     self.dropletID = dropletID
     self.region = region

     self.volume.attach(self.dropletID, self.region)
      
