from multiprocessing import Process
import time
from utils.model import Config

# global config
config = Config(".env")

def updateNodeRoutine(config: Config):
    def start() -> Process:
        p = Process(target=config.start_node, args=[])
        p.start()
        return p
    p = start()
    while True:
        time.sleep(90)  # update every 30 seconds
        lastVersion = config.version
        if config.updateLocalVersion():
            p.kill()  
            start()
            config.sendmail(title=f"Sentry SOFTWARE UPDATED to {config.version}.", content=f"Last version was:{lastVersion}.")

    
updateNodeRoutine(config)