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
import firewall.create

def main():
   
   #http://docs.python-guide.org/en/latest/writing/logging/
   global logger 
   logger = logging.getLogger()
   streamHandler = logging.StreamHandler()
   formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
   streamHandler.setFormatter(formatter)
   streamHandler.setLevel(logging.INFO)
   logger.addHandler(streamHandler)

   fileHandler = logging.FileHandler("../../instance-creation.log")
   fileHandler.setFormatter(formatter)
   fileHandler.setLevel(logging.DEBUG)
   logger.addHandler(fileHandler)
   logger.setLevel(logging.DEBUG) 

   logger.info ("Starting script")

   parser = argparse.ArgumentParser()

   # https://stackoverflow.com/questions/10448200/how-to-parse-multiple-nested-sub-commands-using-python-argparse/49977713#49977713
   # https://docs.python.org/3.6/library/argparse.html
   subparsers = parser.add_subparsers(dest="subparser_name")
   createVolumeArgs = subparsers.add_parser("volume", help="Create a Digital Ocean block storage volume only")
   createVolumeArgs.add_argument("--volume_size", type=int, help="Size of the block storage volume, in gigabytes", required=True)
   createDropletArgsSubParser = subparsers.add_parser('create', help="Create a Digital Ocean droplet")
   createDropletArgsSubParser.add_argument("--droplet_size", type=str, help="Digital Ocean droplet size slug. See https://developers.digitalocean.com/documentation/changelog/api-v2/new-size-slugs-for-droplet-plan-changes/ ", required=True)
   createDropletArgsSubParser.add_argument("--name", type=str, help="Digital Ocean droplet name", required=True)
   createDropletArgsSubParser.add_argument("--volume", type=int, help="Create a block storage volume, in gigabytes, with the Digital Ocean droplet")
   createDropletArgsSubParser.add_argument("--firewall", action="store_true")
   listDropetsArgs = subparsers.add_parser ("list", help="List Digital Ocean droplets")
   args = parser.parse_args()

   # https://stackoverflow.com/questions/10698468/argparse-check-if-any-arguments-have-been-passed
   if not len (sys.argv) > 1:
      logger.error ("Please specify a list, volume or create command.")

   # DO_API_TOKEN enviroment variable is used to be consistent
   # with ansible's digital_ocean module
   # http://docs.ansible.com/ansible/latest/modules/digital_ocean_module.html

   if os.getenv ("DO_API_TOKEN") == None:
      logger.error ("System environment variable DO_API_TOKEN must be specified.")
      sys.exit()
   else:
      logger.debug("Using token "+ os.getenv ("DO_API_TOKEN"))

   # probably refactor this using "set_defaults" (https://codereview.stackexchange.com/questions/93301/argparse-with-subparsers) ?
   if args.subparser_name == "volume":
     # creation of the block storage volume, but does not attach
     VolumeCreation = volume.create.createVolume (os.getenv("DO_API_TOKEN"))
     VolumeCreation.writeVolume(args.volume_size)

   if args.subparser_name == "create":
     if args.volume:
       # creation of the block storage volume, but does not attach
       VolumeCreation = volume.create.createVolume (os.getenv("DO_API_TOKEN"))
       VolumeCreation.writeVolume(args.volume, args.name)
     
     dropletCreation = droplet.create.createDroplet (os.getenv("DO_API_TOKEN"))
     dropletCreation.writeDroplet(args.droplet_size, args.name)

     if args.firewall:
       dropletFirewall = firewall.create.createFirewall(os.getenv("DO_API_TOKEN"))
       dropletFirewall.writeFirewall(args.name)
       dropletFirewall.attachFirewall(dropletCreation.dropletID)

     if args.volume:
       # attach the block storage volume to the new droplet.
       VolumeCreation.attachVolume (dropletCreation.dropletID, 'nyc3')


   if args.subparser_name == "list":
     print ("listing droplets")
     listDO = droplet.list.listDroplets(os.getenv("DO_API_TOKEN"))
     listDO.getList()

if __name__ == "__main__":
   main()
