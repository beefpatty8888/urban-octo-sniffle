#! /usr/bin/env python3

import argparse

import digitalocean
import logging

import os

import sys

#custom modules
import droplet.create
import droplet.list
import volume.create

def main():
   
   #http://docs.python-guide.org/en/latest/writing/logging/
   global logger 
   logger = logging.getLogger()
   streamHandler = logging.StreamHandler()
   formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
   streamHandler.setFormatter(formatter)
   logger.addHandler(streamHandler)

   fileHandler = logging.FileHandler("../instance-creation.log")
   fileHandler.setFormatter(formatter)
   logger.addHandler(fileHandler)
   logger.setLevel(logging.DEBUG) 

   logger.debug ("Starting script")

   parser = argparse.ArgumentParser()
   parser.add_argument ("--create", help="Create a Digital Ocean droplet", action="store_true")
   parser.add_argument("--size", type=str, help="Digital Ocean droplet size")
   parser.add_argument("--name", type=str, help="Digital Ocean droplet name")
   parser.add_argument("--volume", type=str, help="Digital Ocean block storage volume size in gigabytes")
   parser.add_argument ("--list", help="List Digital Ocean droplets", action="store_true")
   args = parser.parse_args()

   # https://stackoverflow.com/questions/10698468/argparse-check-if-any-arguments-have-been-passed
   if not len (sys.argv) > 1:
      logger.error ("Please specify a --list or --create flag.")

   # DO_API_TOKEN enviroment variable is used to be consistent
   # with ansible's digital_ocean module
   # http://docs.ansible.com/ansible/latest/modules/digital_ocean_module.html

   if os.getenv ("DO_API_TOKEN") == None:
      logger.error ("System environment variable DO_API_TOKEN must be specified.")
      sys.exit()
   else:
      logger.debug("Using token "+ os.getenv ("DO_API_TOKEN"))

   if args.create == True and args.list == True:
     logger.error ("Please specify only the --create or --list flag but not both.")
     sys.exit()

   if args.create == True: 

     
     # The logic here for arguments parsing seems to be getting too unwieldy ...
     if args.volume != None and args.size == None and args.name == None:
        # creation of the block storage volume, but does not attach
        volume.create.createVolume (os.getenv("DO_API_TOKEN")).writeVolume(args.volume, args.name)

     elif args.size != None and args.name != None and args.volume != None:

        # creation of the block storage volume, but does not attach
        VolumeCreation = volume.create.createVolume (os.getenv("DO_API_TOKEN"))
        VolumeCreation.writeVolume(args.volume, args.name)


        # create block storage before creating droplet ?
        # https://www.digitalocean.com/community/tutorials/an-introduction-to-digitalocean-block-storage
        dropletCreation = droplet.create.createDroplet (os.getenv("DO_API_TOKEN"))
        dropletCreation.writeDroplet(args.size, args.name)

        # attach the block storage volume to the new droplet.
        VolumeCreation.attachVolume (dropletCreation.dropletID, 'nyc3')

     elif args.size == None:
        logger.error ("The slug for the size of the instance must be specified.")
        logger.error ("See https://developers.digitalocean.com/documentation/changelog/api-v2/new-size-slugs-for-droplet-plan-changes/")
    
     elif args.name == None:
        logger.error ("Please specify the name for the Digital Ocean droplet.")

   if args.list == True:
     listDO = droplet.list.listDroplets(os.getenv("DO_API_TOKEN"))
     listDO.getList()

if __name__ == "__main__":
   main()
