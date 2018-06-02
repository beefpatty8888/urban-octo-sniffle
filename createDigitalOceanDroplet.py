#! /usr/bin/python3

import argparse

import digitalocean
import logging

import os

def main():
   
   #http://docs.python-guide.org/en/latest/writing/logging/
   logger = logging.getLogger()
   streamHandler = logging.StreamHandler()
   formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
   streamHandler.setFormatter(formatter)
   logger.addHandler(streamHandler)

   fileHandler = logging.FileHandler("instance-creation.log")
   fileHandler.setFormatter(formatter)
   logger.addHandler(fileHandler)
   logger.setLevel(logging.DEBUG) 

   logger.debug ("Starting instance creation")

   parser = argparse.ArgumentParser()
   parser.add_argument("--size", type=str, help="Digital Ocean droplet size")
   args = parser.parse_args()

   # DO_API_TOKEN enviroment variable is used to be consistent
   # with ansible's digital_ocean module
   # http://docs.ansible.com/ansible/latest/modules/digital_ocean_module.html
   if args.size != None and os.getenv ("DO_API_TOKEN") != None:
     logger.debug ("Using DO Token " + os.getenv ("DO_API_TOKEN"))
     logger.debug ("Creating droplet of size " + args.size)
      
   elif os.getenv ("DO_API_TOKEN") == None:
     logger.debug ("System environment variable DO_API_TOKEN must be specified.")


if __name__ == "__main__":
   main()
