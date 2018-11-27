import ipfsapi
import IOTATransaction
import IPportal
import json
import requests
Tag = 'HOWDOYOUTIRNTHISONIPPORTALC'
GroupKey = 'DOKUWIKI'
a = IPportal.IPportal('140.92.143.82',GroupKey)

role = 0
# Be a God
if role==0:
    TID = a.ToTheMoon(Tag)
    print(TID)

# Be a Dog
if role==1:
    GoodPeer = a.GetGoodPeer(Tag)
    print(GoodPeer)
    result = a.ConnectWithPeers(GoodPeer)
    print(result)
    for x in result:
        print(result[x])

# Be a Man
#if role==2:
#    print(b.GetTransactionMessage('QYRVTRWQSATSIVFYJTSEAJPWPUTYZSAWPDYLIMEQEFYAPLRLEJFHZKLWMZSZYWMDJDCMNKHCPLEYZ9999'))
