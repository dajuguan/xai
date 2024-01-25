import os
import sys
import subprocess
import time
from subprocess import Popen, PIPE, STDOUT
import json
import logging
from dataclasses import dataclass
import unittest
import requests
from utils.model import Config
from multiprocessing import Process


# global config
ENV_PATH = ".env_copy"
config = Config(ENV_PATH)

def checkLatestReleaseTag():
    response = requests.get(f"https://api.github.com/repos/xai-foundation/sentry/releases/latest")
    tag = response.json()["tag_name"]
    print("latest tag is:", tag)
    return tag

def updateLocalVersion(config: Config) -> bool:
    tag = checkLatestReleaseTag()
    if config.version != tag:
        print(f"latest version is: {tag}, updating......................")
        os.system(f"curl -L -o sentry-node-cli-linux.zip https://github.com/xai-foundation/sentry/releases/latest/download/sentry-node-cli-linux.zip")
        os.system(f"unzip -f sentry-node-cli-linux.zip")
        config.version = tag
        config.dump()
        return True
    return False

def updateNodeRoutine(config: Config):
    def targetFn(config: Config):
        print("running subprocess with version:", config.version)
        while True:
            a = 1

    p = Process(target=targetFn, args=[config])
    p.start()

    tries = 0
    while True:
        if updateLocalVersion(config):
            p.terminate()  
            p = Process(target=targetFn, args=[config])
            p.start()

        time.sleep(1)
        if tries == 2:
            p.kill()
            break
        tries += 1

def subprocess():
    def targetFn():
        try: 
            while True:
                print("aaa")
                time.sleep(0.1)
        except Exception as e:
            print("catch exception")

    p = Process(target=targetFn)
    p.start() 

    time.sleep(0.5)
    p.kill()
    p.join()
   


class TestSuite(unittest.TestCase):
    # @classmethod
    # def tearDownClass(cls):
    #     config.version = ""
    #     config.dump()
    # def testGetRelease(self):
    #     config._checkLatestReleaseTag()
    # def testUpdateLocalVersion(self):
    #     config.updateLocalVersion()
    # def testMockUpdate(self):
    #     updateNodeRoutine(config)
    def testKillSubprocess(self):
        subprocess()

if __name__ == "__main__":
    unittest.main()
