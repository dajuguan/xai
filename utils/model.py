from dataclasses import dataclass
import json
import os
import subprocess
import time
import requests
import smtplib, ssl

@dataclass
class Config:
    prv_key: str
    email: str
    email_passwd: str
    receiver_email: str
    version: str
    env_path: str
    github_token: str | None

    # initialize config and update local version on start
    def __init__(self, env_path=".env"): 
        with open(env_path) as f:
            conf = json.load(f)
            self.email = conf["email"]
            self.email_passwd = conf["email_passwd"]
            self.prv_key = conf["prv_key"]
            self.receiver_email = conf["receiver_email"]
            self.version = conf["version"]
            self.github_token = conf["github_token"]
            self.env_path = env_path

            self.updateLocalVersion()
    def _toJSON(self) -> str:
        serialized = json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)
        return json.loads(serialized)
    def dump(self):
        f = open(self.env_path, "w")
        json.dump(self._toJSON(), f, separators=(',', ':'), indent=4)
        f.close()
    def _checkLatestReleaseTag(self) -> str:
        headers = None
        if self.github_token != None and self.github_token !="":
            headers = {'Authorization': 'token ' + self.github_token}
        response = requests.get(f"https://api.github.com/repos/xai-foundation/sentry/releases/latest", headers=headers)
        if response.status_code != 200:
            raise Exception('''Rate limited(60 requests/hour) by Github.
                Please refer https://docs.github.com/en/rest/quickstart?#authenticating-with-an-access-token-2
                to increase it to 1500 requests/hour.''')
        tag = response.json()["tag_name"]
        print("latest sentry release tag is:", tag)
        return tag
    def updateLocalVersion(self) -> bool:
        tag = self._checkLatestReleaseTag()
        if self.version != tag:
            print(f"latest version is: {tag}, updating......................")
            os.system(f"curl -L -o sentry-node-cli-linux.zip https://github.com/xai-foundation/sentry/releases/latest/download/sentry-node-cli-linux.zip")
            os.system(f"unzip -o sentry-node-cli-linux.zip")
            self.version = tag
            self.dump()
            return True
        return False
    def sendmail(self, title, content):
        port = 587  # For starttls
        smtp_server = "smtp.gmail.com"
        sender_email = self.email
        receiver_email = self.receiver_email
        password = self.email_passwd
        message = f"""Subject: {title}!
        {content}."""

        context = ssl.create_default_context()
        with smtplib.SMTP(smtp_server, port) as server:
            server.ehlo()  # Can be omitted
            server.starttls(context=context)
            server.ehlo()  # Can be omitted
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message)
    def start_node(self):
        try:
            proc = subprocess.Popen("./sentry-node-cli-linux", stdin=subprocess.PIPE, text=True)
            # -----------------boot-operator-------------------------#
            proc.stdin.write('boot-operator\n')
            proc.stdin.write(self.prv_key+"\n")
            proc.stdin.flush()
            time.sleep(0.5)
            # -----------------provision select------------------------------#
            proc.stdin.write('y\n')
            proc.stdin.flush()
            time.sleep(0.5)
            proc.stdin.write(' \n\n')
            proc.stdin.flush()
            print("running sentry node with version======>:", self.version)
            returncode = proc.wait()
            raise subprocess.CalledProcessError(returncode, cmd="sentry-node-cli-linux",stderr=proc.stderr)

        except Exception as e:
            self.sendmail(title="Sentry node is down", content="Please restart it on server!")
            print("node exit==============>",e)