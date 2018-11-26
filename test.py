import ipfsapi
import IOTATransaction
import IPportal
import json
import requests
Tag = 'HOWDOYOUTIRNTHISONIPPORTALX'
GroupKey = 'DOKUWIKI'
From = 'HGW9HB9LJPYUGVHNGCPLFKKPNZAIIFHZBDHKSGMQKFMANUBASSMSV9TAJSSMPRZZU9SFZULXKJ9YLAIUA'

a = IPportal.IPportal('140.92.143.82',GroupKey)
b = IOTATransaction.IOTATransaction(From)

# Be a God
'''
T = b.GetTransactionsFromTag(Tag)
if len(T)==0:
    To = a.GetAddress()
    Message = a.GetMessageFromAddress(To)
    pt = b.MakePreparingTransaction(To,Message,Tag)
    b.SendTransaction([pt])
    print(b.GetTransactionHash())
'''

# Be a Dog
GoodPeer = set()
T = b.GetTransactionsFromTag(Tag)
for x in T:
    Tinfo = b.GetTransactionMessage(x) # address, message
    if a.CheckPeer(*Tinfo):
        GoodPeer.add(a.GetConnectionInfo(*Tinfo))
api = ipfsapi.connect('localhost','5001')
GoodPeer.add('/ip4/85.187.244.103/tcp/4001/ipfs/Qmd2LwsMA1gmaepDCosV9DCmRobZqJAFz4CRHbNy7RzJAE')
Rdict = dict()
for x in GoodPeer:
    try:
        output = api.swarm_connect(x)['Strings'][0].replace("\n","")
        tmp = output.split(" ")
        if tmp[2]=="success":
            Rdict[x] = "success"
    except Exception as e:
        Rdict[x] = str(e)

print(json.dumps(Rdict))
# Be a Man
#print(b.GetTransactionMessage('QYRVTRWQSATSIVFYJTSEAJPWPUTYZSAWPDYLIMEQEFYAPLRLEJFHZKLWMZSZYWMDJDCMNKHCPLEYZ9999'))
