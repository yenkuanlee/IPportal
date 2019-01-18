# coding=utf-8
import io
import ipfsapi
import json
import ObjectNode
import requests
import sys
api = ipfsapi.connect('127.0.0.1','5001')
def GetFhash(text):
    Tbyte = bytes(json.dumps({"Data":text}),encoding='utf8')
    ObjectHash = api.object_put(io.BytesIO(Tbyte))['Hash']
    api.pin_add(ObjectHash)
    return ObjectHash

## Register
Ehash = GetFhash('0x42946c2bb22ad422e7366d68d3ca07fb1862ff36')
ExternalIP = GetFhash('140.92.143.82')
Enode = GetFhash('999')
peerID = GetFhash('QmdxEc5zVVUTUSLZZhcbqWQMU6wnHPmVV8YfWXUcJ55xk4')
Rinfo = ObjectNode.ObjectNode()
Rinfo.new('彥寬提供的節點')
Rinfo.AddHash('Ehash',Ehash)
Rinfo.AddHash('ExternalIP',ExternalIP)
Rinfo.AddHash('Enode',Enode)
Rinfo.AddHash('peerID',peerID)

print(Rinfo.ObjectHash)
#user_info = {'fhash':Rinfo.ObjectHash}
#r = requests.post("http://61.66.218.208:8080/Register", data=user_info)
#print(r.text)
