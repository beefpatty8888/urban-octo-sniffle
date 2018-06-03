#! /usr/bin/env python3

import argparse

import digitalocean
import logging

import os

import sys

class createDroplet:
   def __init__(self, dropletSize, token):
     logger.debug ("Creating droplet of size "+dropletSize)
     self.token = token

   def setDroplet(self, size):
     droplet = digitalocean.Droplet(token=self.token,
                               name='TestDroplet',
                               region='nyc3', # New York 3
                               image='ubuntu-18-04-x64',
                               size_slug=size,
                               private_networking=True, 
                               backups=True)
     droplet.create()

class listDroplets:
   def __init__(self, token):
     self.token = token

   def getList(self):

     logger.debug ("Listing droplets")

     manager = digitalocean.Manager(token=self.token)
     myDroplets = manager.get_all_droplets()
     logger.debug(myDroplets)
 
     # see https://developers.digitalocean.com/documentation/v2/#list-all-droplets
     # for all attributes in the response.
     for droplet in myDroplets:
        logger.debug(str(droplet.id) + 
                         ";" + droplet.name + 
                         ";" + droplet.image["distribution"] + 
                         ";" + str(droplet.networks["v4"]))

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
     if args.size != None:
       createDroplet (args.size, os.getenv("DO_API_TOKEN")).setDroplet(args.size)

     elif args.size == None:
       logger.error ("The slug for the size of the instance must be specified.")
       logger.error ("See https://developers.digitalocean.com/documentation/changelog/api-v2/new-size-slugs-for-droplet-plan-changes/")

   if args.list == True:
     listDO = listDroplets(os.getenv("DO_API_TOKEN"))
     listDO.getList()

if __name__ == "__main__":
   main()
