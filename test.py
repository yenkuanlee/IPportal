import ipfsapi
import IPportal
import json
import requests
Tag = 'HOWDOYOUTIRNTHISONIPPORTALC'
GroupKey = 'DOKUWIKI'
a = IPportal.IPportal('140.92.143.82',GroupKey)

role = 1
# Be a God
if role==0:
    TID = a.ToTheMoon(Tag)
    print(TID)

# Be a Dog
if role==1:
    GoodPeer = a.GetGoodPeer(Tag)
    #print(GoodPeer)
    result = a.ConnectWithPeers(GoodPeer)
    #print(result)
    cnt = 0
    Exsited = False
    for x in result:
        if result[x]=='success':
            cnt += 1
        elif 'dial to self attempted' in result[x]:
            Exsited = True
    if cnt > 0 and not Exsited:
        TID = a.ToTheMoon(Tag)
        print(TID)
