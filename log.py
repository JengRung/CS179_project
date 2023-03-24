from datetime import datetime

class LogDriver:
    def __init__(self, log_file):
        self.log_file = log_file
        self.user = None

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
        self.log(f"{time}  {container} is offloaded")
        
    def onload(self, container):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {container} is onloaded")
        
    def openManifest(self, manifest):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  {manifest} is opened")
        
    def finishCycle(self, manifest):
        time = datetime.now().replace(second=0, microsecond=0).strftime("%Y-%m-%d %H:%M")
        self.log(f"{time}  Finished a Cycle. Manifest {manifest} was written to desktop, and a reminder pop-up to operator to send file was displayed.")