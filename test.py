#import ipfsapi
import IPportal
import json
import os
import requests
Cpath = os.path.dirname(os.path.realpath(__file__))
with open(Cpath+'/config.json') as f:
    Jconfig = json.load(f)
a = IPportal.IPportal(Jconfig['ExternalIP'],Jconfig['GroupKey'])

role = 0
# Be a God
if role==0:
    TID = a.ToTheMoon(Jconfig['Tag'])
    print(TID)

# Be a Dog
if role==1:
    GoodPeer = a.GetGoodPeer(Jconfig['Tag'])
    print(GoodPeer)
    #result = a.ConnectWithPeers(GoodPeer)
    #print(result)
    '''
    cnt = 0
    Exsited = False
    for x in result:
        if result[x]=='success':
            cnt += 1
        elif 'dial to self attempted' in result[x]:
            Exsited = True
    if cnt > 0 and not Exsited:
        TID = a.ToTheMoon(Jconfig['Tag'])
        print(TID)
    '''
