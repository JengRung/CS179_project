from datetime import datetime
import os

class LogDriver:
    def __init__(self, log_file):
        self.log_file = log_file
        self.user = None

        #[+]--------------------------------------------------\\
        absPath= os.path.realpath(__file__)
        thisPath= os.path.dirname(absPath)

        self.log_file= os.path.join(thisPath, log_file)
    
    def log(self, message):
        with open(self.log_file, 'a') as f:
            f.write(message + '\n')
            
    def login(self, user):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.user = user
        self.log(f"{time}  {self.user} signs in ")
    
    def logout(self):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {self.user} signs out ")
        self.user = None
        
    def offload(self, container):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {container} is offloaded to the truck")
        
    def onload(self, container, coord):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {container} is onloaded at coordinate {coord}")
        
    def openManifest(self, manifest, container_cnt):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {manifest} is opened, there are {container_cnt} containers on the ship")
        
    def finishCycle(self, manifest):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  Finished a Cycle. Manifest {manifest} was written to desktop, and a reminder pop-up to operator to send file was displayed.")
        
    def moveInsideShip(self, container, from_location, to_location):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {container} is moved from {from_location} to {to_location}")
        
    def comment(self, comment):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {self.user} comment: {comment}")

    #[+]---
    def error(self, msg):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {self.user} ErrorMessage: {msg}")
