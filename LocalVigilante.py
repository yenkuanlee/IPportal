import IPportal
import json
import os
#import requests
import time
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/config.json') as f:
    Jconfig = json.load(f)
a = IPportal.IPportal(Jconfig['ExternalIP'],Jconfig['GroupKey'])
while True:
    try:
        a.LDBupdate()
        time.sleep(1)
    except:
        pass
